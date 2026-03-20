/*
================================================================================
SQL Data Cleaning Project: HR Recruitment Dataset
Author: Riya Manoj Patil
Purpose: Clean and standardize "Messy_HR_Recruitment_Data" for Funnel Analysis
Tasks: Trim whitespaces, remove corrupt characters (", --), standardize casing,  
       deduplicating rows and handle inconsistent NULL values with logical data
       imputation
================================================================================
*/


-- 1. Preview the Messy Data
SELECT TOP 100 * FROM HR_Recruitment;


-- 2. Standardize NULL placeholders
-- Replacing string variations like 'N/A', '#N/A', and 'NULL' with actual SQL NULLs
UPDATE HR_Recruitment
SET 
    CandidateID = CASE WHEN TRIM(CandidateID) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE CandidateID END,
    PositionID = CASE WHEN TRIM(PositionID) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE PositionID END,
    JobTitle = CASE WHEN TRIM(JobTitle) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE JobTitle END,
    ApplicationDate = CASE WHEN TRIM(ApplicationDate) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE ApplicationDate END,
    Source = CASE WHEN TRIM(Source) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE Source END,
    Stage = CASE WHEN TRIM(Stage) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE Stage END,
    DateatStage = CASE WHEN TRIM(DateatStage) IN ('N/A', '#N/A', 'NULL', '') THEN NULL ELSE DateatStage END;


-- 3. Data Cleaning Transformation
-- Begin the Data Cleaning Process
BEGIN TRANSACTION T1;


-- Clean CandidateID & PositionID
-- Removing double quotes, fixing double hyphens, and trimming whitespace
UPDATE HR_Recruitment
SET 
    CandidateID = UPPER(TRIM(REPLACE(REPLACE(CandidateID, '"', ''), '--', '-'))),
    PositionID = UPPER(TRIM(REPLACE(REPLACE(PositionID, '"', ''), '--', '-')))
WHERE CandidateID IS NOT NULL OR PositionID IS NOT NULL;


-- Clean JobTitle
-- Standardizing Jobtitle to UPPERCASE for consistent grouping
UPDATE HR_Recruitment
SET JobTitle = UPPER(TRIM(REPLACE(JobTitle, '"', '')))
WHERE JobTitle IS NOT NULL;


-- Clean Source & Stage
-- Standardizing casing of categorical columns
UPDATE HR_Recruitment
SET 
    Source = UPPER(TRIM(REPLACE(Source, '"', ''))),
    Stage = UPPER(TRIM(REPLACE(Stage, '"', '')))
WHERE Source IS NOT NULL OR Stage IS NOT NULL;


-- Clean Date Columns (ApplicationDate & DateatStage)
UPDATE HR_Recruitment
SET 
    ApplicationDate = TRIM(REPLACE(REPLACE(ApplicationDate, '"', ''), '--', '-')),
    DateatStage = TRIM(REPLACE(REPLACE(DateatStage, '"', ''), '--', '-'))
WHERE ApplicationDate IS NOT NULL OR DateatStage IS NOT NULL;



-- Convert Date Columns to Proper DATE Datatype
ALTER TABLE HR_Recruitment
ALTER COLUMN ApplicationDate DATE;

ALTER TABLE HR_Recruitment
ALTER COLUMN DateatStage DATE;


-- Validate Columns Data Types
-- Verify that ALTER TABLE commands successfully converted columns to the intended data types
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    CHARACTER_MAXIMUM_LENGTH AS Max_Length,
    IS_NULLABLE AS Is_Nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'HR_Recruitment';



-- If whatever you have changed looks correct, run: COMMIT;
-- If you made a mistake, run: ROLLBACK;
COMMIT;



-- 4. LOGICAL NULL HANDLING
-- Instead of deleting rows with missing values, we use business logic to fill them

-- TRANSACTION 2 (T2) For LOGICAL DATA RECOVERY & IMPUTATION
BEGIN TRANSACTION T2;


-- Fill ApplicationDate if it's missing but we have a 'DateatStage' for 'APPLIED'
UPDATE HR_Recruitment
SET ApplicationDate = DateatStage
WHERE ApplicationDate IS NULL 
  AND Stage = 'APPLIED' 
  AND DateatStage IS NOT NULL;



-- Fill DateatStage using ApplicationDate
-- If a candidate is still in the 'APPLIED' stage and DateatStage is missing,
-- it is logically the same as the ApplicationDate.
UPDATE HR_Recruitment
SET DateatStage = ApplicationDate
WHERE DateatStage IS NULL 
  AND ApplicationDate IS NOT NULL
  AND Stage = 'APPLIED';


