-- specializations
insert into specialization (specialization_id, specialization_name) values
    (1, 'general practitioner'),
    (2, 'dermatology'),
    (3, 'dentist');

-- patients
insert into patient (patient_id, first_name, last_name, dob, gender, phone_number, email, address) values
    (101, 'amy', 'kim', '1997-05-12', 'female', '081234567890', 'amy.kim@example.com', 'jl. merdeka 1'),
    (102, 'mark', 'lee', '1989-08-22', 'male', '081234567891', 'mark.lee@example.com', 'jl. sudirman 2'),
    (103, 'jacob', 'tan', '2002-03-15', 'male', '081234567892', 'jacob.tan@example.com', 'jl. thamrin 3'),
    (104, 'michelle', 'ming', '2000-11-06', 'female', '081234567893', 'michelle.ming@example.com', 'jl. gatot subroto 4'),
    (105, 'linda', 'wong', '1988-07-12', 'female', '081234567894', 'linda.wong@example.com', 'jl. mangga 5'),
    (106, 'brian', 'simanjuntak', '1992-04-10', 'male', '081234567895', 'brian.simanjuntak@example.com', 'jl. bali 6');

-- doctors
insert into doctor (doctor_id, specialization_id, first_name, last_name, phone_number, email) values
    (201, 1, 'dr. agung', 'putra', '081201234500', 'agungputra@clinic.com'),
    (202, 1, 'dr. deni', 'wulandari', '081201234501', 'deniwulandari@clinic.com'),
    (203, 2, 'dr. siti', 'hartono', '081201234502', 'sitihartono@clinic.com'),
    (204, 3, 'dr. katrina', 'chandra', '081201234505', 'katrina.chandra@clinic.com');

-- schedules
insert into schedule (schedule_id, doctor_id, available_day, start_time, end_time, is_booked) values
    (301, 201, 'Monday', '09:00', '09:30', TRUE),
    (302, 201, 'Monday', '09:30', '10:00', TRUE),
    (303, 201, 'Monday', '10:00', '10:30', FALSE),
    (304, 201, 'Monday', '10:30', '11:00', FALSE),
    (305, 201, 'Thursday', '13:00', '13:30', FALSE),
    (306, 202, 'Tuesday', '10:00', '10:30', TRUE),
    (307, 202, 'Tuesday', '10:30', '11:00', FALSE),
    (308, 202, 'Tuesday', '11:00', '11:30', FALSE),
    (309, 203, 'Wednesday', '14:00', '14:30', TRUE),
    (310, 203, 'Wednesday', '14:30', '15:00', FALSE),
    (311, 204, 'Friday', '08:30', '09:00', TRUE),
    (312, 204, 'Friday', '09:00', '09:30', FALSE);

-- Appointments
INSERT INTO Appointment (appointment_id, patient_id, schedule_id, reason_for_visit, appointment_datetime, status) VALUES
    (401, 101, 301, 'Annual checkup', '2025-11-24 09:00', 'completed'),
    (402, 104, 302, 'General consultation', '2025-11-24 09:30', 'scheduled'),
    (403, 102, 306, 'Skin rash evaluation', '2025-11-25 10:00', 'completed'),
    (404, 106, 307, 'Follow-up', '2025-11-25 10:30', 'missed'),
    (405, 105, 309, 'Acne treatment', '2025-11-26 14:00', 'completed'),
    (406, 103, 311, 'Dental cleaning', '2025-11-27 08:30', 'completed');

-- Records
INSERT INTO Record (appointment_id, diagnosis, prescription, notes) VALUES
    (401, 'Healthy', 'Multivitamin', 'Routine annual exam, no issues.'),
    (403, 'Dermatitis', 'Hydrocortisone cream', 'Rash evaluated, mild eczema.'),
    (405, 'Acne', 'Benzoyl peroxide', 'Prescribed topical for moderate acne.'),
    (406, 'Plaque buildup', 'Routine cleaning', 'Dental cleaning successful.');

-- Invoices
INSERT INTO Invoice (appointment_id, amount, issue_date, status) VALUES
    (401, 150000.00, '2025-11-24', 'paid'),
    (403, 180000.00, '2025-11-25', 'unpaid'),
    (405, 190000.00, '2025-11-26', 'unpaid'),
    (406, 200000.00, '2025-11-27', 'unpaid');
