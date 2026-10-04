import json
import os

current_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(current_dir, "utils", "user_queries.json"), "r") as file:
    queries = json.load(file)

class Users:

    """
        Model class to check existence of users and inserting new users into the database.

    """

    @staticmethod
    def insert_new_user(username, hashed_pw, school_year, cursor):
        cursor.execute(
            queries["insert_user_query"],
            (username, hashed_pw, school_year),
        )

    @staticmethod
    def check_existing_user(username, cursor):
        cursor.execute(
            queries["check_user_query"], (username,)
        )

        return cursor.fetchone()
