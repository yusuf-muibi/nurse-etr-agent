from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Patient Schemas
class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

class PatientResponse(BaseModel):
    id: int
    patient_id: str
    name: str
    age: Optional[int]
    gender: Optional[str]
    phone: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Vitals Schemas
class VitalsCreate(BaseModel):
    patient_id: str
    blood_pressure: Optional[str] = None
    temperature: Optional[float] = None
    pulse: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    notes: Optional[str] = None

class VitalsResponse(BaseModel):
    id: int
    blood_pressure: Optional[str]
    temperature: Optional[float]
    pulse: Optional[int]
    respiratory_rate: Optional[int]
    oxygen_saturation: Optional[float]
    recorded_at: datetime
    notes: Optional[str]
    
    class Config:
        from_attributes = True

# Diagnosis Schemas
class DiagnosisCreate(BaseModel):
    patient_id: str
    doctor_name: str
    diagnosis: str

class DiagnosisResponse(BaseModel):
    id: int
    doctor_name: str
    diagnosis: str
    diagnosed_at: datetime
    
    class Config:
        from_attributes = True

# Medication Schemas
class MedicationCreate(BaseModel):
    patient_id: str
    medication_name: str
    dosage: str
    frequency: str
    route: str = "oral"
    notes: Optional[str] = None

class MedicationResponse(BaseModel):
    id: int
    medication_name: str
    dosage: str
    frequency: str
    route: str
    next_dose_time: Optional[datetime]
    is_active: int
    
    class Config:
        from_attributes = True

# Appointment Schemas
class AppointmentCreate(BaseModel):
    patient_id: str
    appointment_type: str
    appointment_datetime: datetime
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: int
    appointment_type: str
    appointment_datetime: datetime
    notes: Optional[str]
    is_completed: int
    
    class Config:
        from_attributes = True

# Telex Webhook Schema
class TelexMessage(BaseModel):
    message: str
    user_id: str
    channel_id: str
    timestamp: datetime