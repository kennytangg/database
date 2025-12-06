CREATE DATABASE clinicDB;

USE clinicDB;

CREATE TABLE Specialization (
    specialization_id INT PRIMARY KEY,
    specialization_name VARCHAR(100) NOT NULL
);

CREATE TABLE Patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_number VARCHAR(25) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255)
);


CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    specialization_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (specialization_id) REFERENCES Specialization(specialization_id)
);

CREATE TABLE Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    available_day VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE Appointment (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    schedule_id INT NOT NULL,
    reason_for_visit VARCHAR(255),
    appointment_datetime DATETIME NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES Schedule(schedule_id)
);

CREATE TABLE Record (
    appointment_id INT PRIMARY KEY,
    diagnosis VARCHAR(255),
    prescription VARCHAR(255),
    notes TEXT,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id) ON DELETE CASCADE
);

CREATE TABLE Invoice (
    appointment_id INT PRIMARY KEY,
    amount DECIMAL(10, 2),
    issue_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id) ON DELETE CASCADE
);
