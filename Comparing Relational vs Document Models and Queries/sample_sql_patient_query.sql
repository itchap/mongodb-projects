SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    p.dob,
    p.gender,
    p.ssn,
    p.marital_status,
    c.email AS contact_email,
    c.phone AS contact_phone,
    c.street AS contact_street,
    c.city AS contact_city,
    c.state AS contact_state,
    c.zip AS contact_zip,
    c.country AS contact_country,
    e.name AS emergency_contact_name,
    e.relationship AS emergency_contact_relationship,
    e.phone AS emergency_contact_phone,
    e.email AS emergency_contact_email,
    e.street AS emergency_contact_street,
    e.city AS emergency_contact_city,
    e.state AS emergency_contact_state,
    e.zip AS emergency_contact_zip,
    e.country AS emergency_contact_country,
    i.provider AS insurance_provider,
    i.policy_number AS insurance_policy_number,
    i.valid_from AS insurance_valid_from,
    i.valid_until AS insurance_valid_until,
    mh.condition AS medical_history_condition,
    mh.diagnosed_on AS medical_history_diagnosed_on,
    mh.treatment AS medical_history_treatment,
    mh.notes AS medical_history_notes,
    m.name AS medication_name,
    m.dose AS medication_dose,
    m.frequency AS medication_frequency,
    m.prescribed_by AS medication_prescribed_by,
    m.start_date AS medication_start_date,
    m.end_date AS medication_end_date,
    a.substance AS allergy_substance,
    a.reaction AS allergy_reaction,
    a.severity AS allergy_severity,
    a.diagnosed_on AS allergy_diagnosed_on,
    ap.date AS appointment_date,
    ap.time AS appointment_time,
    ap.doctor_name AS appointment_doctor_name,
    ap.doctor_specialty AS appointment_doctor_specialty,
    ap.doctor_phone AS appointment_doctor_phone,
    ap.doctor_email AS appointment_doctor_email,
    ap.reason AS appointment_reason,
    ap.notes AS appointment_notes,
    lr.test_name AS lab_result_test_name,
    lr.test_date AS lab_result_test_date,
    lr.result_data AS lab_result_result_data,
    lr.doctor_name AS lab_result_doctor_name,
    lr.doctor_specialty AS lab_result_doctor_specialty,
    lr.doctor_phone AS lab_result_doctor_phone,
    lr.doctor_email AS lab_result_doctor_email,
    lr.notes AS lab_result_notes,
    pr.procedure_name AS procedure_name,
    pr.date AS procedure_date,
    pr.surgeon_name AS procedure_surgeon_name,
    pr.surgeon_specialty AS procedure_surgeon_specialty,
    pr.surgeon_phone AS procedure_surgeon_phone,
    pr.surgeon_email AS procedure_surgeon_email,
    pr.outcome AS procedure_outcome,
    pr.notes AS procedure_notes,
    im.vaccine AS immunization_vaccine,
    im.date_administered AS immunization_date_administered,
    im.administered_by AS immunization_administered_by,
    im.notes AS immunization_notes
FROM
    Patients p
    LEFT JOIN ContactDetails c ON p.patient_id = c.patient_id
    LEFT JOIN EmergencyContacts e ON p.patient_id = e.patient_id
    LEFT JOIN InsuranceDetails i ON p.patient_id = i.patient_id
    LEFT JOIN MedicalHistory mh ON p.patient_id = mh.patient_id
    LEFT JOIN Medications m ON p.patient_id = m.patient_id
    LEFT JOIN Allergies a ON p.patient_id = a.patient_id
    LEFT JOIN Appointments ap ON p.patient_id = ap.patient_id
    LEFT JOIN LabResults lr ON p.patient_id = lr.patient_id
    LEFT JOIN Procedures pr ON p.patient_id = pr.patient_id
    LEFT JOIN Immunizations im ON p.patient_id = im.patient_id
WHERE
    p.patient_id = 1;