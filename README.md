# AI Resume Screening & Candidate Ranking System

## Overview

The AI Resume Screening & Candidate Ranking System is an intelligent recruitment assistant that automates resume analysis and candidate evaluation. It helps recruiters reduce manual screening time by extracting candidate information, comparing resumes with job descriptions, calculating ATS scores, and ranking candidates based on their suitability for a role.

The system combines Natural Language Processing (NLP), semantic similarity using Sentence Transformers, and rule-based skill matching to provide accurate candidate rankings.

---

# Features

* Upload resumes in PDF and DOCX formats
* Upload or paste Job Descriptions (JD)
* Extract candidate information (Name, Email, Phone Number)
* Extract technical and soft skills
* Calculate ATS compatibility score
* Display matched and missing skills
* Rank multiple candidates against one or more job descriptions
* Email high-ranking candidates directly from the interface
* Store candidate information using MongoDB (optional persistence)

---

# Tech Stack

## Backend

* Python
* FastAPI

## Frontend

* Streamlit

## Database

* MongoDB

## NLP & AI

* spaCy
* Sentence Transformers (`all-MiniLM-L6-v2`)
* Regular Expressions

## Resume Parsing

* pdfplumber
* python-docx

---

# System Architecture

```
Recruiter
     │
     ▼
Streamlit Frontend
     │
     ▼
FastAPI Backend
     │
     ├──────────────► Resume Parser
     │                   │
     │                   ▼
     │            Extract Resume Text
     │
     ├──────────────► Candidate Information Extraction
     │                   │
     │                   ▼
     │        Name, Email, Phone, Skills
     │
     ├──────────────► AI Matching Engine
     │                   │
     │                   ├── Semantic Similarity
     │                   ├── Skill Matching
     │                   └── ATS Score Calculation
     │
     ├──────────────► Candidate Ranking
     │
     ├──────────────► MongoDB (Optional Storage)
     │
     ▼
Results Dashboard
```

---

# Data Flow

## Step 1 – Upload Resume

The recruiter uploads one or more resumes through the Streamlit interface.

Supported formats:

* PDF
* DOCX

The files are sent to the FastAPI backend using HTTP POST requests.

---

## Step 2 – Resume Parsing

The backend detects the file type.

For PDF files:

* pdfplumber extracts text page by page.

For DOCX files:

* python-docx extracts text from document paragraphs.

The extracted text becomes the input for NLP processing.

---

## Step 3 – Candidate Information Extraction

The system extracts:

* Candidate Name
* Email Address
* Phone Number
* Skills

Extraction techniques:

* Regular Expressions for Email and Phone Number
* spaCy Named Entity Recognition (NER) for candidate name
* Rule-based skill lookup using a predefined skill database

---

## Step 4 – Job Description Processing

The uploaded or pasted Job Description is cleaned and preprocessed.

Required skills are identified using the same skill database used for resume analysis.

---

## Step 5 – Semantic Similarity

The resume text and job description are converted into embeddings using the Sentence Transformer model:

```
all-MiniLM-L6-v2
```

The embeddings are compared using cosine similarity to determine how closely the resume matches the overall meaning and context of the job description.

This generates the **Semantic Score**.

---

## Step 6 – Skill Matching

The extracted candidate skills are compared with the required skills from the Job Description.

Example:

Required Skills:

```
Java
SQL
Spring Boot
Git
```

Candidate Skills:

```
Java
SQL
Git
Python
```

Matched Skills:

```
Java
SQL
Git
```

Skill Match Percentage:

```
Matched Skills / Required Skills × 100
```

This generates the **Skill Match Score**.

---

## Step 7 – ATS Score Calculation

The final ATS score combines semantic similarity and exact skill matching.

```
ATS Score =
(0.60 × Semantic Score)
+
(0.40 × Skill Match Score)
```

### Why 60:40?

* Semantic similarity receives higher weight because candidates often describe experience using different wording than the job description.
* Skill matching ensures that mandatory technologies and tools required for the role are also considered.

This balance helps improve candidate ranking while avoiding over-reliance on exact keyword matching.

---

## Step 8 – Candidate Ranking

For bulk screening:

* Multiple resumes are compared with one or more Job Descriptions.
* ATS scores are calculated for every candidate.
* Candidates are sorted in descending order of ATS score.

Recruiters receive a ranked list of candidates based on suitability.

---

## Step 9 – Results

The recruiter can view:

* Candidate Name
* Email
* Phone Number
* ATS Score
* Matching Skills
* Missing Skills
* Candidate Ranking

If the ATS score exceeds the configured threshold and an email is available, the system provides an **Email Candidate** option.

---

# API Endpoints

## Upload Resume

```
POST /upload_resume
```

Uploads and parses resume files.

---

## Resume Matching

```
POST /match_resume
```

Compares a single resume against a single job description.

---

## Bulk Ranking

```
POST /bulk_rank
```

Ranks multiple resumes against one or more job descriptions.

---

# MongoDB Usage

MongoDB is used to store candidate-related information for future retrieval.

Example stored fields include:

* Candidate Name
* Email
* Phone Number
* Skills
* ATS Score
* Resume Metadata

MongoDB was selected because resume data is semi-structured and varies between candidates, making a document-oriented database a suitable choice.

---

# Future Improvements

* User Authentication
* Resume Database Search
* OCR Support for Scanned PDFs
* Dynamic Skill Database
* Recruiter Dashboard
* Interview Scheduling
* Feedback Analytics
* AI-powered Resume Recommendations

---

# Conclusion

The AI Resume Screening & Candidate Ranking System demonstrates how Natural Language Processing and semantic similarity can automate recruitment workflows. By combining resume parsing, skill extraction, semantic analysis, and ATS scoring, the system assists recruiters in identifying the most suitable candidates efficiently while reducing manual effort.
