
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
                "status": trek.status.value if trek.status else "Open"
            })
    
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
    
    trek.available_slots -= 1
    booking = Booking(user_id=current_user_id, trek_id=trek_id)
    
    db.session.add(booking)
    db.session.commit()

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

