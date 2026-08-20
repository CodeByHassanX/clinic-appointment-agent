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

        return {
            "success": True, 
            "message": "Appointment successfully booked and pending staff confirmation.",
            "appointment_id": appointment.data[0]["id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
