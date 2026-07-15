
from celery import shared_task
from extensions import db, mail
from flask import render_template, current_app
from flask_mail import Message
from datetime import timedelta, datetime
from models import User, UserRole, Trek, Trekker, BookingStatus
import csv
import os


@shared_task(bind=True)
def send_trek_reminder(self, trek_id):
    print(f"Sending reminder for trek ID: {trek_id}")
    return f"Reminder for trek ID {trek_id} has been sent."
    
@shared_task(bind=True)
def send_say_hii(self, user_id):
    print(f"Sending 'Say Hi' message to user ID: {user_id}")
    return f"'Say Hi' message sent to user ID {user_id}."


@shared_task(bind=True)
def user_daily_reminder_mail(self, user_email, user_name, trek_name, start_date, meeting_time, meeting_location, trek_leader_name, trek_leader_phone):
    try:
        msg = Message(
            subject=f"⛰️ Reminder: Your upcoming trek to {trek_name}!",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=[user_email]
        )
        html_body = render_template('user_email.html',userName=user_name,
            trekName=trek_name,
            startDate=start_date,
            meetingTime=meeting_time,
            meetingLocation=meeting_location,
            trekLeaderName=trek_leader_name,
            trekLeaderPhone=trek_leader_phone)
        
        msg.html = html_body
        msg.body = f"Hi {user_name}, this is a reminder for your trek to {trek_name} on {start_date}."
        mail.send(msg)
        
        print(msg)
        return "Daily morning reminders have been sent."
    except Exception as e:
        raise e
    
@shared_task(bind=True)
def send_daily_morning_reminders(self):
    target_date = datetime.utcnow().date() + timedelta(days=3)
    upcomming_treks = Trek.query.filter(Trek.start_date >= target_date).all()
    participants = Trekker.query.all()
    
    for trek in upcomming_treks:
        for participant in participants:
            print(participant.user)
            user_daily_reminder_mail.delay(
                user_email=participant.user.email,
                user_name=participant.user.username,
                trek_name=trek.trek_name,
                start_date=trek.start_date.strftime("%B %d, %Y"),
                meeting_time=trek.start_date,
                meeting_location=trek.location,
                trek_leader_name=trek.staff.username,
                trek_leader_phone=trek.staff.staff_profile.contact_details
            )
            
            print(f"Sending daily morning reminders for {participant.user.username}")
            print(f"Trek Name: {trek.trek_name}")
            print(f"Start Date: {trek.start_date}")
            print(f"Meeting Time: {trek.start_date}")
            print(f"Meeting Location: {trek.location}")
            print(f"Trek Leader Name: {trek.staff.username}")
            print(f"Trek Leader Phone: {trek.staff.staff_profile.contact_details}")
            # print(f"Instructions: {instructions_html}")
    
    return "Daily morning reminders have been sent."


@shared_task(bind=True)
def admin_monthly_report_mail(self, admin_email, admin_name, month_year, total_treks, total_participants, popular_treks):
    try:
        msg = Message(
            subject=f"📊 Monthly Trekking Report: {month_year}",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=[admin_email]
        )
        
        html_body = render_template(
            'admin_monthly_report.html',
            adminName=admin_name,
            month_year=month_year,
            total_treks=total_treks,
            total_participants=total_participants,
            popular_treks=popular_treks
        )
        
        msg.html = html_body
        msg.body = f"Hi {admin_name}, a total of {total_treks} treks were conducted in {month_year} with {total_participants} participants."
        
        mail.send(msg)
        print(f"Monthly report sent to {admin_email}")
        
        return "Monthly report sent successfully."
    except Exception as e:
        raise e

@shared_task(bind=True)
def generate_monthly_trek_reports(self):
    try:
        today = datetime.utcnow().date()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        start_dt = datetime.combine(first_day_last_month, datetime.min.time())
        end_dt = datetime.combine(last_day_last_month, datetime.max.time())
        
        month_year_str = first_day_last_month.strftime("%B %Y")
        
        treks_last_month = Trek.query.filter(
            Trek.start_date >= start_dt,
            Trek.start_date <= end_dt
        ).all()
        
        total_treks = len(treks_last_month)
        
        total_participants = 0
        trek_stats = []
        
        for trek in treks_last_month:
            # Count only bookings that are NOT cancelled
            valid_bookings = [b for b in trek.bookings if b.status != BookingStatus.CANCELLED]
            participant_count = len(valid_bookings)
            
            total_participants += participant_count
            
            trek_stats.append({
                "name": trek.trek_name,
                "count": participant_count
            })
            
        trek_stats.sort(key=lambda x: x['count'], reverse=True)
        popular_treks = trek_stats[:5]

        admins = User.query.filter(User.role == UserRole.ADMIN).all()
        
        for admin in admins:
            admin_monthly_report_mail.delay(
                admin_email=admin.email,
                admin_name=admin.username,
                month_year=month_year_str,
                total_treks=total_treks,
                total_participants=total_participants,
                popular_treks=popular_treks
            )
            print(f"Queued monthly report for Admin: {admin.username}")
            
        return f"Monthly admin reports queued for {len(admins)} admins."
        
    except Exception as e:
        raise e

@shared_task(bind=True)
def export_booking_history_csv(self, user_id):
    try:
        from models import Booking, User
        from extensions import db, mail
        from flask import current_app
        from flask_mail import Message

        task_id = self.request.id

        export_dir = os.path.join(current_app.root_path, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, f'{task_id}.csv')

        user = User.query.get(user_id)
        bookings = Booking.query.filter_by(user_id=user_id).all()

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'User ID', 'Trek Name', 'Location',
                'Booking Status', 'Start Date', 'End Date', 'Booking Date'
            ])
            for b in bookings:
                writer.writerow([
                    b.user_id,
                    b.treks.trek_name if b.treks else 'Unknown Trek',
                    b.treks.location if b.treks else '',
                    b.status.value if b.status else 'Booked',
                    b.treks.start_date.strftime('%Y-%m-%d') if (b.treks and b.treks.start_date) else '',
                    b.treks.end_date.strftime('%Y-%m-%d') if (b.treks and b.treks.end_date) else '',
                    b.booking_date.strftime('%Y-%m-%d %H:%M') if b.booking_date else '',
                ])

        # ── 4. Send e-mail alert ─────────────────────────────────────────────
        if user and user.email:
            msg = Message(
                subject='✅ Your Booking History Export is Ready!',
                sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
                recipients=[user.email]
            )
            msg.body = (
                f"Hi {user.username},\n\n"
                "Your trekking booking history CSV export has been completed.\n"
                "You can download it from your dashboard.\n\n"
                "— Trekking Management System"
            )
            mail.send(msg)

        return {'status': 'SUCCESS', 'file_path': file_path}

    except Exception as e:
        raise e