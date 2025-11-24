-- Specializations
INSERT INTO Specialization (specialization_id, specialization_name) VALUES
    (1, 'General Practitioner'),
    (2, 'Dermatology'),
    (3, 'Pediatrics');

-- Patients
INSERT INTO Patient (patient_id, first_name, last_name, dob, gender, phone_number, email, address) VALUES
    (101, 'Alice', 'Kim', '1997-05-12', 'Female', '081234567890', 'alice.kim@example.com', 'Jl. Merdeka 1'),
    (102, 'Bob', 'Lee', '1989-08-22', 'Male', '081234567891', 'bob.lee@example.com', 'Jl. Sudirman 2'),
    (103, 'Charlie', 'Tan', '2002-03-15', 'Male', '081234567892', 'charlie.tan@example.com', 'Jl. Thamrin 3');

-- Doctors
INSERT INTO Doctor (doctor_id, specialization_id, first_name, last_name, phone_number, email) VALUES
    (201, 1, 'Dr. Hana', 'Putra', '081201234500', 'hanaputra@clinic.com'),
    (202, 2, 'Dr. Deni', 'Wulandari', '081201234501', 'deniwulandari@clinic.com'),
    (203, 3, 'Dr. Siti', 'Hartono', '081201234502', 'sitihartono@clinic.com');

-- Schedules (for each doctor)
INSERT INTO Schedule (schedule_id, doctor_id, available_day, start_time, end_time, is_booked) VALUES
    (301, 201, 'Monday', '09:00', '12:00', FALSE),
    (302, 202, 'Tuesday', '10:00', '13:00', FALSE),
    (303, 203, 'Wednesday', '14:00', '17:00', FALSE);

-- Appointments (connect patient, doctor, and schedule)
INSERT INTO Appointment (appointment_id, patient_id, doctor_id, schedule_id, reason_for_visit, appointment_datetime, status) VALUES
    (401, 101, 201, 301, 'Annual checkup', '2025-11-24 09:30', 'completed'),
    (402, 102, 202, 302, 'Skin rash consultation', '2025-11-25 10:45', 'scheduled'),
    (403, 103, 203, 303, 'Child vaccination', '2025-11-26 14:30', 'completed');

-- Records (patients that completed appointments get records)
INSERT INTO Record (patient_id, appointment_id, diagnosis, prescription, notes) VALUES
    (101, 401, 'Healthy', 'Multivitamin', 'Routine annual exam, no issues.'),
    (103, 403, 'Common cold', 'Cough syrup', 'Vaccination completed, mild cold observed.');

-- Invoices
INSERT INTO Invoice (patient_id, appointment_id, amount, issue_date, status) VALUES
    (101, 401, 150000.00, '2025-11-24', 'paid'),
    (103, 403, 200000.00, '2025-11-26', 'unpaid');
