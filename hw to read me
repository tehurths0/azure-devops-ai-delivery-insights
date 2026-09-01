# Azure DevOps AI Delivery Insights

System Analysis Proof of Concept (POC).

This project demonstrates how a delivery manager can ask natural-language questions about Azure DevOps delivery performance and receive executive-ready insights.

## Core Flow

Natural Language Question

↓

Intent Extraction

↓

Azure DevOps Data

↓

Delivery Metrics

↓

AI Gateway

↓

Executive Insights

↓

Recommendations


## Example

Manager asks:

"What has Team A completed in the last 60 days?"

The system produces:

- Completed work
- Delivery metrics
- Productivity indicators
- Risks
- Recommendations
- Executive summary


# Demo Modes

The application supports two data modes.


## 1. Demo Data

Uses the included:

data/sample_ado_data.csv

No credentials are required.

Recommended for:

- Manager demonstrations
- System Analysis presentations
- POC testing
- GitHub review


## 2. Client Azure DevOps

Uses the customer's existing Azure DevOps environment.

Required environment variables:

ADO_URL

ADO_PROJECT

ADO_PAT


# AI Modes

## Local Demo AI

The system generates deterministic delivery insights locally.

No AI API key is required.


## Client AI Gateway

The system connects to the customer's OpenAI-compatible AI Gateway.

Required:

AI_GATEWAY_URL

AI_GATEWAY_KEY

AI_MODEL


# Architecture


Manager

↓

Streamlit UI

↓

Natural Language Question

↓

Intent Parser

↓

ADO Data Source

↓

Metrics Engine

↓

AI Gateway

↓

Executive Report


# Repository Structure


azure-devops-delivery-insights/

├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── config/
│   └── config.py
│
├── src/
│   ├── ado_client.py
│   ├── query_parser.py
│   ├── metrics.py
│   ├── ai_gateway.py
│   └── report_generator.py
│
├── data/
│   └── sample_ado_data.csv
│
└── tests/
    └── test_metrics.py


# Installation

## Step 1

Clone the repository.


git clone <YOUR-GITHUB-REPOSITORY-URL>


## Step 2

Enter the repository.


cd azure-devops-delivery-insights


## Step 3

Create a Python virtual environment.


python -m venv .venv


## Step 4

Activate the environment.


### macOS / Linux


source .venv/bin/activate


### Windows


.venv\Scripts\activate


## Step 5

Install dependencies.


pip install -r requirements.txt


# Run Demo

Start Streamlit.


streamlit run app.py


Open:

http://localhost:8501


# Recommended First Test

Use:

Data Source:

Demo Data


AI Mode:

Local Demo AI


Question:

What has Team A completed in the last 60 days?


Click:

Analyse Delivery Performance


# Client Azure DevOps

Create a local `.env` file.

Example:


ADO_URL=https://dev.azure.com/your-organization

ADO_PROJECT=your-project

ADO_PAT=your-personal-access-token


The application uses Azure DevOps REST APIs to retrieve work-item data.


# Client AI Gateway

Add the customer's OpenAI-compatible Gateway configuration:


AI_GATEWAY_URL=https://your-ai-gateway.example.com/v1

AI_GATEWAY_KEY=your-secret-key

AI_MODEL=your-model


The application uses the configured Gateway instead of connecting directly to OpenAI.


# Security

Never commit:

.env

ADO_PAT

AI_GATEWAY_KEY

or any other credentials to GitHub.

The `.gitignore` file excludes `.env`.


# Testing

Run:


pytest -q


# POC Scope

This POC focuses on:

- Natural-language delivery questions
- Team identification
- Timeframe identification
- Azure DevOps work items
- Stories
- Bugs
- Tasks
- Features
- Epics
- Pull-request counts
- Cycle time
- Lead time
- Blocked work
- Priority
- Executive insights
- Recommendations


# Future Production Integration

The POC can later be extended with:

- Microsoft Entra ID
- Azure DevOps OAuth
- Azure DevOps Analytics API
- DORA metrics
- Deployment frequency
- Change failure rate
- Power BI
- Microsoft Teams
- PDF reporting
- Role-based access control
- Audit logging
- Enterprise secret management


# System Analysis Objective

The purpose of this POC is not to replace Azure DevOps.

The purpose is to demonstrate the system design:

Natural Language

→

Structured Intent

→

Delivery Data

→

Business Metrics

→

AI Interpretation

→

Management Action


This provides delivery managers with a faster way to understand delivery performance without manually creating reports or complex queries.
