-- ============================================================
-- Clinic Appointment Agent — Database Schema (Supabase)
-- ============================================================

-- 1. Patients Table
create table if not exists patients (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    phone text,
    email text,
    created_at timestamptz default now()
);

-- 2. Doctors Table
create table if not exists doctors (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    specialization text not null,
    available_days text[] not null,   -- e.g. {Mon,Tue,Wed}
    available_time text not null,     -- e.g. '10:00-16:00'
    status text default 'active'
);

-- 3. Services Table
create table if not exists services (
    id uuid primary key default gen_random_uuid(),
    service_name text not null,
    duration_minutes int not null,
    price_range text,
    status text default 'active'
);

-- 4. Appointments Table
create table if not exists appointments (
    id uuid primary key default gen_random_uuid(),
    patient_id uuid references patients(id),
    doctor_id uuid references doctors(id),
    service_id uuid references services(id),
    appointment_date date not null,
    appointment_time time not null,
    status text default 'pending',    -- pending | confirmed | cancelled | rescheduled
    notes text,
    google_calendar_event_id text,
    created_at timestamptz default now()
);

-- 5. Reminders Table
create table if not exists reminders (
    id uuid primary key default gen_random_uuid(),
    appointment_id uuid references appointments(id),
    reminder_type text not null,      -- confirmation | 24hr | 1hr
    reminder_time timestamptz not null,
    status text default 'pending',    -- pending | sent | failed
    created_at timestamptz default now()
);
