from sqlalchemy.orm import Session
from app.models.patient import Patient, Vitals, Diagnosis, Medication, Appointment
from app.models.schemas import *
from datetime import datetime, timedelta
import random
import string

class PatientService:
    
    @staticmethod
    def generate_patient_id() -> str:
        """Generate unique patient ID like PT001, PT002, etc."""
        return f"PT{random.randint(1000, 9999)}"
    
    @staticmethod
    def create_patient(db: Session, data: dict) -> Patient:
        """Register a new patient"""
        patient_id = PatientService.generate_patient_id()
        
        # Ensure unique ID
        while db.query(Patient).filter(Patient.patient_id == patient_id).first():
            patient_id = PatientService.generate_patient_id()
        
        patient = Patient(
            patient_id=patient_id,
            name=data.get('name'),
            age=data.get('age'),
            gender=data.get('gender'),
            phone=data.get('phone')
        )
        
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def get_patient_by_id(db: Session, patient_id: str) -> Patient:
        """Get patient by patient_id"""
        return db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    @staticmethod
    def record_vitals(db: Session, data: dict) -> Vitals:
        """Record patient vitals"""
        patient = PatientService.get_patient_by_id(db, data.get('patient_id'))
        if not patient:
            return None
        
        vitals = Vitals(
            patient_id=patient.id,
            blood_pressure=data.get('blood_pressure'),
            temperature=data.get('temperature'),
            pulse=data.get('pulse'),
            respiratory_rate=data.get('respiratory_rate'),
            oxygen_saturation=data.get('oxygen_saturation'),
            notes=data.get('notes')
        )
        
        db.add(vitals)
        db.commit()
        db.refresh(vitals)
        return vitals
    
    @staticmethod
    def add_diagnosis(db: Session, data: dict) -> Diagnosis:
        """Add diagnosis for patient"""
        patient = PatientService.get_patient_by_id(db, data.get('patient_id'))
        if not patient:
            return None
        
        diagnosis = Diagnosis(
            patient_id=patient.id,
            doctor_name=data.get('doctor_name'),
            diagnosis=data.get('diagnosis')
        )
        
        db.add(diagnosis)
        db.commit()
        db.refresh(diagnosis)
        return diagnosis
    
    @staticmethod
    def prescribe_medication(db: Session, data: dict) -> Medication:
        """Prescribe medication for patient"""
        patient = PatientService.get_patient_by_id(db, data.get('patient_id'))
        if not patient:
            return None
        
        # Calculate next dose time based on frequency
        next_dose = PatientService.calculate_next_dose(data.get('frequency'))
        
        medication = Medication(
            patient_id=patient.id,
            medication_name=data.get('medication_name'),
            dosage=data.get('dosage'),
            frequency=data.get('frequency'),
            route=data.get('route', 'oral'),
            next_dose_time=next_dose,
            notes=data.get('notes')
        )
        
        db.add(medication)
        db.commit()
        db.refresh(medication)
        return medication
    
    @staticmethod
    def calculate_next_dose(frequency: str) -> datetime:
        """Calculate next dose time based on frequency"""
        now = datetime.utcnow()
        frequency_lower = frequency.lower()
        
        if 'once' in frequency_lower or 'daily' in frequency_lower:
            return now + timedelta(hours=24)
        elif 'twice' in frequency_lower:
            return now + timedelta(hours=12)
        elif 'three times' in frequency_lower or 'thrice' in frequency_lower:
            return now + timedelta(hours=8)
        elif 'four times' in frequency_lower:
            return now + timedelta(hours=6)
        elif 'every 6 hours' in frequency_lower:
            return now + timedelta(hours=6)
        elif 'every 8 hours' in frequency_lower:
            return now + timedelta(hours=8)
        else:
            return now + timedelta(hours=8)  # Default
    
    @staticmethod
    def schedule_appointment(db: Session, data: dict) -> Appointment:
        """Schedule appointment for patient"""
        patient = PatientService.get_patient_by_id(db, data.get('patient_id'))
        if not patient:
            return None
        
        appointment = Appointment(
            patient_id=patient.id,
            appointment_type=data.get('appointment_type', 'checkup'),
            appointment_datetime=data.get('appointment_datetime'),
            notes=data.get('notes')
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment
    
    @staticmethod
    def get_patient_full_record(db: Session, patient_id: str) -> dict:
        """Get complete patient record"""
        patient = PatientService.get_patient_by_id(db, patient_id)
        if not patient:
            return None
        
        vitals = db.query(Vitals).filter(Vitals.patient_id == patient.id).order_by(Vitals.recorded_at.desc()).all()
        diagnoses = db.query(Diagnosis).filter(Diagnosis.patient_id == patient.id).order_by(Diagnosis.diagnosed_at.desc()).all()
        medications = db.query(Medication).filter(Medication.patient_id == patient.id).all()
        appointments = db.query(Appointment).filter(Appointment.patient_id == patient.id).order_by(Appointment.appointment_datetime).all()
        
        return {
            'patient': {
                'patient_id': patient.patient_id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone
            },
            'vitals': [
                {
                    'blood_pressure': v.blood_pressure,
                    'temperature': v.temperature,
                    'pulse': v.pulse,
                    'respiratory_rate': v.respiratory_rate,
                    'oxygen_saturation': v.oxygen_saturation,
                    'recorded_at': v.recorded_at
                } for v in vitals
            ],
            'diagnoses': [
                {
                    'doctor_name': d.doctor_name,
                    'diagnosis': d.diagnosis,
                    'diagnosed_at': d.diagnosed_at
                } for d in diagnoses
            ],
            'medications': [
                {
                    'medication_name': m.medication_name,
                    'dosage': m.dosage,
                    'frequency': m.frequency,
                    'route': m.route,
                    'next_dose_time': m.next_dose_time,
                    'is_active': m.is_active
                } for m in medications
            ],
            'appointments': [
                {
                    'appointment_type': a.appointment_type,
                    'appointment_datetime': a.appointment_datetime,
                    'is_completed': a.is_completed
                } for a in appointments
            ]
        }