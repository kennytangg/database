-- Specializations
INSERT INTO Specialization (specialization_id, specialization_name) VALUES
    (1, 'General Practitioner'),
    (2, 'Dermatology'),
    (3, 'Pediatrics'),
    (4, 'Cardiology');

-- Patients
INSERT INTO Patient (patient_id, first_name, last_name, dob, gender, phone_number, email, address) VALUES
    (101, 'Amy', 'Kim', '1997-05-12', 'Female', '081234567890', 'amy.kim@example.com', 'Jl. Merdeka 1'),
    (102, 'Mark', 'Lee', '1989-08-22', 'Male', '081234567891', 'mark.lee@example.com', 'Jl. Sudirman 2'),
    (103, 'Jacob', 'Tan', '2002-03-15', 'Male', '081234567892', 'jacob.tan@example.com', 'Jl. Thamrin 3'),
    (104, 'Michelle', 'Ming', '2000-11-06', 'Female', '081234567893', 'michelle.ming@example.com', 'Jl. Gatot Subroto 4');

-- Doctors
INSERT INTO Doctor (doctor_id, specialization_id, first_name, last_name, phone_number, email) VALUES
    (201, 1, 'Dr. Agung', 'Putra', '081201234500', 'agungputra@clinic.com'),
    (202, 2, 'Dr. Deni', 'Wulandari', '081201234501', 'deniwulandari@clinic.com'),
    (203, 3, 'Dr. Siti', 'Hartono', '081201234502', 'sitihartono@clinic.com'),
    (204, 4, 'Dr. Hendra', 'Salim', '081201234503', 'Hendrasalim@clinic.com');

-- Schedules
INSERT INTO Schedule (schedule_id, doctor_id, available_day, start_time, end_time, is_booked) VALUES
    (301, 201, 'Monday', '09:00', '12:00', FALSE),
    (302, 202, 'Tuesday', '10:00', '13:00', FALSE),
    (303, 203, 'Wednesday', '14:00', '17:00', FALSE),
    (304, 204, 'Friday', '08:00', '11:00', TRUE);

-- Appointments
INSERT INTO Appointment (appointment_id, patient_id, doctor_id, schedule_id, reason_for_visit, appointment_datetime, status) VALUES
    (401, 101, 201, 301, 'Annual checkup', '2025-11-24 09:30', 'completed'),
    (402, 102, 202, 302, 'Skin rash consultation', '2025-11-25 10:45', 'scheduled'),
    (403, 103, 203, 303, 'Child vaccination', '2025-11-26 14:30', 'completed'),
    (404, 101, 204, 304, 'Chest pain', '2025-11-27 08:30', 'cancelled'),
    (405, 104, 201, 301, 'General consultation', '2025-11-28 10:00', 'missed'),
    (406, 104, 202, 302, 'Dermatitis', '2025-12-01 11:30', 'scheduled');

-- Records
INSERT INTO Record (patient_id, appointment_id, diagnosis, prescription, notes) VALUES
    (101, 401, 'Healthy', 'Multivitamin', 'Routine annual exam, no issues.'),
    (103, 403, 'Common cold', 'Cough syrup', 'Vaccination completed, mild cold observed.'),
    (104, 405, 'Missed appointment', '', 'No notes since patient missed.'),
    (101, 404, 'Cancelled appointment', '', 'Cancelled by patient due to health improvement.');

-- Invoices
INSERT INTO Invoice (patient_id, appointment_id, amount, issue_date, status) VALUES
    (101, 401, 150000.00, '2025-11-24', 'paid'),
    (103, 403, 200000.00, '2025-11-26', 'unpaid'),
    (104, 405, 100000.00, '2025-11-28', 'unpaid'),
    (101, 404, 50000.00, '2025-11-27', 'cancelled');
