# CourseAid - Database Management Systems Project

## Introduction

Course selection can often feel overwhelming. As master's students, we frequently spend a lot of time researching and comparing courses to determine which ones will best enhance our learning experience. While platforms like Rate My Professor are commonly used to gather insights, they are primarily designed for searching specific professors rather than exploring courses holistically. The existing navigation and filters are also limited, making it difficult to obtain comprehensive and comparative information for students.

Our project aims to create a centralized hub for all course-related information. This application integrates objective course descriptions, student reviews, and perceptions of course difficulty based on the professor teaching the course. Additionally, it features robust filtering and search capabilities, enabling students to make more informed decisions when planning their academic paths.

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



### Database Logical Design



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


### Home Page
You can search by professor's name or course number. You can also select any departments as to filter from.


### Instructor profile
The profile shows instructor details along with the courses and departments that they are in. The instructor details contains a unique feature called consensus summary which is the summary of all the reviews of the instructor thus far and is updated every 20 reviews for that instructor.
This is followed by reviews of the instructor by other students. Here the user can upvote or downvote on a review.


## Instructor review from
This where the user can upload a new review


## User's past reviews
Here the user can view all their past reviews and choose to either edit or delete their review.


## Course Assistant
This is the AI assistant which runs using the RAG setup.
First, the intent from user query is identified after which the call goes to the right context builder whichbuilds relevant context by pulling data from database based on course_description embeddings and review embeddings.





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
