from flask import session
from Models.base_model import db
from Models.notification import Notification, NotificationType

class NotificationService:
  @staticmethod
  def create_notification(notification_type, title, message, related_id=None):
    notification = Notification(
      clinic_id=session["clinic_id"],
      notification_type=notification_type,
      title=title,
      message=message,
      related_id=related_id
    )
    db.session.add(notification)
    db.session.commit()
    return notification

  @staticmethod
  def create_prescription_notification(prescription_id, patient_name):
    title = "New Prescription Created"
    message = f"Prescription for {patient_name} is ready"
    return NotificationService.create_notification(
      NotificationType.PRESCRIPTION,
      title,
      message,
      prescription_id
    )

  @staticmethod
  def create_diagnosis_notification(diagnosis_id, patient_name):
    title = "New Diagnosis Recorded"
    message = f"Diagnosis completed for {patient_name}"
    return NotificationService.create_notification(
      NotificationType.DIAGNOSIS,
      title,
      message,
      diagnosis_id
    )

  @staticmethod
  def create_payment_notification(payment_id, amount, patient_name):
    title = "Payment Received"
    message = f"Payment of Tsh {amount:,} from {patient_name}"
    return NotificationService.create_notification(
      NotificationType.PAYMENT,
      title,
      message,
      payment_id
    )

  @staticmethod
  def create_low_inventory_notification(medicine_name, current_quantity):
    title = "Low Medicine Stock"
    message = f"{medicine_name} is running low ({current_quantity} remaining)"
    return NotificationService.create_notification(
      NotificationType.INVENTORY,
      title,
      message
    )

  @staticmethod
  def mark_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
      notification.is_read = True
      db.session.commit()
      return True
    return False

  @staticmethod
  def mark_all_as_read(clinic_id):
    Notification.query.filter_by(clinic_id=clinic_id, is_read=False).update(
      {'is_read': True},
      synchronize_session=False
    )
    db.session.commit()
