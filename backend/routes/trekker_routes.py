
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from celery.result import AsyncResult
from flask import send_file
from tasks import export_booking_history_csv

trekker_bp = Blueprint('trekker', __name__)

@trekker_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    current_user_id = get_jwt_identity()
    # print(current_user_id)
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()
    # print(trekker_profile)
    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    total_treks = Trek.query.count()
    total_bookings = Booking.query.filter_by(user_id=current_user_id).count()

    print({
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })
    return jsonify({
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })
    

@trekker_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_treks():
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()

    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    treks = Trek.query.all()
    trek_list = []
    for trek in treks:
        if trek.status in [TrekStatus.APPROVED, TrekStatus.OPEN]:
            duration = (trek.end_date - trek.start_date).days if (trek.end_date and trek.start_date) else 1
            trek_list.append({
                "id": trek.id, 
                "trek_name": trek.trek_name, 
                "location": trek.location, 
                "difficulty": trek.difficulty.value if trek.difficulty else "Easy", 
                "available_slots": trek.available_slots,
                "start_date": trek.start_date.strftime('%Y-%m-%d') if trek.start_date else "",
                "end_date": trek.end_date.strftime('%Y-%m-%d') if trek.end_date else "",
                "duration_days": duration if duration > 0 else 1,
                "status": trek.status.value if trek.status else "Open",
                # "alread_booked": True if trek.bookings.filter_by(user_id=current_user_id).first() else False
            })
        # print(trek.bookings)
    
    return jsonify({"treks": trek_list}), 200
    

@trekker_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()

    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    history = Booking.query.filter_by(user_id=trekker_profile.user_id).all()
    history_list = [{
        "id": b.id, 
        "user_id": b.user_id, 
        "trek_id": b.trek_id, 
        "trek_name": b.treks.trek_name if b.treks else "Unknown Trek",
        "location": b.treks.location if b.treks else "",
        "difficulty": b.treks.difficulty.value if (b.treks and b.treks.difficulty) else "Easy",
        "start_date": b.treks.start_date.strftime('%Y-%m-%d') if (b.treks and b.treks.start_date) else "",
        "end_date": b.treks.end_date.strftime('%Y-%m-%d') if (b.treks and b.treks.end_date) else "",
        "booking_date": b.booking_date.strftime('%Y-%m-%d %H:%M') if b.booking_date else "", 
        "status": b.status.value if b.status else "Booked"
    } for b in history]

    return jsonify({"history": history_list}), 200

@trekker_bp.route('/book-trek/<int:trek_id>', methods=['POST'])
@jwt_required()
def book_trek(trek_id):
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trekker_profile or not trek:
        return jsonify({"error": "Trekker profile or trek not found"}), 404
    
    if trek.status != TrekStatus.OPEN:
        return jsonify({"error": "Trek is not open"}), 400
    
    if trek.available_slots == 0:
        return jsonify({"error": "No slots available"}), 400
    
    is_booked = Booking.query.filter_by(user_id=current_user_id, trek_id=trek_id).first()
    already_booked = False
    if is_booked:
        already_booked = True
        return jsonify({"error": "Already booked this trek"}), 400
    
    trek.available_slots -= 1
    booking = Booking(user_id=current_user_id, trek_id=trek_id)
    
    db.session.add(booking)
    db.session.commit()
    
    print({"message": "Booking created successfully", "booking": {
        "id": booking.id, 
        "user_id": booking.user_id, 
        "trek_id": booking.trek_id, 
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else "Easy",
        "start_date": trek.start_date.strftime('%Y-%m-%d') if trek.start_date else "",
        "end_date": trek.end_date.strftime('%Y-%m-%d') if trek.end_date else "",
        "booking_date": booking.booking_date.strftime('%Y-%m-%d %H:%M') if booking.booking_date else "", 
        "already_booked": already_booked,
        "status": booking.status.value if booking.status else "Booked"
    }})

    return jsonify({"message": "Booking created successfully", "booking": {
        "id": booking.id, 
        "user_id": booking.user_id, 
        "trek_id": booking.trek_id, 
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else "Easy",
        "start_date": trek.start_date.strftime('%Y-%m-%d') if trek.start_date else "",
        "end_date": trek.end_date.strftime('%Y-%m-%d') if trek.end_date else "",
        "booking_date": booking.booking_date.strftime('%Y-%m-%d %H:%M') if booking.booking_date else "", 
        "already_booked": already_booked,
        "status": booking.status.value if booking.status else "Booked"
    }}), 201


