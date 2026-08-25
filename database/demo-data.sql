-- ============================================================
-- Clinic Appointment Agent — Demo Data (Supabase)
-- DEMO DATA ONLY. No real patient/medical information.
-- ============================================================

-- 1. DEMO DOCTORS ----------------------------------------------
insert into doctors (name, specialization, available_days, available_time) values
('Dr. Sara Ahmed', 'General Physician', '{Mon,Tue,Wed,Thu,Fri}', '09:00-15:00'),
('Dr. Imran Khalid', 'Dentist', '{Mon,Wed,Fri}', '11:00-18:00'),
('Dr. Ayesha Malik', 'Dermatologist', '{Tue,Thu,Sat}', '10:00-16:00'),
('Dr. Bilal Hassan', 'Pathologist / Lab', '{Mon,Tue,Wed,Thu,Fri,Sat}', '08:00-14:00');

-- 2. DEMO SERVICES ----------------------------------------------
insert into services (service_name, duration_minutes, price_range) values
('General Consultation', 20, 'PKR 1000-1500'),
('Dental Checkup', 30, 'PKR 1500-2500'),
('Teeth Cleaning', 45, 'PKR 2000-3000'),
('Skin Consultation', 25, 'PKR 1500-2000'),
('Blood Test (CBC)', 15, 'PKR 800-1200'),
('X-Ray', 20, 'PKR 1000-1800');

-- 3. DEMO PATIENTS -----------------------------------------------
insert into patients (name, phone, email) values
('Ali Raza', '+92-300-9876543', 'ali.raza.demo@example.com'),
('Fatima Noor', '+92-301-7654321', 'fatima.noor.demo@example.com'),
('Usman Tariq', '+92-333-9988776', null),
('Zainab Sheikh', null, 'zainab.sheikh.demo@example.com');

-- 4. SAMPLE APPOINTMENT (Template) -------------------------------
-- Example of how to insert an appointment after generating real IDs

-- Appointment 1: Ali Raza with Dr. Sara Ahmed
insert into appointments (patient_id, doctor_id, service_id, appointment_date, appointment_time, status, notes)
select p.id, d.id, s.id,
       current_date + interval '2 day',
       '11:00',
       'confirmed',
       'Demo test booking'
from patients p, doctors d, services s
where p.name = 'Ali Raza'
  and d.name = 'Dr. Sara Ahmed'
  and s.service_name = 'General Consultation'
limit 1;
 
-- Appointment 2: Fatima Noor with Dr. Imran Khalid
insert into appointments (patient_id, doctor_id, service_id, appointment_date, appointment_time, status, notes)
select p.id, d.id, s.id,
       current_date + interval '4 day',
       '14:00',
       'pending',
       'Demo test booking 2'
from patients p, doctors d, services s
where p.name = 'Fatima Noor'
  and d.name = 'Dr. Imran Khalid'
  and s.service_name = 'Dental Checkup'
limit 1;
 
 
-- ---------------------------------------------------------------
-- READ: View all appointments with human-readable joins
-- ---------------------------------------------------------------
 
select p.name as patient, d.name as doctor, s.service_name,
       a.appointment_date, a.appointment_time, a.status, a.notes
from appointments a
join patients p on a.patient_id = p.id
join doctors d on a.doctor_id = d.id
join services s on a.service_id = s.id
order by a.appointment_date;
 
 
-- ---------------------------------------------------------------
-- UPDATE: Cancel the second appointment
-- ---------------------------------------------------------------
 
update appointments
set status = 'cancelled'
where notes = 'Demo test booking 2';
 
-- Verify the update
select p.name as patient, a.status
from appointments a
join patients p on a.patient_id = p.id
where a.notes = 'Demo test booking 2';
 
 
-- ---------------------------------------------------------------
-- DELETE: Remove the first test appointment
-- ---------------------------------------------------------------
 
delete from appointments
where notes = 'Demo test booking';
 
-- Verify the delete (should return zero rows)
select * from appointments where notes = 'Demo test booking';
 
 
-- ---------------------------------------------------------------
-- CLEANUP (optional): remove all demo appointments after testing
-- ---------------------------------------------------------------
 
delete from appointments where notes like 'Demo test booking%';
 
