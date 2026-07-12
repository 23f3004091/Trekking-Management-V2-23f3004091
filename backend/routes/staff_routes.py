
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def staff_dashboard():
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
    print(treks)
    trek_list = [{"id": trek.id, "trek_name": trek.trek_name, "location": trek.location, "difficulty": trek.difficulty.value, "status": trek.status.value} for trek in treks]
    
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

    booking_list = [{"id": booking.id, "user_id": booking.user_id, "trek_id": booking.trek_id, "booking_date": booking.booking_date.isoformat(), "status": booking.status.value} for booking in trek.bookings]

    return jsonify({"bookings": booking_list}), 200

@staff_bp.route('/user/<int:trek_id>', methods=['GET'])
@jwt_required()
def get_users_for_trek(trek_id):
    current_user_id = get_jwt_identity()
    staff_profile = StaffProfile.query.filter_by(user_id=current_user_id).first()

    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    users = User.query.join(Booking).filter(Booking.trek_id == trek_id).all()
    
    if not users:
        return jsonify({"message": "No users found for this trek."}), 404
        
    user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

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

    if new_status not in [status.value for status in TrekStatus]:
        return jsonify({"error": "Invalid status value"}), 400

    trek.available_slots = new_slots if new_slots is not None else trek.available_slots
    trek.status = TrekStatus(new_status)
    db.session.commit()

    return jsonify({"message": "Trek status updated successfully", "trek": {"id": trek.id, "status": trek.status.value}}), 200


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