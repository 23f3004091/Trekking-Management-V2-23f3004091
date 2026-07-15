
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    user = User.query.get(int(current_user_id))
    return jsonify({
        "username": user.username if user else "",
        "email": user.email if user else "",
        "role": user.role.value if user else "Trek Staff",
        "full_name": staff_profile.full_name or "",
        "phone": staff_profile.phone or "",
        "contact_details": staff_profile.contact_details or "",
        "experience_years": staff_profile.experience_years,
        "specialization": staff_profile.specialization or "",
        "bio": staff_profile.bio or "",
        "status": staff_profile.status.value if staff_profile.status else "Pending",
        "blacklisted": staff_profile.blacklisted,
        "member_since": staff_profile.created_at.strftime('%Y-%m-%d') if staff_profile.created_at else ""
    }), 200


@staff_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    data = request.get_json()
    if 'full_name' in data:
        staff_profile.full_name = data['full_name']
    if 'phone' in data:
        staff_profile.phone = data['phone']
    if 'contact_details' in data:
        staff_profile.contact_details = data['contact_details']
    if 'experience_years' in data:
        staff_profile.experience_years = int(data['experience_years']) if data['experience_years'] else None
    if 'specialization' in data:
        staff_profile.specialization = data['specialization']
    if 'bio' in data:
        staff_profile.bio = data['bio']

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200



@staff_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    current_user_id = get_jwt_identity()
    # print(current_user_id)
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()
    # print(staff_profile)
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    total_treks = Trek.query.filter_by(staff_id=staff_profile.user_id).count()
    total_bookings = Booking.query.join(Trek).filter(Trek.staff_id == staff_profile.user_id).count()

    return jsonify({
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })

# use db relationships to get treks and bookings for the staff member
@staff_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_treks():
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    treks = Trek.query.filter_by(staff_id=staff_profile.user_id).all()
    trek_list = [{
        "id": trek.id, 
        "trek_name": trek.trek_name, 
        "location": trek.location, 
        "difficulty": trek.difficulty.value if trek.difficulty else "Easy", 
        "available_slots": trek.available_slots,
        "start_date": trek.start_date.strftime('%Y-%m-%d') if trek.start_date else "",
        "end_date": trek.end_date.strftime('%Y-%m-%d') if trek.end_date else "",
        "registered_count": len(trek.bookings),
        "status": trek.status.value if trek.status else "Pending"
    } for trek in treks]
    
    return jsonify({"treks": trek_list}), 200


@staff_bp.route('/bookings/<int:trek_id>', methods=['GET'])
@jwt_required()
def get_bookings(trek_id):
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    booking_list = [{
        "id": booking.id, 
        "user_id": booking.user_id, 
        "username": booking.trekker.username if booking.trekker else f"User #{booking.user_id}",
        "email": booking.trekker.email if booking.trekker else "",
        "trek_id": booking.trek_id, 
        "trek_name": trek.trek_name,
        "booking_date": booking.booking_date.strftime('%Y-%m-%d %H:%M') if booking.booking_date else "", 
        "status": booking.status.value if booking.status else "Booked"
    } for booking in trek.bookings]

    return jsonify({"bookings": booking_list}), 200

@staff_bp.route('/user/<int:trek_id>', methods=['GET'])
@jwt_required()
def get_users_for_trek(trek_id):
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    if not bookings:
        return jsonify({"users": [], "message": "No users found for this trek."}), 200
        
    user_data = [{
        "id": booking.trekker.id if booking.trekker else booking.user_id, 
        "username": booking.trekker.username if booking.trekker else f"User #{booking.user_id}", 
        "email": booking.trekker.email if booking.trekker else "",
        "booking_id": booking.id,
        "booking_status": booking.status.value if booking.status else "Booked",
        "booking_date": booking.booking_date.strftime('%Y-%m-%d %H:%M') if booking.booking_date else ""
    } for booking in bookings]

    return jsonify({"users": user_data}), 200


# This route to updated 
@staff_bp.route('/update-trek/<int:trek_id>', methods=['PATCH'])
@jwt_required()
def update_trek_status(trek_id):
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    data = request.get_json()
    new_slots = data.get('available_slots')
    new_status = data.get('status')

    if new_status and new_status not in [status.value for status in TrekStatus]:
        return jsonify({"error": "Invalid status value"}), 400

    if new_slots is not None:
        trek.available_slots = int(new_slots)
    if new_status:
        trek.status = TrekStatus(new_status)
    db.session.commit()

    return jsonify({"message": "Trek status updated successfully", "trek": {"id": trek.id, "status": trek.status.value, "available_slots": trek.available_slots}}), 200


@staff_bp.route('/update-booking-status/<int:booking_id>', methods=['PATCH'])
@jwt_required()
def update_booking_status(booking_id):
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

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