# Project Summary

## Project Name
Recruitment Funnel Analytics Pipeline

## Overview
This project is an end-to-end recruitment analytics workflow built using Azure services, SQL, and Python.

It starts with messy HR recruitment data in CSV format, stores the raw file in Azure Blob Storage, moves the data into Azure SQL Database using Azure Data Factory, cleans and standardizes the data in SQL through SSMS, and then uses the cleaned data for Python-based exploratory data analysis.

The main goal of the project is to study the recruitment funnel and understand applicant flow, stage-wise conversion, hiring source effectiveness, and time taken across the hiring process.

## Business Objective
The project was created to convert raw recruitment data into analysis-ready data and answer common hiring process questions such as:

- How many candidates entered the recruitment funnel?
- How many candidates were finally hired?
- Where do the biggest candidate drop-offs happen?
- Which recruitment sources contribute the most hires?
- How much time is taken at each hiring stage?

## Pipeline Summary
The project follows this workflow:

**Messy CSV → Azure Blob Storage → Azure Data Factory → Azure SQL Database → SQL Cleaning in SSMS → Python EDA**

This flow helped organize the project as both a data pipeline and an analytics project instead of only a Python analysis project.

## Data Preparation Work
The raw dataset required cleaning before analysis. The SQL cleaning process included:

- Standardizing null and placeholder values
- Trimming and formatting text fields
- Fixing inconsistent categorical values
- Converting date columns into proper date format
- Handling logically recoverable missing values
- Removing duplicate records
- Keeping the dataset ready for analysis

## Analysis Focus
The Python analysis mainly focused on:

- Total applicants
- Total hired candidates
- Hiring rate
- Recruitment funnel stage distribution
- Stage-to-stage conversion rates
- Hiring source effectiveness
- Average time spent at each stage

## Project Outcome
The project shows how recruitment data can be moved, cleaned, and analyzed through a simple cloud-based analytics pipeline.

It also helps demonstrate practical skills in Azure data movement, SQL data cleaning, and Python EDA using a realistic HR analytics use case.