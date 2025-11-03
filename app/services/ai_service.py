import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

class AIAgent:
    
    @staticmethod
    def parse_intent(message: str) -> dict:
        """
        Determine user intent and extract relevant information
        """
        prompt = f"""
You are a healthcare assistant AI. Analyze this nurse's message and extract structured information.

Message: "{message}"

Return a JSON object with:
- intent: one of ["register_patient", "record_vitals", "add_diagnosis", "prescribe_medication", "schedule_appointment", "query_patient", "list_reminders", "unknown"]
- data: extracted relevant information based on intent

Examples:
1. "New patient John Doe, 45 years old, male" → {{"intent": "register_patient", "data": {{"name": "John Doe", "age": 45, "gender": "male"}}}}
2. "Record vitals for PT001: BP 120/80, temp 37.2, pulse 75" → {{"intent": "record_vitals", "data": {{"patient_id": "PT001", "blood_pressure": "120/80", "temperature": 37.2, "pulse": 75}}}}
3. "Dr Smith diagnosed PT001 with hypertension" → {{"intent": "add_diagnosis", "data": {{"patient_id": "PT001", "doctor_name": "Dr Smith", "diagnosis": "hypertension"}}}}
4. "Prescribe amoxicillin 500mg three times daily for PT001" → {{"intent": "prescribe_medication", "data": {{"patient_id": "PT001", "medication_name": "amoxicillin", "dosage": "500mg", "frequency": "three times daily"}}}}
5. "Schedule follow-up for PT001 tomorrow at 2pm" → {{"intent": "schedule_appointment", "data": {{"patient_id": "PT001", "appointment_type": "follow-up", "time": "tomorrow at 2pm"}}}}
6. "Show me PT001's records" → {{"intent": "query_patient", "data": {{"patient_id": "PT001"}}}}

Return ONLY valid JSON, no explanation.
"""
        
        try:
            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            result = json.loads(result_text)
            return result
        except Exception as e:
            print(f"AI parsing error: {e}")
            return {"intent": "unknown", "data": {}}
    
    @staticmethod
    def generate_response(intent: str, success: bool, data: dict = None) -> str:
        """
        Generate natural language responses
        """
        if intent == "register_patient" and success:
            return f"✅ Patient registered successfully!\n\n**Patient ID:** {data.get('patient_id')}\n**Name:** {data.get('name')}\n\nYou can now record vitals, diagnoses, and medications using this Patient ID."
        
        elif intent == "record_vitals" and success:
            vitals = data.get('vitals', {})
            vitals_text = "\n".join([f"• {k.replace('_', ' ').title()}: {v}" for k, v in vitals.items() if v])
            return f"✅ Vitals recorded for Patient {data.get('patient_id')}:\n\n{vitals_text}"
        
        elif intent == "add_diagnosis" and success:
            return f"✅ Diagnosis added for Patient {data.get('patient_id')}:\n\n**Doctor:** {data.get('doctor_name')}\n**Diagnosis:** {data.get('diagnosis')}"
        
        elif intent == "prescribe_medication" and success:
            return f"✅ Medication prescribed for Patient {data.get('patient_id')}:\n\n**Medication:** {data.get('medication_name')}\n**Dosage:** {data.get('dosage')}\n**Frequency:** {data.get('frequency')}\n\n⏰ Reminders have been set automatically."
        
        elif intent == "schedule_appointment" and success:
            return f"✅ Appointment scheduled for Patient {data.get('patient_id')}:\n\n**Type:** {data.get('appointment_type')}\n**Date/Time:** {data.get('appointment_datetime')}\n\n📅 Reminder will be sent 24 hours before."
        
        elif intent == "query_patient" and success:
            patient = data.get('patient', {})
            vitals = data.get('vitals', [])
            diagnoses = data.get('diagnoses', [])
            medications = data.get('medications', [])
            
            response = f"📋 **Patient Record: {patient.get('patient_id')}**\n\n"
            response += f"**Name:** {patient.get('name')}\n"
            response += f"**Age:** {patient.get('age', 'N/A')}\n"
            response += f"**Gender:** {patient.get('gender', 'N/A')}\n\n"
            
            if vitals:
                latest_vital = vitals[0]
                response += "**Latest Vitals:**\n"
                if latest_vital.get('blood_pressure'):
                    response += f"• BP: {latest_vital['blood_pressure']}\n"
                if latest_vital.get('temperature'):
                    response += f"• Temp: {latest_vital['temperature']}°C\n"
                if latest_vital.get('pulse'):
                    response += f"• Pulse: {latest_vital['pulse']} BPM\n\n"
            
            if diagnoses:
                response += "**Diagnoses:**\n"
                for d in diagnoses[:3]:
                    response += f"• {d.get('diagnosis')} (Dr. {d.get('doctor_name')})\n"
                response += "\n"
            
            if medications:
                response += "**Active Medications:**\n"
                for m in [med for med in medications if med.get('is_active') == 1]:
                    response += f"• {m.get('medication_name')} {m.get('dosage')} - {m.get('frequency')}\n"
            
            return response
        
        elif not success:
            return f"❌ Sorry, I couldn't complete that action. Please check the patient ID and try again."
        
        else:
            return "I'm here to help! You can:\n\n• Register a new patient\n• Record vitals\n• Add diagnoses\n• Prescribe medications\n• Schedule appointments\n• Query patient records\n\nJust tell me what you need!"