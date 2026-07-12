
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    # print(treks)
    trek_list = []
    for trek in treks:
        # print(trek.status)
        if trek.status in [TrekStatus.APPROVED, TrekStatus.OPEN]:
            trek_list.append({"id": trek.id, "trek_name": trek.trek_name, "location": trek.location, "difficulty": trek.difficulty.value, "status": trek.status.value})
    
    return jsonify({"treks": trek_list}), 200
    

@trekker_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    current_user_id = get_jwt_identity()
    trekker_profile = Trekker.query.filter_by(user_id=current_user_id).first()

    if not trekker_profile:
        return jsonify({"error": "Trekker profile not found"}), 404

    history = Booking.query.filter_by(user_id=trekker_profile.user_id).all()
    history_list = [{"id": history.id, "user_id": history.user_id, "trek_id": history.trek_id, "booking_date": history.booking_date.isoformat(), "status": history.status.value} for history in history]

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
    
    trek.available_slots -= 1
    booking = Booking(user_id=current_user_id, trek_id=trek_id)
    
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking created successfully", "booking": {"id": booking.id, "user_id": booking.user_id, "trek_id": booking.trek_id, "booking_date": booking.booking_date.isoformat(), "status": booking.status.value}}), 201


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

