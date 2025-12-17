-- specializations
INSERT INTO Specialization (specialization_id, specialization_name) VALUES
    (1, 'General Practitioner'),
    (2, 'Dermatology'),
    (3, 'Dentist');


-- patients
INSERT INTO Patient (patient_id, first_name, last_name, dob, gender, phone_number, email, address) VALUES
    (101, 'Amy', 'Kim', '1997-05-12', 'Female', '081234567890', 'amy.kim@example.com', 'Jl. Merdeka 1'),
    (102, 'Mark', 'Lee', '1989-08-22', 'Male', '081234567891', 'mark.lee@example.com', 'Jl. Sudirman 2'),
    (103, 'Jacob', 'Tan', '2002-03-15', 'Male', '081234567892', 'jacob.tan@example.com', 'Jl. Thamrin 3'),
    (104, 'Michelle', 'Ming', '2000-11-06', 'Female', '081234567893', 'michelle.ming@example.com', 'Jl. Gatot Subroto 4'),
    (105, 'Linda', 'Wong', '1988-07-12', 'Female', '081234567894', 'linda.wong@example.com', 'Jl. Mangga 5'),
    (106, 'Brian', 'Simanjuntak', '1992-04-10', 'Male', '081234567895', 'brian.simanjuntak@example.com', 'Jl. Bali 6');


-- doctors
INSERT INTO Doctor (doctor_id, specialization_id, first_name, last_name, phone_number, email) values
    (201, 1, 'dr. Agung', 'Putra', '081201234500', 'agungputra@clinic.com'),
    (202, 1, 'dr. Deni', 'Wulandari', '081201234501', 'deniwulandari@clinic.com'),
    (203, 2, 'dr. Siti', 'Hartono', '081201234502', 'sitihartono@clinic.com'),
    (204, 3, 'dr. Katrina', 'Chandra', '081201234505', 'katrina.chandra@clinic.com');


-- schedules
INSERT INTO Schedule (schedule_id, doctor_id, available_day, start_time, end_time, is_booked) values
    (301, 201, 'Monday', '09:00', '09:30', TRUE),
    (302, 201, 'Monday', '09:30', '10:00', TRUE),
    (303, 201, 'Monday', '10:00', '10:30', TRUE),
    (304, 201, 'Monday', '10:30', '11:00', TRUE),
    (305, 201, 'Thursday', '13:00', '13:30', FALSE),
    (306, 202, 'Tuesday', '10:00', '10:30', TRUE),
    (307, 202, 'Tuesday', '10:30', '11:00', TRUE),
    (308, 202, 'Tuesday', '11:00', '11:30', FALSE),
    (309, 203, 'Wednesday', '14:00', '14:30', TRUE),
    (310, 203, 'Wednesday', '14:30', '15:00', FALSE),
    (311, 204, 'Friday', '08:30', '09:00', TRUE),
    (312, 204, 'Friday', '09:00', '09:30', FALSE);
    
-- Appointments
INSERT INTO Appointment (appointment_id, patient_id, schedule_id, reason_for_visit, appointment_datetime, status) VALUES
    (401, 101, 301, 'Annual checkup', '2025-12-15 09:00', 'completed'),
    (407, 102, 303, 'Flu symptoms', '2025-11-18 10:00', 'completed'),
    (408, 102, 304, 'Follow-up flu', '2025-11-25 10:30', 'completed'),
    (402, 104, 302, 'General consultation', '2025-12-22 09:30', 'scheduled'),
    (403, 102, 306, 'Skin rash evaluation', '2025-12-17 10:00', 'scheduled'),
    (404, 106, 307, 'Follow-up', '2025-12-17 10:30', 'scheduled'),
    (405, 105, 309, 'Acne treatment', '2025-12-18 14:00', 'scheduled'),
    (406, 103, 311, 'Dental cleaning', '2025-12-20 08:30', 'scheduled');


-- Records (only for completed appointments)
INSERT INTO Record (appointment_id, diagnosis, prescription, notes) VALUES
    (401, 'Healthy', 'Multivitamin', 'Routine annual exam, no issues.'),
    (407, 'Influenza Type A', 'Oseltamivir 75mg, Paracetamol 500mg', 'Rest for 3-5 days. Return if symptoms worsen.'),
    (408, 'Recovered from flu', 'Continue vitamin C', 'Patient recovered well. No further treatment needed.');


-- Invoices (only for completed appointments)
INSERT INTO Invoice (appointment_id, amount, issue_date, status) VALUES
    (401, 150000.00, '2025-12-15', 'paid'),
    (407, 200000.00, '2025-11-18', 'paid'),
    (408, 120000.00, '2025-11-25', 'unpaid');
