import os
from datetime import datetime, time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

router = APIRouter()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

class BookingRequest(BaseModel):
    patient_name: str
    patient_phone: str
    doctor_name: str
    service_name: str
    appointment_date: str  # YYYY-MM-DD
    appointment_time: str  # HH:MM

@router.post("/book")
def book_appointment(request: BookingRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not configured. Missing SUPABASE_URL or SUPABASE_KEY.")

    try:
        # 1. Verify Doctor
        doctor_res = supabase.table("doctors").select("*").ilike("name", f"%{request.doctor_name}%").execute()
        if not doctor_res.data:
            return {"success": False, "message": f"Doctor {request.doctor_name} not found in our system."}
        doctor = doctor_res.data[0]

        # 2. Verify Service
        service_res = supabase.table("services").select("*").ilike("service_name", f"%{request.service_name}%").execute()
        if not service_res.data:
            return {"success": False, "message": f"Service {request.service_name} not found."}
        service = service_res.data[0]

        # 3. Check Doctor Availability (Day of Week)
        req_date = datetime.strptime(request.appointment_date, "%Y-%m-%d")
        day_of_week = req_date.strftime("%a") # e.g. 'Mon', 'Tue'
        
        # Note: If the request is for a past date, reject it
        if req_date.date() < datetime.now().date():
            return {"success": False, "message": "Cannot book an appointment in the past."}
            
        if day_of_week not in doctor["available_days"]:
            return {"success": False, "message": f"Doctor is only available on {', '.join(doctor['available_days'])}."}

        # 4. Check Doctor Availability (Time)
        req_time = datetime.strptime(request.appointment_time, "%H:%M").time()
        start_str, end_str = doctor["available_time"].split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        if not (start_time <= req_time <= end_time):
            return {"success": False, "message": f"Requested time is outside doctor's working hours ({doctor['available_time']})."}

        # 5. Check for Double Booking
        conflict_res = supabase.table("appointments")\
            .select("id")\
            .eq("doctor_id", doctor["id"])\
            .eq("appointment_date", request.appointment_date)\
            .eq("appointment_time", request.appointment_time)\
            .in_("status", ["pending", "confirmed"])\
            .execute()
            
        if conflict_res.data:
            return {"success": False, "message": "This slot is already booked. Please suggest an alternative time."}

        # 6. Get or Create Patient
        patient_res = supabase.table("patients").select("id").eq("phone", request.patient_phone).execute()
        if patient_res.data:
            patient_id = patient_res.data[0]["id"]
        else:
            new_patient = supabase.table("patients").insert({
                "name": request.patient_name,
                "phone": request.patient_phone
            }).execute()
            patient_id = new_patient.data[0]["id"]

        # 7. Create Appointment
        appointment = supabase.table("appointments").insert({
            "patient_id": patient_id,
            "doctor_id": doctor["id"],
            "service_id": service["id"],
            "appointment_date": request.appointment_date,
            "appointment_time": request.appointment_time,
            "status": "pending",
            "notes": "Booked via AI Assistant"
        }).execute()

        # 8. Trigger n8n Automation Webhook
        import urllib.request, json
        try:
            webhook_url = "https://common-donkeys-laugh.loca.lt/webhook/appointment-booked"
            payload = {
                "patient_name": request.patient_name,
                "patient_phone": request.patient_phone,
                "patient_email": "mohamadhasanpkk101@gmail.com", # Hardcoded for testing, usually fetched from DB
                "doctor_name": request.doctor_name,
                "service_name": request.service_name,
                "appointment_date": request.appointment_date,
                "appointment_time": request.appointment_time
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req)
        except Exception as e:
            print("Warning: Failed to trigger n8n webhook:", e)

        return {
            "success": True, 
            "message": "Appointment successfully booked and pending staff confirmation.",
            "appointment_id": appointment.data[0]["id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CancelRequest(BaseModel):
    appointment_id: str
    patient_phone: str

@router.post("/cancel")
def cancel_appointment(request: CancelRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured.")

    try:
        # Verify appointment exists and belongs to patient
        appt_res = supabase.table("appointments").select("*, patients!inner(phone, name), doctors!inner(name), services!inner(service_name)").eq("id", request.appointment_id).execute()
        
        if not appt_res.data:
            return {"success": False, "message": "Appointment not found."}
            
        appt = appt_res.data[0]
        if appt["patients"]["phone"] != request.patient_phone:
            return {"success": False, "message": "Phone number does not match the appointment record."}

        # Update status to cancelled
        supabase.table("appointments").update({"status": "cancelled"}).eq("id", request.appointment_id).execute()

        # Trigger n8n Webhook for cancellation
        import urllib.request, json
        try:
            webhook_url = "https://common-donkeys-laugh.loca.lt/webhook/appointment-cancelled"
            payload = {
                "patient_name": appt["patients"]["name"],
                "patient_email": "mohamadhasanpkk101@gmail.com",
                "doctor_name": appt["doctors"]["name"],
                "service_name": appt["services"]["service_name"],
                "appointment_date": appt["appointment_date"],
                "appointment_time": appt["appointment_time"]
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req)
        except Exception as e:
            print("Warning: Failed to trigger n8n webhook:", e)

        return {"success": True, "message": "Appointment cancelled successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class RescheduleRequest(BaseModel):
    appointment_id: str
    patient_phone: str
    new_date: str
    new_time: str

@router.post("/reschedule")
def reschedule_appointment(request: RescheduleRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured.")

    try:
        # Verify appointment exists
        appt_res = supabase.table("appointments").select("*, patients!inner(phone, name), doctors!inner(name, available_days, available_time, id), services!inner(service_name)").eq("id", request.appointment_id).execute()
        
        if not appt_res.data:
            return {"success": False, "message": "Appointment not found."}
            
        appt = appt_res.data[0]
        if appt["patients"]["phone"] != request.patient_phone:
            return {"success": False, "message": "Phone number does not match."}
            
        doctor = appt["doctors"]

        # 1. Check Date Validity
        req_date = datetime.strptime(request.new_date, "%Y-%m-%d")
        if req_date.date() < datetime.now().date():
            return {"success": False, "message": "Cannot reschedule to a past date."}
            
        day_of_week = req_date.strftime("%a")
        if day_of_week not in doctor["available_days"]:
            return {"success": False, "message": f"Doctor is only available on {', '.join(doctor['available_days'])}."}

        # 2. Check Time Validity
        req_time = datetime.strptime(request.new_time, "%H:%M").time()
        start_str, end_str = doctor["available_time"].split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        if not (start_time <= req_time <= end_time):
            return {"success": False, "message": f"Time outside doctor's working hours ({doctor['available_time']})."}

        # 3. Check Double Booking
        conflict_res = supabase.table("appointments")\
            .select("id")\
            .eq("doctor_id", doctor["id"])\
            .eq("appointment_date", request.new_date)\
            .eq("appointment_time", request.new_time)\
            .in_("status", ["pending", "confirmed"])\
            .execute()
            
        if conflict_res.data:
            return {"success": False, "message": "This new slot is already booked."}

        # 4. Update Appointment
        supabase.table("appointments").update({
            "appointment_date": request.new_date,
            "appointment_time": request.new_time,
            "status": "pending"
        }).eq("id", request.appointment_id).execute()

        # 5. Trigger n8n Webhook
        import urllib.request, json
        try:
            webhook_url = "https://common-donkeys-laugh.loca.lt/webhook/appointment-rescheduled"
            payload = {
                "patient_name": appt["patients"]["name"],
                "patient_email": "mohamadhasanpkk101@gmail.com",
                "doctor_name": doctor["name"],
                "service_name": appt["services"]["service_name"],
                "old_date": appt["appointment_date"],
                "old_time": appt["appointment_time"],
                "new_date": request.new_date,
                "new_time": request.new_time
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req)
        except Exception as e:
            print("Warning: Failed to trigger n8n webhook:", e)

        return {"success": True, "message": "Appointment rescheduled successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_agent(request: ChatRequest):
    """
    This endpoint receives messages from the Next.js frontend.
    It forwards the message to Flowise/LangChain for AI processing.
    """
    import requests
    
    # NOTE: Replace this URL with your actual Flowise Chatflow API URL!
    # Because Next.js uses port 3000, you may need to run Flowise on port 3001.
    flowise_url = "http://localhost:3001/api/v1/prediction/YOUR_CHATFLOW_ID_HERE"
    
    try:
        # Forward the patient's message to your Flowise AI
        payload = {"question": request.message}
        response = requests.post(flowise_url, json=payload, timeout=15)
        
        if response.status_code == 200:
            flowise_data = response.json()
            # Flowise returns the AI's answer in the 'text' field
            return {"reply": flowise_data.get("text", "I received an empty response from the AI.")}
        else:
            return {"reply": "Error: Flowise is returning a bad status code. Did you update the URL?"}
            
    except Exception as e:
        # Fallback message if Flowise is turned off
        return {"reply": "System Alert: Flowise is currently turned off or the URL is incorrect. Please start Flowise and paste your Chatflow API URL into backend/routes/booking.py!"}
