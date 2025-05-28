CREATE TABLE Patients (
  patient_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  dob DATE,
  gender VARCHAR(10),
  ssn VARCHAR(11),
  marital_status VARCHAR(20),
  visually_impared: true
);

CREATE TABLE ContactDetails (
  contact_id INT PRIMARY KEY,
  patient_id INT,
  email VARCHAR(100),
  phone VARCHAR(20),
  street VARCHAR(100),
  city VARCHAR(50),
  state VARCHAR(50),
  zip VARCHAR(10),
  country VARCHAR(50),
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

CREATE TABLE EmergencyContacts (
  emergency_contact_id INT PRIMARY KEY,
  patient_id INT,
  name VARCHAR(100),
  relationship VARCHAR(50),
  phone VARCHAR(20),
  email VARCHAR(100),
  street VARCHAR(100),
  city VARCHAR(50),
  state VARCHAR(50),
  zip VARCHAR(10),
  country VARCHAR(50),
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

CREATE TABLE InsuranceDetails (
  insurance_id INT PRIMARY KEY,
  patient_id INT,
  provider VARCHAR(100),
  policy_number VARCHAR(50),
  valid_from DATE,
  valid_until DATE,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

CREATE TABLE MedicalHistory (
  history_id INT PRIMARY KEY,
  patient_id INT,
  condition VARCHAR(100),
  diagnosed_on DATE,
  treatment VARCHAR(100),
  notes TEXT,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);


CREATE TABLE Medications (
  medication_id INT PRIMARY KEY,
  patient_id INT,
  name VARCHAR(100),
  dose VARCHAR(50),
  frequency VARCHAR(50),
  prescribed_by VARCHAR(100),
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);


CREATE TABLE Allergies (
  allergy_id INT PRIMARY KEY AUTO_INCREMENT,
  patient_id INT NOT NULL,
  substance VARCHAR(100),
  reaction VARCHAR(100),
  severity VARCHAR(50),
  diagnosed_on DATE,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

CREATE TABLE Appointments (
  appointment_id INT PRIMARY KEY AUTO_INCREMENT,
  patient_id INT NOT NULL,
  date DATE,
  time TIME,
  doctor_name VARCHAR(100),
  doctor_specialty VARCHAR(100),
  doctor_phone VARCHAR(20),
  doctor_email VARCHAR(100),
  reason VARCHAR(255),
  notes TEXT,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);


CREATE TABLE LabResults (
  lab_result_id INT PRIMARY KEY AUTO_INCREMENT,
  patient_id INT NOT NULL,
  test_name VARCHAR(100),
  test_date DATE,
  result_data JSON,
  doctor_name VARCHAR(100),
  doctor_specialty VARCHAR(100),
  doctor_phone VARCHAR(20),
  doctor_email VARCHAR(100),
  notes TEXT,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);


CREATE TABLE Procedures (
  procedure_id INT PRIMARY KEY AUTO_INCREMENT,
  patient_id INT NOT NULL,
  procedure_name VARCHAR(100),
  date DATE,
  surgeon_name VARCHAR(100),
  surgeon_specialty VARCHAR(100),
  surgeon_phone VARCHAR(20),
  surgeon_email VARCHAR(100),
  outcome VARCHAR(255),
  notes TEXT,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);


CREATE TABLE Immunizations (
  immunization_id INT PRIMARY KEY AUTO_INCREMENT,
  patient_id INT NOT NULL,
  vaccine VARCHAR(100),
  date_administered DATE,
  administered_by VARCHAR(100),
  notes TEXT,
  FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);