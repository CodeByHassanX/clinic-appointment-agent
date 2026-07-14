# Clinic Appointment Agent

AI-powered appointment booking chatbot for clinics, dentists, and diagnostic labs.
Built as an internship project for **Synexus Software Technologies**.

## Overview
The chatbot detects patient intent (book / FAQ / cancel / reschedule / human support),
answers clinic questions via a small RAG knowledge base, collects appointment details,
validates availability, stores records in Supabase, creates Google Calendar events, and
triggers n8n reminder workflows.

![Architecture Diagram](./Architecture_Diagram.png)

> **Note:** This project uses demo clinic and patient data only. No real patient or
> medical information is used.

## Tech Stack
- **Chatbot Builder:** Flowise / Langflow
- **Knowledge Base:** RAG (documents + vector store)
- **Database:** Supabase (PostgreSQL)
- **Calendar:** Google Calendar API
- **Automation:** n8n
- **Backend (optional):** FastAPI
- **AI Model:** Gemini API (free tier) / Groq / Ollama

## Repository Structure
```
clinic-appointment-agent/
├── README.md
├── docs/
│   ├── requirement-notes.md
│   ├── architecture-diagram.mermaid
│   ├── srs.pdf
│   └── final-report.md
├── knowledge-base/
│   ├── clinic-faq.md
│   ├── doctors.md
│   ├── services.md
│   └── policies.md
├── database/
│   ├── schema.sql
│   └── demo-data.sql
├── chatbot-flow/
│   └── flowise-export.json
├── backend/                # optional FastAPI service
│   ├── main.py
│   ├── routes/
│   └── requirements.txt
├── n8n-workflows/
│   ├── appointment-confirmation.json
│   ├── reminder-24hr.json
│   ├── reminder-1hr.json
│   ├── cancellation-update.json
│   └── reschedule-update.json
├── screenshots/
├── test-cases/
│   └── booking-cancel-reschedule-tests.md
└── demo-video-link.md
```

## Weekly Progress
| Week | Focus | Status |
|---|---|---|
| 1 | Requirement analysis, setup, demo data, architecture | 🔲 |
| 2 | Clinic FAQ + RAG knowledge base | 🔲 |
| 3 | Chatbot flow + intent detection | 🔲 |
| 4 | Supabase database + data models | 🔲 |
| 5 | Slot booking logic + validation | 🔲 |
| 6 | Google Calendar + n8n workflows | 🔲 |
| 7 | Cancellation, rescheduling, QA | 🔲 |
| 8 | Final demo + documentation | 🔲 |

## Setup (to be completed as project progresses)
1. Clone repo
2. Set up Supabase project, run `database/schema.sql`
3. Configure Flowise/Langflow chatbot flow
4. Add Google Calendar API credentials (never commit keys)
5. Import n8n workflows
6. Run backend (if used): `pip install -r requirements.txt && uvicorn main:app --reload`

## Security
API keys and credentials are kept in a local `.env` file (git-ignored) — never committed
to the repository.

## License
Internship project — Synexus Software Technologies.
