# AI Clinic Appointment Agent 🏥🤖

A fully autonomous AI-powered clinic agent that handles patient inquiries, validates availability, and manages appointments end-to-end. Built with a modern stack including FastAPI, Supabase, n8n, and Flowise.

## 🛠️ How to Run Locally (For Testers & Reviewers)

### 1. Database (Supabase)
Create a Supabase project and create the following tables:
- `patients` (id, name, phone)
- `doctors` (id, name, available_days, available_time)
- `services` (id, service_name)
- `appointments` (id, patient_id, doctor_id, service_id, appointment_date, appointment_time, status)

### 2. Backend (FastAPI)
Navigate to the `backend` folder and install dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the `backend` folder with:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```
Run the backend:
```bash
uvicorn main:app --reload
```

### 3. Frontend (Next.js)
Navigate to the `frontend` folder and install dependencies:
```bash
npm install
```
Run the development server:
```bash
npm run dev
```

### 4. AI & Automation
- **Flowise:** Import the Chatflow JSON into Flowise and configure the Custom Tools (`book_appointment`, `reschedule_appointment`, `cancel_appointment`) to point to your live FastAPI endpoints.
- **n8n:** Create Webhooks for Booking, Rescheduling, and Canceling. Connect your Gmail and Google Calendar credentials.

---

## 📁 Project Structure

```text
├── README.md
├── docs/                                 # Documentation and architectural diagrams
│   ├── requirement-notes.md
│   ├── architecture-diagram.mermaid
│   ├── srs.pdf
│   └── final-report.md
├── knowledge-base/                       # RAG Knowledge Base files
│   ├── clinic-faq.md
│   ├── doctors.md
│   ├── services.md
│   └── policies.md
├── database/                             # Database schemas and seed data
│   ├── schema.sql
│   └── demo-data.sql
├── chatbot-flow/                         # LLM / Flowise Agent configs
│   └── flowise-export.json
├── backend/                              # Python FastAPI Server
│   ├── main.py
│   ├── routes/
│   │   └── booking.py
│   └── requirements.txt
├── frontend/                             # Next.js Chatbot UI
├── n8n-workflows/                        # Automation pipelines
│   ├── appointment-confirmation.json
│   ├── reminder-24hr.json
│   ├── reminder-1hr.json
│   ├── cancellation-update.json
│   └── reschedule-update.json
├── screenshots/                          # Visual proof of work, organized by week
│   ├── Week_1/
│   ├── Week_2/
│   └── ...
└── test-cases/
    └── booking-cancel-reschedule-tests.md
```

## 🗓️ Internship Progress: Week by Week

### Week 1: AI Agent Setup & RAG Knowledge Base
- Designed the overarching architecture for the Clinic AI.
- Created the core knowledge base documents (`clinic-faq.md`, `doctors.md`, `services.md`, `policies.md`).
- Built the foundation for the Retrieval-Augmented Generation (RAG) system so the AI can answer clinic-specific questions accurately.

### Week 2: LangChain & Intent Detection
- Developed the LLM logic to distinguish between casual chat, Q&A, and booking intents.
- Configured the system to extract precise entities (Patient Name, Doctor Name, Service, Date, Time) from natural language.
- Exported the chatbot flow configurations.

### Week 3: Database Architecture (Supabase)
- Designed the PostgreSQL relational database schema.
- Created tables for `patients`, `doctors`, `services`, and `appointments`.
- Wrote the `schema.sql` and `demo-data.sql` scripts to seed the database with test doctors and services.

### Week 4 & 5: Core FastAPI Backend & Booking Logic
- Built the Python FastAPI backend to serve as the bridge between the AI and the Database.
- Implemented the `/api/book` endpoint.
- Added strict validation logic: checking doctor availability, validating working hours, and preventing double-booking.
- Resolved Supabase Row Level Security (RLS) policies to allow secure inserts.

### Week 6: n8n Automation (Webhooks, Calendar & Email)
- Deployed n8n locally via Docker.
- Connected the FastAPI backend to n8n using HTTP Webhooks.
- Built the `appointment-confirmation.json` workflow.
- Automated Google Calendar event creation and dynamic Email Confirmations to patients.

### Week 7: Cancellations & Rescheduling
- Added `/api/cancel` and `/api/reschedule` endpoints to the FastAPI backend.
- Built n8n workflows (`cancellation-update.json` and `reschedule-update.json`) to handle calendar cleanup.
- Ensured the database stays perfectly synced with Google Calendar and patient emails.

### Week 8: Frontend UI & Final Polish
- Reorganized the monolithic repository into a clean, production-ready directory structure.
- Developed a sleek **Next.js (React + Tailwind)** Chatbot UI for patients to interact with the agent natively.
- Finalized project documentation and test cases.

---
*Developed during the AI Automation Internship at Synexus Software Technologies.*
