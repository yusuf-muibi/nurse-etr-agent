from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_service import AIAgent
from app.services.patient_service import PatientService
from app.models.schemas import TelexMessage
from datetime import datetime, timedelta
import dateparser
from pydantic import BaseModel

router = APIRouter(prefix="/agent", tags=["Agent"])

class MessageRequest(BaseModel):
    message: str
    user_id: str

@router.post("/message")
async def process_message(data: MessageRequest, db: Session = Depends(get_db)):
    """
    Process incoming messages from Telex
    """
    try:
        message = data.message.strip()
        user_id = data.user_id
        
        # Log incoming request
        print(f"📨 Received message from {user_id}: {message}")
        
        if not message:
            return {
                "response": "Please provide a message.",
                "text": "Please provide a message.",
                "message": "Please provide a message.",
                "content": "Please provide a message."
            }
        
        # Parse intent using AI
        parsed = AIAgent.parse_intent(message)
        intent = parsed.get('intent')
        data_dict = parsed.get('data', {})
        
        print(f"🎯 Detected intent: {intent}")
        print(f"📋 Extracted data: {data_dict}")
        
        response_text = ""
        success = False
        response_data = {}
        
        # Handle different intents
        if intent == "register_patient":
            patient = PatientService.create_patient(db, data_dict)
            if patient:
                success = True
                response_data = {
                    'patient_id': patient.patient_id,
                    'name': patient.name
                }
        
        elif intent == "record_vitals":
            vitals = PatientService.record_vitals(db, data_dict)
            if vitals:
                success = True
                response_data = {
                    'patient_id': data_dict.get('patient_id'),
                    'vitals': {
                        'blood_pressure': vitals.blood_pressure,
                        'temperature': vitals.temperature,
                        'pulse': vitals.pulse,
                        'respiratory_rate': vitals.respiratory_rate,
                        'oxygen_saturation': vitals.oxygen_saturation
                    }
                }
        
        elif intent == "add_diagnosis":
            diagnosis = PatientService.add_diagnosis(db, data_dict)
            if diagnosis:
                success = True
                response_data = {
                    'patient_id': data_dict.get('patient_id'),
                    'doctor_name': diagnosis.doctor_name,
                    'diagnosis': diagnosis.diagnosis
                }
        
        elif intent == "prescribe_medication":
            medication = PatientService.prescribe_medication(db, data_dict)
            if medication:
                success = True
                response_data = {
                    'patient_id': data_dict.get('patient_id'),
                    'medication_name': medication.medication_name,
                    'dosage': medication.dosage,
                    'frequency': medication.frequency
                }
        
        elif intent == "schedule_appointment":
            # Parse the time string into datetime
            time_str = data_dict.get('time', '')
            appointment_dt = dateparser.parse(time_str)
            
            if not appointment_dt:
                appointment_dt = datetime.utcnow() + timedelta(days=1)
            
            data_dict['appointment_datetime'] = appointment_dt
            appointment = PatientService.schedule_appointment(db, data_dict)
            
            if appointment:
                success = True
                response_data = {
                    'patient_id': data_dict.get('patient_id'),
                    'appointment_type': appointment.appointment_type,
                    'appointment_datetime': appointment.appointment_datetime.strftime('%B %d, %Y at %I:%M %p')
                }
        
        elif intent == "query_patient":
            patient_record = PatientService.get_patient_full_record(db, data_dict.get('patient_id'))
            if patient_record:
                success = True
                response_data = patient_record
        
        # Generate natural language response
        response_text = AIAgent.generate_response(intent, success, response_data)
        
        print(f"✅ Response generated: {response_text[:100]}...")
        
        # Return in multiple formats for compatibility with different systems
        return {
            "response": response_text,      # Standard field
            "text": response_text,          # Alternative field name
            "message": response_text,       # Alternative field name
            "content": response_text,       # Alternative field name
            "intent": intent,
            "success": success,
            "data": response_data,          # Structured data
            "user_id": user_id,            # Echo back user info
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        error_msg = "Sorry, I encountered an error. Please try again."
        print(f"❌ Error processing message: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "response": error_msg,
            "text": error_msg,
            "message": error_msg,
            "content": error_msg,
            "error": str(e),
            "success": False,
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Nurse ETR Assistant",
        "timestamp": datetime.utcnow().isoformat()
    }