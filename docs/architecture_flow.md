# Architecture Flow

## Project Workflow
This project follows a simple end-to-end data pipeline for recruitment analytics:

**Messy CSV → Azure Blob Storage → Azure Data Factory → Azure SQL Database → SQL Cleaning in SSMS → Python EDA**

## Step-by-Step Flow

### 1. Raw Recruitment Data
The project started with messy HR recruitment data in CSV format.

The raw data included applicant and hiring-stage related fields such as candidate details, job roles, application dates, recruitment sources, and funnel stages.

### 2. Azure Blob Storage
The raw CSV file was uploaded to Azure Blob Storage.

This served as the cloud storage layer for the source data before pipeline movement.

### 3. Azure Data Factory
Azure Data Factory was used to move the raw data from Azure Blob Storage into Azure SQL Database.

This step created a simple cloud-based data ingestion workflow.

### 4. Azure SQL Database
The raw recruitment data was stored in Azure SQL Database.

This database became the central layer for structured storage and further cleaning.

### 5. SQL Data Cleaning in SSMS
The dataset was cleaned in SQL using SSMS.

The cleaning work included:
- handling null and placeholder values
- standardizing text fields
- fixing inconsistent values
- converting date columns
- logically filling recoverable missing values
- removing duplicates

This step prepared the dataset for reliable analysis.

### 6. Python EDA
After cleaning, the prepared data was used in Python through Jupyter Notebook for exploratory data analysis.

The analysis focused on:
- applicant volume
- hired candidates
- funnel stage distribution
- conversion rates
- source effectiveness
- average time at each stage

## Architecture Purpose
This workflow shows how raw recruitment data can move through cloud storage, pipeline ingestion, SQL-based cleaning, and Python analysis in a structured way.

It makes the project stronger than a basic analysis notebook because it also demonstrates practical data pipeline and cloud handling steps.