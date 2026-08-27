# Clinic Appointment Agent 🏥🤖

An AI-powered Clinic Receptionist Agent built with a modern tech stack. The agent can seamlessly **book, reschedule, and cancel** appointments through a natural conversation. 

## 🚀 Architecture & Tech Stack
- **Frontend:** Next.js (React) 
- **Backend:** Python FastAPI (hosted on Vercel)
- **AI Engine:** Flowise AI (LangChain framework)
- **Database:** Supabase (PostgreSQL)
- **Automation:** n8n (Google Calendar & Gmail integrations)

## 🌟 Features
1. **Natural Conversations:** Talk to the AI naturally to find available times.
2. **Smart Booking:** Automatically checks doctor schedules and prevents double-booking.
3. **Rescheduling & Canceling:** Uses Phone Number and Date verification to securely modify appointments.
4. **Automated Emails:** n8n instantly sends HTML confirmation emails to the patient upon any action.
5. **Google Calendar:** Automatically syncs confirmed appointments to the doctor's Google Calendar.

## 🛠️ Local Setup

### 1. Database (Supabase)
Create a Supabase project and create the following tables:
- patients (id, name, phone)
- doctors (id, name, available_days, available_time)
- services (id, service_name)
- ppointments (id, patient_id, doctor_id, service_id, appointment_date, appointment_time, status)

### 2. Backend (FastAPI)
Navigate to the \ackend\ folder and install dependencies:
\\\ash
pip install -r requirements.txt
\\\
Set up your environment variables:
\\\env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
\\\
Run the backend:
\\\ash
uvicorn main:app --reload
\\\

### 3. Frontend (Next.js)
Navigate to the \rontend\ folder and install dependencies:
\\\ash
npm install
\\\
Run the development server:
\\\ash
npm run dev
\\\

### 4. AI & Automation
- **Flowise:** Import the Chatflow JSON and configure the Custom Tools (\ook_appointment\, \eschedule_appointment\, \cancel_appointment\) to point to the FastAPI endpoints.
- **n8n:** Import the 3 workflows for Booking, Rescheduling, and Canceling. Configure the Webhook nodes and connect your Gmail and Google Calendar credentials.
