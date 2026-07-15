
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus, User, ProfileStatus, DifficultyLevel
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
admin_bp = Blueprint('admin', __name__)

def fmt_dt(dt):
    """Return a plain YYYY-MM-DD date string, or None."""
    if not dt:
        return None
    return dt.strftime('%Y-%m-%d')

@admin_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    total_treks = Trek.query.count()
    total_trekkers = Trekker.query.count()
    total_staff = StaffProfile.query.count()
    total_bookings = Booking.query.count()
    return jsonify({
        "total_trekkers": total_trekkers,
        "total_staff": total_staff,
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })

@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
def get_users():
    users = StaffProfile.query.all()
    user_list = [{
        "id": user.id,
        "user_id": user.user_id,
        "username": user.user.username,
        "email": user.user.email,
        "full_name": user.full_name or "",
        "phone": user.phone or "",
        "contact_details": user.contact_details,
        "specialization": user.specialization or "",
        "experience_years": user.experience_years,
        "status": user.status.value,
        "blacklisted": user.blacklisted
    } for user in users]
    return jsonify({"users": user_list})

@admin_bp.route('/trekkers', methods=['GET'])
@jwt_required()
def get_trekkers():
    trekkers = Trekker.query.all()
    trekker_list = [{
        "id": trekker.id,
        "user_id": trekker.user_id,
        "username": trekker.user.username if trekker.user else f"User #{trekker.user_id}",
        "email": trekker.user.email if trekker.user else "",
        "full_name": trekker.full_name or "",
        "phone": trekker.phone or "",
        "age": trekker.age,
        "emergency_contact": trekker.emergency_contact or "",
        "blacklisted": trekker.blacklisted
    } for trekker in trekkers]
    return jsonify({"trekkers": trekker_list})

@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_treks():
    treks = Trek.query.all()
    trek_list = [{
        "id": trek.id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else "Easy",
        "available_slots": trek.available_slots,
        "start_date": fmt_dt(trek.start_date),
        "end_date": fmt_dt(trek.end_date),
        "staff_id": trek.staff_id,
        "staff_name": trek.assigned_staff.username if trek.assigned_staff else "Unassigned",
        "status": trek.status.value if trek.status else "Pending"
    } for trek in treks]
    return jsonify({"treks": trek_list})

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    bookings = Booking.query.all()
    booking_list = [{
        "id": booking.id,
        "user_id": booking.user_id,
        "username": booking.trekker.username if booking.trekker else f"User #{booking.user_id}",
        "email": booking.trekker.email if booking.trekker else "",
        "trek_id": booking.trek_id,
        "trek_name": booking.treks.trek_name if booking.treks else "Unknown Trek",
        "location": booking.treks.location if booking.treks else "",
        "booking_date": fmt_dt(booking.booking_date),
        "status": booking.status.value if booking.status else "Booked"
    } for booking in bookings]
    return jsonify({"bookings": booking_list})

@admin_bp.route('/manage-trek/<int:trek_id>', methods=['PATCH'])
@jwt_required()
def manage_trek(trek_id):
    data = request.get_json()
    action = data.get('action')
    trek = Trek.query.get(trek_id)
    
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    if action == 'approve':
        if trek.status not in [TrekStatus.PENDING]:
            return jsonify({"error": "Trek can only be approved when it is Pending"}), 400
        trek.status = TrekStatus.APPROVED
    elif action == 'cancel':
        if trek.status == TrekStatus.COMPLETED:
            return jsonify({"error": "Cannot cancel a trek that is already Completed"}), 400
        trek.status = TrekStatus.CANCELLED
    else:
        return jsonify({"error": "Invalid action. Admin can only 'approve' or 'cancel' a trek."}), 400
    
    db.session.commit()
    return jsonify({"message": f"Trek {action}d successfully", "trek": {"id": trek.id, "status": trek.status.value}})