@trekker_bp.route('/update-booking-status/<int:booking_id>', methods=['PATCH'])
@jwt_required()
def update_booking_status(booking_id):
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()

    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    booking = Booking.query.filter_by(id=booking_id).first()

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in [status.value for status in BookingStatus]:
        return jsonify({"error": "Invalid status value"}), 400
    
    booking.status = BookingStatus(new_status)
    db.session.commit()

    return jsonify({"message": "Booking status updated successfully", "booking": {"id": booking.id, "status": booking.status.value}}), 200


@trekker_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()
    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    user = User.query.get(int(current_user_id))
    return jsonify({
        "username": user.username if user else "",
        "email": user.email if user else "",
        "role": user.role.value if user else "Trekker",
        "full_name": trekker_profile.full_name or "",
        "age": trekker_profile.age,
        "phone": trekker_profile.phone or "",
        "bio": trekker_profile.bio or "",
        "emergency_contact": trekker_profile.emergency_contact or "",
        "blacklisted": trekker_profile.blacklisted,
        "member_since": trekker_profile.created_at.strftime('%Y-%m-%d') if trekker_profile.created_at else ""
    }), 200


# @trekker_bp.route('/profile', methods=['PATCH'])
# @jwt_required()
# def update_profile():
#     current_user_id = get_jwt_identity()
#     trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()
#     if not trekker_profile:
#         return jsonify({"error": "Trekker profile not found"}), 404

#     data = request.get_json()
#     if 'full_name' in data:
#         trekker_profile.full_name = data['full_name']
#     if 'age' in data:
#         trekker_profile.age = int(data['age']) if data['age'] else None
#     if 'phone' in data:
#         trekker_profile.phone = data['phone']
#     if 'bio' in data:
#         trekker_profile.bio = data['bio']
#     if 'emergency_contact' in data:
#         trekker_profile.emergency_contact = data['emergency_contact']

#     db.session.commit()
#     return jsonify({"message": "Profile updated successfully"}), 200


@trekker_bp.route('/export-history', methods=['POST'])
@jwt_required()
def trigger_export():
    """Trigger an async CSV export job. Returns 202 Accepted immediately."""
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()

    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    task = export_booking_history_csv.delay(current_user_id)

    return jsonify({
        "message": "Export started. You will be notified by email when it is ready.",
        "task_id": task.id
    }), 202


@trekker_bp.route('/export-status/<string:task_id>', methods=['GET'])
@jwt_required()
def export_status(task_id):
    """Poll the status of a running CSV export job."""
    result = AsyncResult(task_id)

    if result.state == 'SUCCESS':
        return jsonify({"status": "SUCCESS", "download_url": f"/api/trekker/download-csv/{task_id}"}), 200
    elif result.state == 'FAILURE':
        return jsonify({"status": "FAILURE", "error": str(result.result)}), 200
    else:
        return jsonify({"status": result.state}), 200


@trekker_bp.route('/download-csv/<string:task_id>', methods=['GET'])
@jwt_required(locations=['headers', 'query_string'])
def download_csv(task_id):
    """Serve the generated CSV file for download."""
    from flask import current_app

    export_dir = os.path.join(current_app.root_path, 'exports')
    file_path = os.path.join(export_dir, f'{task_id}.csv')

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found. The export may still be processing."}), 404

    return send_file(
        file_path,
        mimetype='text/csv',
        as_attachment=True,
        download_name='booking_history.csv'
    )
