# CourseAid - A better RateMyProfessor

## Introduction

Course selection can often feel overwhelming. As a master's student, I frequently spend a lot of time researching and comparing courses to determine which ones will best enhance our learning experience. While platforms like Rate My Professor are commonly used to gather insights, they are primarily designed for searching specific professors rather than exploring courses holistically. The existing navigation and filters are also limited, making it difficult to obtain comprehensive and comparative information for students.

This project aims to create a centralized hub for all course-related information. This application integrates objective course descriptions, student reviews, and perceptions of course difficulty based on the professor teaching the course. Additionally, it features robust filtering and search capabilities, enabling students to make more informed decisions when planning their academic paths.

## Technical Specifications

### Architecture
Full-stack application with SQL database utilizing:
- **Backend:** Flask (Python) for application logic
- **Database:** PostgreSQL (relational and vector storage with pgvector)
- **Embedding:** Gemma Embedding Model for reviews and course information
- **Database Hosting:** Amazon RDS (AWS)
- **Frontend:** HTML/CSS with Jinja2 Templates
- **AI Assistant:** Gemini API using "gemini-2.5-flash" model

### Technologies

**Languages:**
- Python (Backend)
- SQL (Database management)
- HTML/CSS (Frontend)

**Frameworks & Tools:**
- Flask - Web framework
- PostgreSQL & pgvector - Database and vector storage
- AWS RDS - Database hosting
- Huggingface
- [Gemma Embedding Model](https://huggingface.co/google/gemma-2b)
- [Gemini API](https://ai.google.dev/gemini-api)

### Database Design
The data is synthetically generated. All professors, courses, reviews and users are fake. The data revovles around only one university for now.

- **Total Tables:** 11
- **Features:** Complex SQL operations including JOINs, subqueries, aggregations, and CTEs
- **Schema:** Designed with foreign keys and constraints for data integrity

### Database Conceptual Design

<img width="1070" height="943" alt="Image" src="https://github.com/user-attachments/assets/8f9a089b-969e-4c33-9c0b-3fcf8deb0811" />


### Database Logical Design

<img width="843" height="770" alt="Image" src="https://github.com/user-attachments/assets/eb6e93dd-0f7a-4644-bafc-9513501f8fdd" />



## Prerequisites

Before running this project, ensure you have:
- Python 3.13+ installed
- Latest pip version
- API accounts and keys from:
  - Hugging Face
  - Gemini API
  - AWS

## Installation

### Step 1: Clone Repository
Open the repository in your IDE.

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs all required libraries including:
- Flask - Web framework
- psycopg2-binary - PostgreSQL database adapter
- huggingface-hub - Hugging Face API integration
- google-genai - Google Gemini API
- sentence-transformers - Text embeddings
- torch - PyTorch for ML models
- pgvector - Vector similarity search for PostgreSQL
- pandas - Data manipulation
- scikit-learn - Machine learning utilities

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory with the following credentials:
```env
DB_HOST=
DB_NAME=
DB_USER=
DB_PORT=
DB_PASSWORD=
SECRET_KEY=
HF_TOKEN=
GEMINI_API_KEY=
```

**Note:** Obtain a new HF token from [Hugging Face](https://huggingface.co/settings/tokens) and update the `.env` file.

## Running the Application

Once your development environment is set up, run:
```bash
python3 run.py
```
OR

```bash
flask run
```

The application will start and be accessible at: **http://localhost:5000** (or the port specified in your configuration)

## Walkthrough

### Login and Register
This is the login and register page for a returning or a new user.

<img width="1512" height="963" alt="Image" src="https://github.com/user-attachments/assets/ec739fb1-791a-46a5-9131-a94c04ba7e9c" />

<img width="1512" height="942" alt="Image" src="https://github.com/user-attachments/assets/42c2daf5-12a8-4e65-a6dd-2c461ac857a1" />



### Home Page
You can search by professor's name or course number. You can also select any departments as to filter from.

<img width="1512" height="944" alt="Image" src="https://github.com/user-attachments/assets/cfc6d3b9-393f-4df5-b26c-eb029e4ab104" />


### Instructor profile
The profile shows instructor details along with the courses and departments that they are in. The instructor details contains a unique feature called consensus summary which is the summary of all the reviews of the instructor thus far and is updated every 20 reviews for that instructor.
This is followed by reviews of the instructor by other students. Here the user can upvote or downvote on a review.

<img width="1512" height="945" alt="Image" src="https://github.com/user-attachments/assets/66cd855f-49e3-4bb0-bbc4-9e304281f561" />


## Instructor review from
This where the user can upload a new review

<img width="1511" height="945" alt="Image" src="https://github.com/user-attachments/assets/97d201c7-93b0-47df-ae35-5f72586a5712" />

## User's past reviews
Here the user can view all their past reviews and choose to either edit or delete their review.

<img width="1512" height="945" alt="Image" src="https://github.com/user-attachments/assets/b8db0698-1b83-4713-a1eb-ea7c80c1dcda" />


## Course Assistant
This is the AI assistant which runs using the RAG setup.
First, the intent from user query is identified after which the call goes to the right context builder whichbuilds relevant context by pulling data from database based on course_description embeddings and review embeddings.

<img width="1512" height="944" alt="Image" src="https://github.com/user-attachments/assets/f33c9766-e62e-44f5-b0a5-9402f89c489a" />



## Troubleshooting

### Common Issues

**1. "HF_TOKEN is expired" error**
- Generate a new token at https://huggingface.co/settings/tokens
- Update the `HF_TOKEN` in your `.env` file

**2. "ModuleNotFoundError" error**
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt` again

## Features

- **Semantic Search:** Vector-based search using embeddings for reviews and course descriptions for relevant course discovery
- **AI Assistant:** RAG-powered chatbot for course recommendations and comparisons
- **Advanced Filtering:** Robust search and filter capabilities
- **User Reviews:** Student-generated reviews and difficulty ratings
- **Professor Insights:** Course difficulty based on instructors


## Future Work

Planned enhancements include:

- Admin role implementation for managing courses, sections, and professors
- Real data scraping for courses, instructors, and reviews
- Automated semester updates for course information
- Caching mechanisms (KV caching for assistant, Redis integration to store consensus summaries)
- Multi-university database scaling
- Integrating LLM council into RAG for generating and validating response from multiple LLMs
- Enhanced embedding for professor profiles and additional metadata


---
