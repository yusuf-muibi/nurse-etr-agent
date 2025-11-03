from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.models.patient import Medication, Appointment
from app.database import SessionLocal
from datetime import datetime, timedelta
import httpx
import os

class ReminderService:
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def check_medication_reminders(self):
        """Check for due medications and send reminders"""
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            due_medications = db.query(Medication).filter(
                Medication.is_active == 1,
                Medication.next_dose_time <= now + timedelta(minutes=15)
            ).all()
            
            for med in due_medications:
                patient = med.patient
                message = f"🔔 **Medication Reminder**\n\n"
                message += f"Patient: {patient.name} ({patient.patient_id})\n"
                message += f"Medication: {med.medication_name} {med.dosage}\n"
                message += f"Route: {med.route}\n"
                message += f"Due: {med.next_dose_time.strftime('%I:%M %p')}"
                
                self.send_telex_message(message)
                
                # Update next dose time
                from app.services.patient_service import PatientService
                med.next_dose_time = PatientService.calculate_next_dose(med.frequency)
                db.commit()
        
        finally:
            db.close()
    
    def check_appointment_reminders(self):
        """Check for upcoming appointments"""
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            upcoming = db.query(Appointment).filter(
                Appointment.is_completed == 0,
                Appointment.appointment_datetime >= now,
                Appointment.appointment_datetime <= now + timedelta(hours=24)
            ).all()
            
            for apt in upcoming:
                patient = apt.patient
                message = f"📅 **Appointment Reminder**\n\n"
                message += f"Patient: {patient.name} ({patient.patient_id})\n"
                message += f"Type: {apt.appointment_type}\n"
                message += f"Time: {apt.appointment_datetime.strftime('%B %d, %Y at %I:%M %p')}\n"
                if apt.notes:
                    message += f"Notes: {apt.notes}"
                
                self.send_telex_message(message)
        
        finally:
            db.close()
    
    def send_telex_message(self, message: str):
        """Send message to Telex"""
        try:
            # This will be implemented when we integrate Telex
            # For now, just print
            print(f"[REMINDER] {message}")
            # TODO: Implement actual Telex API call
        except Exception as e:
            print(f"Error sending reminder: {e}")
    
    def start(self):
        """Start scheduled tasks"""
        # Check medication reminders every 15 minutes
        self.scheduler.add_job(
            self.check_medication_reminders,
            'interval',
            minutes=15,
            id='medication_reminders'
        )
        
        # Check appointment reminders every hour
        self.scheduler.add_job(
            self.check_appointment_reminders,
            'interval',
            hours=1,
            id='appointment_reminders'
        )
        
        print("✅ Reminder service started")