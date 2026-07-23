-- ============================================================
-- Clinic Appointment Agent — Demo Data (Week 1)
-- DEMO DATA ONLY. No real patient/medical information.
-- Target: Supabase (PostgreSQL)
-- ============================================================

-- 1. TABLES ---------------------------------------------------

create table if not exists patients (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    phone text,
    email text,
    created_at timestamptz default now()
);

create table if not exists doctors (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    specialization text not null,
    available_days text[] not null,   -- e.g. {Mon,Tue,Wed}
    available_time text not null,     -- e.g. '10:00-16:00'
    status text default 'active'
);

create table if not exists services (
    id uuid primary key default gen_random_uuid(),
    service_name text not null,
    duration_minutes int not null,
    price_range text,
    status text default 'active'
);

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

create table if not exists reminders (
    id uuid primary key default gen_random_uuid(),
    appointment_id uuid references appointments(id),
    reminder_type text not null,      -- confirmation | 24hr | 1hr
    reminder_time timestamptz not null,
    status text default 'pending',    -- pending | sent | failed
    created_at timestamptz default now()
);

-- 2. DEMO DOCTORS ----------------------------------------------

insert into doctors (name, specialization, available_days, available_time) values
('Dr. Sara Ahmed', 'General Physician', '{Mon,Tue,Wed,Thu,Fri}', '09:00-15:00'),
('Dr. Imran Khalid', 'Dentist', '{Mon,Wed,Fri}', '11:00-18:00'),
('Dr. Ayesha Malik', 'Dermatologist', '{Tue,Thu,Sat}', '10:00-16:00'),
('Dr. Bilal Hassan', 'Pathologist / Lab', '{Mon,Tue,Wed,Thu,Fri,Sat}', '08:00-14:00');

-- 3. DEMO SERVICES ----------------------------------------------

insert into services (service_name, duration_minutes, price_range) values
('General Consultation', 20, 'PKR 1000-1500'),
('Dental Checkup', 30, 'PKR 1500-2500'),
('Teeth Cleaning', 45, 'PKR 2000-3000'),
('Skin Consultation', 25, 'PKR 1500-2000'),
('Blood Test (CBC)', 15, 'PKR 800-1200'),
('X-Ray', 20, 'PKR 1000-1800');

-- 4. DEMO PATIENTS -----------------------------------------------

insert into patients (name, phone, email) values
('Ali Raza', '+92-300-9876543', 'ali.raza.demo@example.com'),
('Fatima Noor', '+92-301-7654321', 'fatima.noor.demo@example.com'),
('Usman Tariq', '+92-333-9988776', null),
('Zainab Sheikh', null, 'zainab.sheikh.demo@example.com');

-- 5. SAMPLE APPOINTMENT (for testing booking/reminder flow) ------
-- Run after real IDs are generated; example shown as a template query:
--
-- insert into appointments (patient_id, doctor_id, service_id, appointment_date, appointment_time, status, notes)
-- select p.id, d.id, s.id, current_date + interval '2 day', '11:00',
--        'confirmed', 'Demo test booking'
-- from patients p, doctors d, services s
-- where p.name = 'Ali Raza' and d.name = 'Dr. Sara Ahmed' and s.service_name = 'General Consultation'
-- limit 1;
