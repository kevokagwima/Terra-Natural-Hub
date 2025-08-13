from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from Utils.notification_service import NotificationService
from Models.notification import Notification

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
  limit = request.args.get('limit', default=10, type=int)
  notifications = Notification.query.filter_by(clinic_id=session["clinic_id"]).order_by(Notification.created_at.desc()).limit(limit).all()
  
  return jsonify([n.to_dict() for n in notifications])

@notifications.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
  if NotificationService.mark_as_read(notification_id):
    return jsonify({'success': True})
  return jsonify({'success': False}), 404

@notifications.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
  NotificationService.mark_all_as_read(session["clinic_id"])
  return jsonify({'success': True})
