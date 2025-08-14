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
  def create_new_patient_notification(patient_id, patient_name):
    title = "New Patient Added"
    message = f"Patient {patient_name} added"
    return NotificationService.create_notification(
      NotificationType.PATIENT,
      title,
      message,
      patient_id
    )
  
  @staticmethod
  def create_remove_patient_notification(patient_id, patient_name):
    title = "Patient Removed"
    message = f"Patient {patient_name} has been removed"
    return NotificationService.create_notification(
      NotificationType.PATIENT,
      title,
      message,
      patient_id
    )

  @staticmethod
  def create_new_staff_notification(staff_id, staff_role, staff_name):
    title = "New Staff Added"
    message = f"{staff_role} {staff_name} added"
    return NotificationService.create_notification(
      NotificationType.STAFF,
      title,
      message,
      staff_id
    )
  
  @staticmethod
  def create_remove_staff_notification(staff_id, staff_role, staff_name):
    title = "Staff Removed"
    message = f"{staff_role} {staff_name} removed from this branch"
    return NotificationService.create_notification(
      NotificationType.STAFF,
      title,
      message,
      staff_id
    )

  @staticmethod
  def create_prescription_notification(prescription_id, patient_name, medicine_name):
    title = "New Prescription Created"
    message = f"Prescription for {patient_name} is ready. Prescribed {medicine_name}"
    return NotificationService.create_notification(
      NotificationType.PRESCRIPTION,
      title,
      message,
      prescription_id
    )

  @staticmethod
  def create_diagnosis_notification(diagnosis_id, patient_name, disease_name):
    title = "New Diagnosis Recorded"
    message = f"Diagnosis completed for {patient_name}. Diagnosed with {disease_name}"
    return NotificationService.create_notification(
      NotificationType.DIAGNOSIS,
      title,
      message,
      diagnosis_id
    )

  @staticmethod
  def create_payment_notification(payment_id, amount, patient_name):
    title = "Payment Received"
    message = f"Payment of Tsh {amount:,} from {patient_name} recorded successfully"
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

  @staticmethod
  def create_new_appointment_notification(appointment_id, patient_name):
    title = "New Appointment Created"
    message = f"Appointment with patient {patient_name} has started"
    return NotificationService.create_notification(
      NotificationType.APPOINTMENT,
      title,
      message,
      appointment_id
    )
  
  @staticmethod
  def create_appointment_ended_notification(appointment_id, patient_name):
    title = "Appointment Ended"
    message = f"Appointment with patient {patient_name} has ended"
    return NotificationService.create_notification(
      NotificationType.APPOINTMENT,
      title,
      message,
      appointment_id
    )

  @staticmethod
  def create_new_medicine_notification(medicine_id, medicine_name, medicine_quantity):
    title = "New Medicine Added"
    message = f"{medicine_quantity} pieces of {medicine_name} added"
    return NotificationService.create_notification(
      NotificationType.MEDICINE,
      title,
      message,
      medicine_id
    )
  
  @staticmethod
  def create_remove_medicine_notification(medicine_id, medicine_name):
    title = "Medicine Removed"
    message = f"Medicine {medicine_name} removed from this branch"
    return NotificationService.create_notification(
      NotificationType.MEDICINE,
      title,
      message,
      medicine_id
    )
  
  @staticmethod
  def create_new_disease_notification(medicine_id, disease_name):
    title = "New Medicine Added"
    message = f"Disease {disease_name} added to all branches"
    return NotificationService.create_notification(
      NotificationType.DISEASE,
      title,
      message,
      medicine_id
    )
  
  @staticmethod
  def create_remove_disease_notification(disease_id, disease_name):
    title = "Disease Removed"
    message = f"Disease {disease_name} has been removed from all branches"
    return NotificationService.create_notification(
      NotificationType.DISEASE,
      title,
      message,
      disease_id
    )
