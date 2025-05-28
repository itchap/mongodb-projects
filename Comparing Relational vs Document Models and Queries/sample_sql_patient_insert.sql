-- Insert data into Patients table
INSERT INTO Patients (patient_id, first_name, last_name, dob, gender, ssn, marital_status, vis_imp)
VALUES (1, 'John', 'Doe', '1980-05-15', 'Male', '123-45-6789', 'Married', true);

-- Insert data into ContactDetails table
INSERT INTO ContactDetails (contact_id, patient_id, email, phone, street, city, state, zip, country)
VALUES (1, 1, 'john.doe@example.com', '555-1234', '123 Main St', 'Anytown', 'Anystate', '12345', 'USA');

-- Insert data into EmergencyContacts table
INSERT INTO EmergencyContacts (emergency_contact_id, patient_id, name, relationship, phone, email, street, city, state, zip, country)
VALUES (1, 1, 'Jane Doe', 'Spouse', '555-5678', 'jane.doe@example.com', '123 Main St', 'Anytown', 'Anystate', '12345', 'USA');

-- Insert data into InsuranceDetails table
INSERT INTO InsuranceDetails (insurance_id, patient_id, provider, policy_number, valid_from, valid_until)
VALUES (1, 1, 'Health Insurance Inc.', 'HII-12345678', '2020-01-01', '2025-12-31');

-- Insert data into MedicalHistory table
INSERT INTO MedicalHistory (history_id, patient_id, condition, diagnosed_on, treatment, notes)
VALUES (1, 1, 'Hypertension', '2015-08-20', 'Medication', 'Patient advised to reduce salt intake');

-- Insert data into Medications table
INSERT INTO Medications (medication_id, patient_id, name, dose, frequency, prescribed_by, start_date, end_date)
VALUES (1, 1, 'Lisinopril', '10mg', 'Once daily', 'Dr. Smith', '2015-08-21', 'Ongoing');

-- Insert data into Allergies table
INSERT INTO Allergies (allergy_id, patient_id, substance, reaction, severity, diagnosed_on)
VALUES (1, 1, 'Penicillin', 'Rash', 'Moderate', '2010-04-12');

-- Insert data into Appointments table
INSERT INTO Appointments (appointment_id, patient_id, date, time, doctor_name, doctor_specialty, doctor_phone, doctor_email, reason, notes)
VALUES (1, 1, '2023-06-10', '10:00:00', 'Dr. Smith', 'Cardiologist', '555-1111', 'dr.smith@hospital.com', 'Regular check-up', 'Blood pressure stable');

-- Insert data into LabResults table
INSERT INTO LabResults (lab_result_id, patient_id, test_name, test_date, result_data, doctor_name, doctor_specialty, doctor_phone, doctor_email, notes)
VALUES (1, 1, 'Complete Blood Count', '2023-05-15', '{"WBC": "5.5", "RBC": "4.7", "Hemoglobin": "14.0", "Hematocrit": "42%"}', 'Dr. Lee', 'Hematologist', '555-3333', 'dr.lee@hospital.com', 'All values within normal range');

-- Insert data into Procedures table
INSERT INTO Procedures (procedure_id, patient_id, procedure_name, date, surgeon_name, surgeon_specialty, surgeon_phone, surgeon_email, outcome, notes)
VALUES (1, 1, 'Appendectomy', '2010-06-15', 'Dr. Brown', 'General Surgeon', '555-4444', 'dr.brown@hospital.com', 'Successful', 'No complications');

-- Insert data into Immunizations table
INSERT INTO Immunizations (immunization_id, patient_id, vaccine, date_administered, administered_by, notes)
VALUES (1, 1, 'Influenza', '2023-09-15', 'Nurse Kelly', 'No adverse reactions');