-- If ApplicationDate is missing but they are already at 'SCREENED' or 'INTERVIEW',
-- we know they must have applied ON or BEFORE that date so we use the DateatStage as a conservative estimate for the ApplicationDate.
UPDATE HR_Recruitment
SET ApplicationDate = DateatStage
WHERE ApplicationDate IS NULL 
  AND DateatStage IS NOT NULL;



UPDATE HR_Recruitment
SET JobTitle = 'REGIONAL SALES'
WHERE JobTitle = 'REGIONALSALES';


-- Fill Missing JobTitle using PositionID
-- We use a CTE to find the most frequent Title for each PositionID
WITH PositionMapping AS (
    SELECT 
        PositionID, 
        JobTitle,
        ROW_NUMBER() OVER (PARTITION BY PositionID ORDER BY COUNT(*) DESC) as RankNum
    FROM HR_Recruitment
    WHERE PositionID IS NOT NULL AND JobTitle IS NOT NULL
    GROUP BY PositionID, JobTitle
)
UPDATE t1
SET t1.JobTitle = m.JobTitle
FROM HR_Recruitment t1
JOIN PositionMapping m ON t1.PositionID = m.PositionID
WHERE t1.JobTitle IS NULL AND m.RankNum = 1;



-- Fill Missing PositionID using JobTitle
-- We fill PositionID with the ID that appeared most frequently
WITH FrequencyMapping AS (
    SELECT 
        JobTitle, 
        PositionID,
        -- Count how many times each ID appears for each Title
        ROW_NUMBER() OVER (PARTITION BY JobTitle ORDER BY COUNT(*) DESC) as RankNum
    FROM HR_Recruitment
    WHERE JobTitle IS NOT NULL AND PositionID IS NOT NULL
    GROUP BY JobTitle, PositionID
)
UPDATE t1
SET t1.PositionID = f.PositionID
FROM HR_Recruitment t1
JOIN FrequencyMapping f ON t1.JobTitle = f.JobTitle
WHERE t1.PositionID IS NULL 
  AND f.RankNum = 1;


-- Assigning placeholders to the remaining 125 rows missing both JobTitle and PositionID 
UPDATE HR_Recruitment
SET 
    JobTitle = COALESCE(JobTitle, 'NOT SPECIFIED'),
    PositionID = COALESCE(PositionID, 'POS-UNKNOWN');


-- Fill missing values of Source as 'OTHER'
UPDATE HR_Recruitment
SET Source = 'OTHER'
WHERE Source = 'UNKNOWN';

-- Fill Null values of Stage column as 'UNKNOWN'
UPDATE HR_Recruitment
SET Stage = 'UNKNOWN'
WHERE Stage IS NULL;


-- Delete null values where values cannot be filled by any logical imputation

-- Delete rows where dates are missing
-- If we cannot use logical imputing we simply delete those missing values rows
DELETE FROM HR_Recruitment
WHERE ApplicationDate IS NULL 
  OR DateatStage IS NULL;


-- Delete Null Values of CandidateID
-- Rows with NULL CandidateIDs are considered 'junk data'
DELETE FROM HR_Recruitment
WHERE CandidateID IS NULL;


-- Verify if any NULLs remaining in the columns
SELECT 
    SUM(CASE WHEN CandidateID IS NULL THEN 1 ELSE 0 END) AS CandidateID_Nulls,
    SUM(CASE WHEN PositionID IS NULL THEN 1 ELSE 0 END) AS PositionID_Nulls,
    SUM(CASE WHEN JobTitle IS NULL THEN 1 ELSE 0 END) AS JobTitle_Nulls,
    SUM(CASE WHEN ApplicationDate IS NULL THEN 1 ELSE 0 END) AS AppDate_Nulls,
    SUM(CASE WHEN Source IS NULL THEN 1 ELSE 0 END) AS Source_Nulls,
    SUM(CASE WHEN Stage IS NULL THEN 1 ELSE 0 END) AS Stage_Nulls,
    SUM(CASE WHEN DateatStage IS NULL THEN 1 ELSE 0 END) AS DateAtStage_Nulls
FROM HR_Recruitment;


-- Deduplication - Delete duplicate records from the data

-- Create a CTE to identify duplicates
-- Assign a RowNumber '1' is the original, '2' and above are duplicates
-- Deleting duplicate rows from the data
WITH Deduplicating AS (
    SELECT 
        CandidateID, 
        PositionID, 
        JobTitle, 
        Source, 
        Stage,
        ROW_NUMBER() OVER (PARTITION BY CandidateID, PositionID, JobTitle, Source, Stage
                            ORDER BY CandidateID 
        ) AS DuplicateCount
    FROM HR_Recruitment
)
DELETE FROM Deduplicating
WHERE DuplicateCount > 1;


-- Final Validation of the Data
SELECT * FROM HR_Recruitment;


-- If everything looks correct, run: COMMIT;
-- If you made a mistake, run: ROLLBACK;
COMMIT;