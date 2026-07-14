# Week 1 – Requirement Notes
## Clinic Appointment Agent (Synexus Software Technologies)

**Project:** AI-powered appointment booking chatbot for clinics, dentists, and labs
**Duration:** 8 weeks | **Role:** AI/Automation Intern

---

## 1. Purpose
Build a chatbot that talks to patients, understands intent, answers clinic FAQs, collects
appointment details, checks availability, saves records to Supabase, creates Google Calendar
events, and triggers n8n reminder workflows.

## 2. Scope (in)
- Web-based chatbot for booking + support
- Intent detection: book, FAQ, cancel, reschedule, human support
- Small RAG knowledge base (clinic FAQs, doctors, services, timings, fees, location, policies)
- Supabase storage for patients, doctors, services, appointments, reminders
- Google Calendar event creation for confirmed appointments
- n8n workflows for confirmation + reminders
- Final demo, screenshots, GitHub repo, docs, demo video

## 3. Out of Scope (MVP)
Real medical records, payment gateway, production hospital system, AI medical
diagnosis/advice, paid SMS/WhatsApp APIs (unless approved), full CRM.

## 4. Target Users
| User | Role |
|---|---|
| Patient | Books/cancels/reschedules appointments, asks FAQs |
| Clinic Admin | Reviews & manages bookings |
| Doctor/Specialist | Receives scheduled slots via calendar |
| Intern/Developer | Builds, tests, documents, demos |

## 5. Tech Stack
| Component | Tool |
|---|---|
| Chatbot Builder | Flowise or Langflow |
| Knowledge Base / RAG | Documents + Vector Store (Supabase / ChromaDB optional) |
| Database | Supabase |
| Calendar | Google Calendar |
| Automation/Reminders | n8n |
| Backend API (if needed) | FastAPI |
| AI Model | Gemini API free tier / Groq / Ollama local |
| Version Control | GitHub |

## 6. Core Functional Requirements (summary)
- **FR-001 Book Appointment** – collect service, doctor, date, time, name, contact
- **FR-002 FAQ** – answer from knowledge base
- **FR-003 Cancel** – verify patient + appointment ID, mark cancelled
- **FR-004 Reschedule** – collect old + new slot, update appointment & calendar
- **FR-005 Human Support** – capture details, provide contact or create lead

## 7. Slot Booking Rules
- Validate doctor availability, prevent double-booking
- Reject past/invalid date-time
- Ask only for missing fields
- Suggest alternate slots on conflict

## 8. Non-Functional Requirements
Usability (friendly language), Reliability (no confirm without validation),
Performance (fast demo responses), Maintainability (documented flows/schema),
Security (no hardcoded API keys), Privacy (demo data only), Scalability
(multi-doctor/service ready).

## 9. Acceptance Criteria (10 items)
1. Detects all 5 intents
2. Answers FAQs via RAG
3. Collects full appointment slot data
4. Validates availability before confirming
5. Saves data in Supabase
6. Creates Google Calendar events
7. Triggers n8n confirmation/reminders
8. Handles duplicate booking conflicts
9. Submits screenshots, docs, repo, demo video
10. Full end-to-end demo works

## 10. Privacy Note
Use **demo patient data only** throughout development — no real patient/medical data
without formal company approval.

