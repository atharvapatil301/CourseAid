import psycopg2
from ..utils.helper import validate_instructor
import json

with open("./app/utils/instructor_queries.json") as json_file:
    queries = json.load(json_file)

class Instructor:
    """
        Model class to fetch relevant Instructor information from the database
    """

    @staticmethod
    def get_average_rating(cursor, instructor_name):
        instructor_first, instructor_last = validate_instructor(cursor, instructor_name)

        avg_query = queries["avg_rating_query"]
        try:
            cursor.execute(avg_query, (instructor_first, instructor_last))

            avg_rating = cursor.fetchall()[0][0]
            if avg_rating:
                return avg_rating
            return None
        except psycopg2.ProgrammingError as e:
            raise Exception(f"{e}")

    @staticmethod
    def get_courses_of_instructor(cursor, instructor_name):
        instructor_first, instructor_last = validate_instructor(cursor, instructor_name)

        courses_of_instructor_query = queries["instructor_courses_query"]

        try:
            cursor.execute(courses_of_instructor_query, (instructor_first, instructor_last))
            rows = cursor.fetchall()
            courses_of_instructor = [row[0] for row in rows]
            return courses_of_instructor
        except psycopg2.ProgrammingError as e:
            raise Exception(f"{e}")

    @staticmethod
    def get_departments_of_instructor(cursor, instructor_name):

        instructor_first, instructor_last = validate_instructor(cursor, instructor_name)

        departments_of_instructor_query = queries["instructor_departments_query"]

        try:
            cursor.execute(departments_of_instructor_query, (instructor_first, instructor_last))
            rows = cursor.fetchall()
            departments_of_instructor = [row[0] for row in rows]
            return departments_of_instructor
        except psycopg2.ProgrammingError as e:
            raise Exception(f"{e}")


    @staticmethod
    def get_all_comments_for_instructor(cursor, instructor_first, instructor_last):
        all_reviews = queries["instructor_reviews_query"]

        try:
            cursor.execute(all_reviews, [instructor_first, instructor_last])
            comments = cursor.fetchall()
            if len(comments) == 0:
                return None

            else:
                return comments

        except psycopg2.Error as e:
            raise Exception(f"Error fetching reviews: {e}")


