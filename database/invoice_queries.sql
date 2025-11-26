-- CREATE: Add a new invoice for any appointment
INSERT INTO Invoice (appointment_id, amount, issue_date, status)
VALUES (405, 250000.00, '2025-11-29', 'unpaid');

-- CREATE: Add an invoice for a completed appointment only
INSERT INTO Invoice (appointment_id, amount, issue_date, status)
SELECT a.appointment_id, 150000.00, CURDATE(), 'unpaid'
FROM Appointment a
WHERE a.appointment_id = 401 AND a.status = 'completed';

-- READ: Get all invoices (view all billing details)
SELECT * FROM Invoice;

-- READ: Get invoice for a specific appointment
SELECT * FROM Invoice WHERE appointment_id = 403;

-- UPDATE: Mark an invoice as paid and update issue date
UPDATE Invoice
SET status = 'paid', issue_date = CURDATE()
WHERE appointment_id = 401;

-- DELETE: Remove an invoice (cancel bill for an appointment)
DELETE FROM Invoice WHERE appointment_id = 404;

-- Total billing amount by payment status
SELECT status, SUM(amount) AS total_amount
FROM Invoice
GROUP BY status;

-- Show patient, appointment, and invoice info by joining tables
SELECT p.patient_id, p.first_name, a.appointment_id, i.amount, i.status
FROM Invoice i
JOIN Appointment a ON i.appointment_id = a.appointment_id
JOIN Patient p ON a.patient_id = p.patient_id;

-- List all unpaid invoices and related appointment/patient info
SELECT i.appointment_id, p.first_name, p.last_name, i.amount, i.issue_date
FROM Invoice i
JOIN Appointment a ON i.appointment_id = a.appointment_id
JOIN Patient p ON a.patient_id = p.patient_id
WHERE i.status = 'unpaid';

-- Count invoices per patient
SELECT a.patient_id, COUNT(*) AS total_invoices
FROM Invoice i
JOIN Appointment a ON i.appointment_id = a.appointment_id
GROUP BY a.patient_id;
