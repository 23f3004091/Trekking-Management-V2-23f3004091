from datetime import datetime, timedelta
from models import (
    User, Trekker, StaffProfile, Trek, Booking,
    UserRole, ProfileStatus, TrekStatus, BookingStatus, DifficultyLevel
)
from extensions import db

def seed_database():
    print("Clearing old database tables to prevent duplicate entries...")
    # Delete in reverse order of relationships to prevent foreign key constraint errors
    Booking.query.delete()
    Trek.query.delete()
    Trekker.query.delete()
    StaffProfile.query.delete()
    User.query.delete()
    db.session.commit()
        
    # Admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@gmail.com', role=UserRole.ADMIN)
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
    staff_profile_1 = StaffProfile(
        user_id=staff1.id, 
        full_name="John Doe",
        phone="111-222-3333",
        contact_details="111-222-3333", 
        experience_years=5,
        specialization="High Altitude Mountaineering",
        bio="Experienced guide with over 30 summits in the Himalayas.",
        status=ProfileStatus.APPROVED,
        blacklisted=False
    )
    staff_profile_2 = StaffProfile(
        user_id=staff2.id, 
        full_name="Sarah Smith",
        phone="444-555-6666",
        contact_details="444-555-6666", 
        experience_years=3,
        specialization="Wilderness First Aid",
        bio="Passionate outdoor educator and rescue specialist.",
        status=ProfileStatus.APPROVED,
        blacklisted=False
    )

    db.session.add_all([staff_profile_1, staff_profile_2])
    db.session.commit()

    print("Creating 4 Trekker Users...")
    trekker_user_1 = User(
        username="trekker_1",
        email="23f3004091@ds.study.iitm.ac.in",
        role=UserRole.TREKKER
    )
    trekker_user_1.set_password("password123")

    trekker_user_2 = User(
        username="trekker_2",
        email="23f30040912-dummy@ds.study.iitm.ac.in",
        role=UserRole.TREKKER
    )
    trekker_user_2.set_password("password123")

    trekker_user_3 = User(
        username="trekker_3",
        email="23f30040913-dummy@ds.study.iitm.ac.in",
        role=UserRole.TREKKER
    )
    trekker_user_3.set_password("password123")

    trekker_user_4 = User(
        username="trekker_4",
        email="23f30040914-dummy@ds.study.iitm.ac.in",
        role=UserRole.TREKKER
    )
    trekker_user_4.set_password("password123")

    db.session.add_all([trekker_user_1, trekker_user_2, trekker_user_3, trekker_user_4])
    db.session.commit()

    print("Creating Trekker Profiles...")
    profile_1 = Trekker(
        user_id=trekker_user_1.id, 
        full_name="Alice Explorer",
        age=22, 
        phone="555-0101",
        bio="Avid hiker looking for the next great adventure in the mountains.",
        emergency_contact="Bob (Brother): 999-888-7771",
        blacklisted=False
    )
    
    profile_2 = Trekker(
        user_id=trekker_user_2.id, 
        full_name="Bob Adventurer",
        age=24, 
        phone="555-0102",
        bio="Weekend warrior, loves moderate trails and nature photography.",
        emergency_contact="Alice (Sister): 999-888-7772",
        blacklisted=False
    )

    profile_3 = Trekker(
        user_id=trekker_user_3.id, 
        full_name="Charlie Climber",
        age=26, 
        phone="555-0103",
        bio="Experienced trekker aiming to conquer high altitude peaks this year.",
        emergency_contact="Diana (Wife): 999-888-7773",
        blacklisted=False
    )

    profile_4 = Trekker(
        user_id=trekker_user_4.id, 
        full_name="Diana Hiker",
        age=28, 
        phone="555-0104",
        bio="Nature enthusiast. Prefer long, scenic routes over steep climbs.",
        emergency_contact="Charlie (Husband): 999-888-7774",
        blacklisted=False
    )

    db.session.add_all([profile_1, profile_2, profile_3, profile_4])
    db.session.commit()

    print("Creating 5 Treks...")
    now = datetime.utcnow()
    trek_1 = Trek(
        trek_name="Everest Base Camp",
        location="Nepal",
        difficulty=DifficultyLevel.HARD,
        available_slots=20,
        status=TrekStatus.OPEN,
        start_date=now + timedelta(days=30),
        end_date=now + timedelta(days=45),
        staff_id=staff1.id
    )
    trek_2 = Trek(
        trek_name="Annapurna Circuit",
        location="Nepal",
        difficulty=DifficultyLevel.HARD,
        available_slots=15,
        status=TrekStatus.OPEN,
        start_date=now + timedelta(days=15),
        end_date=now + timedelta(days=30),
        staff_id=staff2.id
    )
    trek_3 = Trek(
        trek_name="Mount Kilimanjaro",
        location="Tanzania",
        difficulty=DifficultyLevel.MODERATE,
        available_slots=10,
        status=TrekStatus.APPROVED,
        start_date=now + timedelta(days=60),
        end_date=now + timedelta(days=68),
        staff_id=staff1.id
    )
    trek_4 = Trek(
        trek_name="Inca Trail",
        location="Peru",
        difficulty=DifficultyLevel.MODERATE,
        available_slots=25,
        status=TrekStatus.COMPLETED,
        start_date=now - timedelta(days=20),
        end_date=now - timedelta(days=15),
        staff_id=staff2.id
    )
    trek_5 = Trek(
        trek_name="Blue Mountains Trek",
        location="Australia",
        difficulty=DifficultyLevel.EASY,
        available_slots=12,
        status=TrekStatus.PENDING,
        start_date=now + timedelta(days=90),
        end_date=now + timedelta(days=95),
        staff_id=staff1.id
    )
    
    db.session.add_all([trek_1, trek_2, trek_3, trek_4, trek_5])
    db.session.commit()

    print("Creating 10 Bookings...")

    bookings = [
        # Trekker 1 books 3 treks
        Booking(user_id=trekker_user_1.id, trek_id=trek_1.id, status=BookingStatus.BOOKED),
        Booking(user_id=trekker_user_1.id, trek_id=trek_2.id, status=BookingStatus.BOOKED),
        Booking(user_id=trekker_user_1.id, trek_id=trek_3.id, status=BookingStatus.CANCELLED),

        # Trekker 2 books 3 treks
        Booking(user_id=trekker_user_2.id, trek_id=trek_1.id, status=BookingStatus.BOOKED),
        Booking(user_id=trekker_user_2.id, trek_id=trek_4.id, status=BookingStatus.COMPLETED),
        Booking(user_id=trekker_user_2.id, trek_id=trek_5.id, status=BookingStatus.BOOKED),

        # Trekker 3 books 2 treks
        Booking(user_id=trekker_user_3.id, trek_id=trek_2.id, status=BookingStatus.BOOKED),
        Booking(user_id=trekker_user_3.id, trek_id=trek_4.id, status=BookingStatus.COMPLETED),

        # Trekker 4 books 2 treks
        Booking(user_id=trekker_user_4.id, trek_id=trek_3.id, status=BookingStatus.BOOKED),
        Booking(user_id=trekker_user_4.id, trek_id=trek_5.id, status=BookingStatus.BOOKED),
    ]

    db.session.add_all(bookings)
    db.session.commit()

    print("Database successfully seeded with 2 staff, 4 trekkers, 5 treks, and 10 bookings!")

if __name__ == '__main__':
    seed_database()