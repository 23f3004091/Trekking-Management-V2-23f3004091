from datetime import datetime, timedelta
from models import (
    User, Trekker, StaffProfile, Trek, Booking,
    UserRole, ProfileStatus, TrekStatus, BookingStatus, DifficultyLevel
)
from extensions import db

def seed_database():
    print("Clearing old database tables...")
    db.drop_all()
    db.create_all()
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@gmail.com',role=UserRole.ADMIN)
        admin.set_password('admin') 
        db.session.add(admin)
        db.session.commit()

    print("Creating Staff Users...")
    # 2 Staff Users
    staff1 = User(username="staff_john", email="john.staff@trek.com", role=UserRole.TREK_STAFF)
    staff1.set_password("password123")
    
    staff2 = User(username="staff_sarah", email="sarah.staff@trek.com", role=UserRole.TREK_STAFF)
    staff2.set_password("password123")

    db.session.add_all([staff1, staff2])
    db.session.commit()  # Commit to generate IDs for foreign keys

    print("Creating Staff Profiles...")
    staff_profile_1 = StaffProfile(user_id=staff1.id, contact_details="111-222-3333", status=ProfileStatus.APPROVED)
    staff_profile_2 = StaffProfile(user_id=staff2.id, contact_details="444-555-6666", status=ProfileStatus.APPROVED)

    db.session.add_all([staff_profile_1, staff_profile_2])
    db.session.commit()

    print("Creating 4 Trekkers...")
    trekkers_users = []
    for i in range(1, 5):
        t_user = User(
            username=f"trekker_{i}", 
            email=f"trekker{i}@mail.com", 
            role=UserRole.TREKKER
        )
        t_user.set_password("password123")
        trekkers_users.append(t_user)

    db.session.add_all(trekkers_users)
    db.session.commit()

    print("Creating Trekker Profiles...")
    trekker_profiles = []
    # Assign ages 22, 24, 26, 28 to the 4 trekkers
    for idx, user in enumerate(trekkers_users):
        profile = Trekker(user_id=user.id, age=22 + (idx * 2), blacklisted=False)
        trekker_profiles.append(profile)

    db.session.add_all(trekker_profiles)
    db.session.commit()

    print("Creating 5 Treks...")
    now = datetime.utcnow()
    treks = [
        Trek(
            trek_name="Everest Base Camp",
            location="Nepal",
            difficulty=DifficultyLevel.HARD,
            available_slots=20,
            status=TrekStatus.OPEN,
            start_date=now + timedelta(days=30),
            end_date=now + timedelta(days=45),
            staff_id=staff1.id
        ),
        Trek(
            trek_name="Annapurna Circuit",
            location="Nepal",
            difficulty=DifficultyLevel.HARD,
            available_slots=15,
            status=TrekStatus.OPEN,
            start_date=now + timedelta(days=15),
            end_date=now + timedelta(days=30),
            staff_id=staff2.id
        ),
        Trek(
            trek_name="Mount Kilimanjaro",
            location="Tanzania",
            difficulty=DifficultyLevel.MODERATE,
            available_slots=10,
            status=TrekStatus.APPROVED,
            start_date=now + timedelta(days=60),
            end_date=now + timedelta(days=68),
            staff_id=staff1.id
        ),
        Trek(
            trek_name="Inca Trail",
            location="Peru",
            difficulty=DifficultyLevel.MODERATE,
            available_slots=25,
            status=TrekStatus.COMPLETED,
            start_date=now - timedelta(days=20),
            end_date=now - timedelta(days=15),
            staff_id=staff2.id
        ),
        Trek(
            trek_name="Blue Mountains Trek",
            location="Australia",
            difficulty=DifficultyLevel.EASY,
            available_slots=12,
            status=TrekStatus.PENDING,
            start_date=now + timedelta(days=90),
            end_date=now + timedelta(days=95),
            staff_id=staff1.id
        )
    ]
    db.session.add_all(treks)
    db.session.commit()

    print("Creating 10 Bookings...")
    # Get lists of IDs to easily map them
    t_ids = [user.id for user in trekkers_users]
    trek_ids = [trek.id for trek in treks]

    bookings = [
        # Trekker 1 books 3 treks
        Booking(user_id=t_ids[0], trek_id=trek_ids[0], status=BookingStatus.BOOKED),
        Booking(user_id=t_ids[0], trek_id=trek_ids[1], status=BookingStatus.BOOKED),
        Booking(user_id=t_ids[0], trek_id=trek_ids[2], status=BookingStatus.CANCELLED),

        # Trekker 2 books 3 treks
        Booking(user_id=t_ids[1], trek_id=trek_ids[0], status=BookingStatus.BOOKED),
        Booking(user_id=t_ids[1], trek_id=trek_ids[3], status=BookingStatus.COMPLETED),
        Booking(user_id=t_ids[1], trek_id=trek_ids[4], status=BookingStatus.BOOKED),

        # Trekker 3 books 2 treks
        Booking(user_id=t_ids[2], trek_id=trek_ids[1], status=BookingStatus.BOOKED),
        Booking(user_id=t_ids[2], trek_id=trek_ids[3], status=BookingStatus.COMPLETED),

        # Trekker 4 books 2 treks
        Booking(user_id=t_ids[3], trek_id=trek_ids[2], status=BookingStatus.BOOKED),
        Booking(user_id=t_ids[3], trek_id=trek_ids[4], status=BookingStatus.BOOKED),
    ]

    db.session.add_all(bookings)
    db.session.commit()

    print("Database successfully seeded with 2 staff, 4 trekkers, 5 treks, and 10 bookings!")

if __name__ == '__main__':
    seed_database()