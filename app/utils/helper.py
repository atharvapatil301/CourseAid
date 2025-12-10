import json
import os
from functools import wraps
from flask import jsonify, session
import psycopg2
from ..config import db_connection
import re
from datetime import datetime, timezone

with open("./app/utils/helper_queries.json", "r") as file:
    queries = json.load(file)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Login required'}), 401
        return f(*args, **kwargs)

    return decorated_function

def execute_qry(sql_cmd, params):
    """
    This method is a helper function that helps execute a sql command with indicated parameters. 
    Can be used for insert, read, update, and delete assistant_queries
    """
    conn = db_connection.connect()
    cur = conn.cursor()
    try:
        cur.execute(sql_cmd, params)
        if sql_cmd.strip().upper().startswith(("INSERT")):
            if "RETURNING" in sql_cmd.upper():
                result = cur.fetchone()
                conn.commit()
                print("Insertion committed to the database.")
                return result[0] if result else None
            else:
                conn.commit()
                print("Insertion committed to the database.")
                return None
        elif sql_cmd.strip().upper().startswith(("UPDATE", "DELETE")):
            conn.commit()
            print("Changes committed to the database.")
            return cur.rowcount if cur.rowcount else None
        else:
                result = cur.fetchall()
                return result
    except psycopg2.Error as e:
        conn.rollback()
        print(f"failed to query: {e}")
        return None
    finally: 
        cur.close()
        conn.close()

def validate_instructor(cursor, instructor_name):

    instructor_first = instructor_name.split(" ")[0]
    instructor_last = instructor_name.split(" ")[-1]

    check_query = queries["validate_instructor_query"]
    cursor.execute(check_query, [instructor_first, instructor_last])
    valid_instructors = cursor.fetchall()
    if valid_instructors:
        return valid_instructors[0][0], valid_instructors[0][1]

    return None


def check_for_summary(instructor_first, instructor_last, last_timestamp):

    conn = db_connection.connect()
    cursor = conn.cursor()
    try:


        cursor.execute(queries["check_summary_query"], [instructor_first, instructor_last, last_timestamp])

        return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Error while calling summary procedure: {e}")
        cursor.close()
        conn.close()


def get_consensus_summary(instructor_first, instructor_last):
    BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILE = os.path.join(BASE_DIR, 'summary_cache.json')

    with open(CACHE_FILE, "r") as file:
        summary_cache = json.load(file)

    key = f"{instructor_first}_{instructor_last}"
    instructor_data = summary_cache["data"].get(key)
    if instructor_data:
        return instructor_data["summary"]
    return None


def update_summary_cache(instructor_first, instructor_last):

    from ..models.assistant import AssistantRoles
    try:

        deepseek = AssistantRoles()
        with open("./app/utils/summary_cache.json", "r") as file:
            summary_cache = json.load(file)

        key = f"{instructor_first}_{instructor_last}"
        instructor_data =  summary_cache["data"].get(key)
        if instructor_data:
            if(check_for_summary(instructor_first, instructor_last, instructor_data["last_timestamp"])):
                summary = deepseek.generate_consensus_summary(instructor_first, instructor_last)
                instructor_data["summary"] = summary
                print("Updated summary cache for instructor", instructor_first, instructor_last)
                instructor_data["last_timestamp"] = datetime.now(timezone.utc).isoformat()
            else:
                print(
                    f'Condition to update summary cache not satisfied for instructor {instructor_first, instructor_last}')

        else:
            print("Instructor does not exist", instructor_first,
                  instructor_last)

    except Exception as e:
        print(f"error updating summary for {instructor_first} {instructor_last}: {e}")



class IntentClassifier:
    """
        Helper class to call the right context builder based on the intent of user query.
    """

    @staticmethod
    def classify(user_query: str) -> str:

        query_lower = user_query.lower()


        pattern = r'(?:Professor |Prof\. |Prof |Dr\. |Dr )?[A-Z][a-z]+\s+[A-Z][a-z]+'
        professor_names = re.findall(pattern, user_query)

        comparison_keywords = ['compare', 'vs', 'versus', 'between', 'difference']
        has_comparison_keyword = any(keyword in query_lower for keyword in comparison_keywords)

        if has_comparison_keyword and len(professor_names) >= 2:
            print(f"[Intent Classifier] COMPARE detected: {professor_names}")
            return 'compare'


        curriculum_keywords = [
            'recommend courses', 'suggest courses', 'curriculum',
            'courses for', 'courses in', 'learning path',
            'what courses', 'which courses', 'study plan',
            'field of'
        ]


        field_indicators = [
            'machine learning', 'data science', 'artificial intelligence',
            'databases', 'software engineering', 'web development',
            'cybersecurity', 'algorithms', 'networking', 'ai', 'ml',
            'computer science', 'programming'
        ]

        has_curriculum_keyword = any(keyword in query_lower for keyword in curriculum_keywords)
        mentions_field = any(field in query_lower for field in field_indicators)

        if has_curriculum_keyword or mentions_field:
            print(f"[Intent Classifier] CURRICULUM detected")
            return 'curriculum'


        print(f"[Intent Classifier] QNA detected (default)")
        return 'qna'





