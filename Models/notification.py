from Models.base_model import db, BaseModel, get_local_time
from enum import Enum

class NotificationType(Enum):
  PRESCRIPTION = 'prescription'
  DIAGNOSIS = 'diagnosis'
  PAYMENT = 'payment'
  INVENTORY = 'inventory'
  APPOINTMENT = 'appointment'
  PATIENT = 'patient'
  STAFF = 'staff'
  MEDICINE = 'medicine'
  DISEASE = 'disease'
  # LABTEST = 'labtest'

class Notification(BaseModel, db.Model):
  clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
  notification_type = db.Column(db.Enum(NotificationType), nullable=False)
  title = db.Column(db.String(100), nullable=False)
  message = db.Column(db.String(255), nullable=False)
  is_read = db.Column(db.Boolean, default=False)
  related_id = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, default=get_local_time())

  def to_dict(self):
    return {
      'id': self.id,
      'type': self.notification_type.value,
      'title': self.title,
      'message': self.message,
      'is_read': self.is_read,
      'created_at': self.created_at.isoformat(),
      'related_id': self.related_id
    }
