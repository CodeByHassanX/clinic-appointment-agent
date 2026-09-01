from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, HTTPException
from datetime import datetime
import urllib.request, json
from config import get_supabase_client

router = APIRouter()
supabase = get_supabase_client()

class BookingRequest(BaseModel):
    patient_name: str
    patient_email: str
    patient_phone: str
    doctor_name: str
    service_name: str
    appointment_date: str
    appointment_time: str

@router.post("/book")
def book_appointment(request: BookingRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured.")

    try:
        # 1. Verify Doctor
        doctor_res = supabase.table("doctors").select("*").eq("name", request.doctor_name).execute()
        if not doctor_res.data:
            return {"success": False, "message": f"Doctor {request.doctor_name} not found."}
        doctor = doctor_res.data[0]

        # 2. Check Date Validity
        req_date = datetime.strptime(request.appointment_date, "%Y-%m-%d")
        if req_date.date() < datetime.now().date():
            return {"success": False, "message": "Cannot book an appointment in the past."}
            
        day_of_week = req_date.strftime("%a")
        if day_of_week not in doctor["available_days"]:
            return {"success": False, "message": f"{doctor['name']} is only available on {', '.join(doctor['available_days'])}."}

        # 3. Check Time Validity
        req_time = datetime.strptime(request.appointment_time, "%H:%M").time()
        start_str, end_str = doctor["available_time"].split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        if not (start_time <= req_time <= end_time):
            return {"success": False, "message": f"Time outside doctor's working hours ({doctor['available_time']})."}

        # 4. Verify Service
        service_res = supabase.table("services").select("*").eq("service_name", request.service_name).execute()
        if not service_res.data:
            return {"success": False, "message": f"Service {request.service_name} not found."}
        service = service_res.data[0]

        # 5. Check Double Booking
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
            "appointment_time": request.appointment_time
        }).execute()

        # Trigger n8n Webhook for booking
        try:
            webhook_url = "https://shah1.app.n8n.cloud/webhook/appointment-booked"
            payload = {
                "patient_name": request.patient_name,
                "patient_phone": request.patient_phone,
                "patient_email": (request.patient_email.strip() if request.patient_email and "@" in request.patient_email else "mohamadhasanpkk101@gmail.com"),
                "doctor_name": request.doctor_name,
                "service_name": request.service_name,
                "appointment_date": request.appointment_date,
                "appointment_time": request.appointment_time
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print("Webhook Error:", e)

        return {
            "success": True, 
            "message": "Appointment successfully booked and pending staff confirmation.",
            "appointment_id": appointment.data[0]["id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CancelRequest(BaseModel):
    patient_name: str
    patient_phone: str
    patient_email: str
    appointment_date: str
    doctor_name: str

@router.post("/cancel")
def cancel_appointment(request: CancelRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured.")

    try:
        # Find the appointment by matching phone and date
        appt_res = supabase.table("appointments").select("*, patients!inner(phone, name), doctors!inner(name), services!inner(service_name)").eq("appointment_date", request.appointment_date).in_("status", ["pending", "confirmed"]).execute()
        
        target_appt = None
        for a in appt_res.data:
            if a["patients"]["phone"] == request.patient_phone and a["doctors"]["name"] == request.doctor_name:
                target_appt = a
                break
                
        if not target_appt:
            return {"success": False, "message": "I could not find an active appointment matching those details."}

        # Update status to cancelled
        supabase.table("appointments").update({"status": "cancelled"}).eq("id", target_appt["id"]).execute()

        # Trigger n8n Webhook for cancellation
        try:
            webhook_url = "https://shah1.app.n8n.cloud/webhook/appointment-cancelled"
            payload = {
                "patient_name": target_appt["patients"]["name"],
                "patient_email": (request.patient_email.strip() if request.patient_email and "@" in request.patient_email else "mohamadhasanpkk101@gmail.com"),
                "doctor_name": target_appt["doctors"]["name"],
                "service_name": target_appt["services"]["service_name"],
                "appointment_date": target_appt["appointment_date"],
                "appointment_time": target_appt["appointment_time"]
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print("Webhook Error:", e)

        return {"success": True, "message": f"Your appointment for {request.appointment_date} has been successfully cancelled."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class RescheduleRequest(BaseModel):
    patient_name: str
    patient_phone: str
    patient_email: str
    doctor_name: str
    old_date: str
    new_date: str
    new_time: str

@router.post("/reschedule")
def reschedule_appointment(request: RescheduleRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured.")

    try:
        # Find the old appointment
        appt_res = supabase.table("appointments").select("*, patients!inner(phone, name), doctors!inner(name, available_days, available_time, id), services!inner(service_name)").eq("appointment_date", request.old_date).in_("status", ["pending", "confirmed"]).execute()
        
        target_appt = None
        for a in appt_res.data:
            if a["patients"]["phone"] == request.patient_phone and a["doctors"]["name"] == request.doctor_name:
                target_appt = a
                break
                
        if not target_appt:
            return {"success": False, "message": "I could not find an active appointment on the old date matching your details."}
            
        doctor = target_appt["doctors"]

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
        }).eq("id", target_appt["id"]).execute()

        # 5. Trigger n8n Webhook
        try:
            webhook_url = "https://shah1.app.n8n.cloud/webhook/appointment-rescheduled"
            payload = {
                "patient_name": target_appt["patients"]["name"],
                "patient_email": (request.patient_email.strip() if request.patient_email and "@" in request.patient_email else "mohamadhasanpkk101@gmail.com"),
                "doctor_name": doctor["name"],
                "service_name": target_appt["services"]["service_name"],
                "old_date": target_appt["appointment_date"],
                "old_time": target_appt["appointment_time"],
                "new_date": request.new_date,
                "new_time": request.new_time
            }
            req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true'}, method='POST')
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print("Webhook Error:", e)

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
    flowise_url = "http://localhost:3001/api/v1/prediction/YOUR_CHATFLOW_ID_HERE"
    try:
        payload = {"question": request.message}
        response = requests.post(flowise_url, json=payload, timeout=15)
        if response.status_code == 200:
            flowise_data = response.json()
            return {"reply": flowise_data.get("text", "I received an empty response from the AI.")}
        else:
            return {"reply": "Error: Flowise is returning a bad status code. Did you update the URL?"}
    except Exception as e:
        return {"reply": "System Alert: Flowise is currently turned off or the URL is incorrect. Please start Flowise and paste your Chatflow API URL into backend/routes/booking.py!"}
