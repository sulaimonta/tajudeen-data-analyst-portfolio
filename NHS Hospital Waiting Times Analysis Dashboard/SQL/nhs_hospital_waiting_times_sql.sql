SELECT * FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT COUNT(*) AS Total_Patient  from nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT * FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT ROUND(AVG(Waiting_Days), 2) AS Average_Waiting_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT max(Waiting_Days) AS Maximum_Waiting_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT min(Waiting_Days) AS Minimum_Waiting_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT Target_Status, COUNT(*) AS Patient_Count FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned GROUP BY Target_Status;
SELECT ROUND(SUM(CASE WHEN Target_Status = 'Breached' THEN 1 ELSE 0 END),2) AS Breached_Patients FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT ROUND(SUM(CASE WHEN Target_Status = "Breached" THEN 1 ELSE 0 END) *100.0 / COUNT(*),2 ) AS Breach_Rate_Percentage FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned;
SELECT Specialty, COUNT(*) AS Patient_Count, ROUND(AVG(Waiting_Days), 2) AS Average_Waiting_Days, MAX(Waiting_Days) AS Maximum_Waiting_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned GROUP BY Specialty ORDER BY Average_Waiting_Days DESC;
SELECT Hospital, COUNT(*) AS Patient_Count, ROUND(AVG(Waiting_Days), 2) AS Average_Waiting_Days, ROUND(AVG(Breach_Days), 2) AS Average_Breach_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned GROUP BY Hospital ORDER BY Average_Waiting_Days DESC;
SELECT Priority, COUNT(*) AS Patient_Count, ROUND(AVG(Waiting_Days), 2) AS Average_Waiting_Days, ROUND(AVG(Breach_Days), 2) AS Average_Breach_Days FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned GROUP BY Priority ORDER BY Average_Waiting_Days DESC;
SELECT Outcome, COUNT(*) AS Patient_Count FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned GROUP BY Outcome;
SELECT Patient_ID, Specialty, Hospital, Priority, Waiting_Days, Target_Status FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned ORDER BY Waiting_Days DESC LIMIT 20;
CREATE VIEW hospital_waiting_summary AS
SELECT
    Hospital,
    COUNT(*) AS Total_Patients,
    ROUND(AVG(Waiting_Days), 2) AS Average_Waiting_Days,
    MAX(Waiting_Days) AS Maximum_Waiting_Days,
    MIN(Waiting_Days) AS Minimum_Waiting_Days,
    ROUND(SUM(CASE WHEN Target_Status = 'Breached' THEN 1 ELSE 0 END),2) AS Breached_Patients,
   ROUND(SUM(CASE WHEN Target_Status = "Breached" THEN 1 ELSE 0 END) *100.0 / COUNT(*),2 ) AS Breach_Rate_Percentage
FROM nhs_hospital_waiting_times.nhs_hospital_waiting_times_cleaned
GROUP BY Hospital;
SELECT *
FROM hospital_waiting_summary;