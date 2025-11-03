from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)  # Auto-generated unique ID
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vitals = relationship("Vitals", back_populates="patient", cascade="all, delete-orphan")
    diagnoses = relationship("Diagnosis", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")


class Vitals(Base):
    __tablename__ = "vitals"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    blood_pressure = Column(String)  # e.g., "120/80"
    temperature = Column(Float)  # Celsius
    pulse = Column(Integer)  # BPM
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Float)  # SpO2 percentage
    recorded_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    patient = relationship("Patient", back_populates="vitals")


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_name = Column(String)
    diagnosis = Column(Text, nullable=False)
    diagnosed_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="diagnoses")


class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medication_name = Column(String, nullable=False)
    dosage = Column(String)  # e.g., "500mg"
    frequency = Column(String)  # e.g., "twice daily", "every 6 hours"
    route = Column(String)  # e.g., "oral", "IV", "injection"
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    next_dose_time = Column(DateTime)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = completed
    notes = Column(Text)
    
    patient = relationship("Patient", back_populates="medications")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_type = Column(String)  # e.g., "follow-up", "checkup"
    appointment_datetime = Column(DateTime, nullable=False)
    notes = Column(Text)
    is_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="appointments")