@admin_bp.route('/create-trek', methods=['POST'])
@jwt_required()
def create_trek():
    data = request.get_json()
    trek_name = data.get('trek_name')
    location = data.get('location')
    diff_str = data.get('difficulty', 'Easy')
    available_slots = int(data.get('available_slots', 10))
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    staff_name = data.get('staff_name')
    
    staff = User.query.filter_by(username=staff_name).first()
    if not staff:
        return jsonify({"error": "Staff member not found"}), 404

    from datetime import datetime
    try:
        start_date = datetime.strptime(start_date_str[:10], '%Y-%m-%d') if start_date_str else datetime.utcnow()
        end_date = datetime.strptime(end_date_str[:10], '%Y-%m-%d') if end_date_str else datetime.utcnow()
    except Exception:
        start_date = datetime.utcnow()
        end_date = datetime.utcnow()

    diff_enum = DifficultyLevel(diff_str) if diff_str in [d.value for d in DifficultyLevel] else DifficultyLevel.EASY

    new_trek = Trek(trek_name=trek_name, location=location, difficulty=diff_enum, available_slots=available_slots, start_date=start_date, end_date=end_date, staff_id=staff.id, status=TrekStatus.PENDING)

    db.session.add(new_trek)
    db.session.commit()
    return jsonify({"message": "Trek created successfully", "trek": {
        "id": new_trek.id,
        "trek_name": new_trek.trek_name,
        "location": new_trek.location,
        "difficulty": new_trek.difficulty.value if new_trek.difficulty else "Easy",
        "available_slots": new_trek.available_slots,
        "start_date": fmt_dt(new_trek.start_date),
        "end_date": fmt_dt(new_trek.end_date),
        "staff_id": new_trek.staff_id,
        "staff_name": staff.username,
        "status": new_trek.status.value if new_trek.status else "Pending"
    }}), 201

@admin_bp.route('/update-trek/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    data = request.get_json()
    trek.trek_name = data.get('trek_name', trek.trek_name)
    trek.location = data.get('location', trek.location)
    
    diff_str = data.get('difficulty')
    if diff_str in [d.value for d in DifficultyLevel]:
        trek.difficulty = DifficultyLevel(diff_str)
        
    if data.get('available_slots') is not None:
        trek.available_slots = int(data.get('available_slots'))
        
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    from datetime import datetime
    if start_date_str:
        try:
            trek.start_date = datetime.strptime(start_date_str[:10], '%Y-%m-%d')
        except Exception:
            pass
    if end_date_str:
        try:
            trek.end_date = datetime.strptime(end_date_str[:10], '%Y-%m-%d')
        except Exception:
            pass
            
    staff_name = data.get('staff_name')
    if staff_name:
        staff = User.query.filter_by(username=staff_name).first()
        if staff:
            trek.staff_id = staff.id

    db.session.commit()
    return jsonify({"message": "Trek updated successfully", "trek": {
        "id": trek.id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else "Easy",
        "available_slots": trek.available_slots,
        "start_date": fmt_dt(trek.start_date),
        "end_date": fmt_dt(trek.end_date),
        "staff_id": trek.staff_id,
        "staff_name": trek.assigned_staff.username if trek.assigned_staff else "Unassigned",
        "status": trek.status.value if trek.status else "Pending"
    }})

@admin_bp.route('/delete-trek/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"})


@admin_bp.route('/manage-booking/<int:booking_id>', methods=['PATCH'])
@jwt_required()
def manage_booking(booking_id):
    data = request.get_json()
    action = data.get('action')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    
    if action == 'cancel':
        booking.status = BookingStatus.CANCELLED
    elif action == 'complete':
        booking.status = BookingStatus.COMPLETED
    else:
        return jsonify({"error": "Invalid action"}), 400
    db.session.commit()
    return jsonify({"message": f"Booking {action}d successfully", "booking": {"id": booking.id, "status": booking.status.value}})

@admin_bp.route('/approve-staff', methods=['PATCH'])
@jwt_required()
def approve_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')
    staff_profile = StaffProfile.query.get(staff_id)
    
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404
    
    staff_profile.status = ProfileStatus.APPROVED
    db.session.commit()
    return jsonify({"message": "Staff profile approved successfully", "staff_profile": {"id": staff_profile.id, "status": staff_profile.status.value}})

@admin_bp.route('/blacklist-staff', methods=['PATCH'])
@jwt_required()
def reject_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')
    staff_profile = StaffProfile.query.get(staff_id)
    
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    if staff_profile.blacklisted:
        staff_profile.blacklisted = False
    else:
        staff_profile.blacklisted = True
    db.session.commit()
    return jsonify({"message": "Staff profile blacklisted successfully", "staff_profile": {"id": staff_profile.id, "blacklisted": staff_profile.blacklisted}})

@admin_bp.route('/blacklist-trekker', methods=['PATCH'])
@jwt_required()
def blacklist_trekker():
    data = request.get_json()
    trekker_id = data.get('trekker_id')
    trekker = Trekker.query.get(trekker_id)
    
    if not trekker:
        return jsonify({"error": "Trekker not found"}), 404

    trekker.blacklisted = not trekker.blacklisted
    db.session.commit()
    return jsonify({"message": "Trekker blacklisted successfully", "trekker": {"id": trekker.id, "blacklisted": trekker.blacklisted}})