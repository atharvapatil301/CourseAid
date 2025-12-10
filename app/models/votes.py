import json

with open("./app/utils/vote_queries.json", "r") as file:
    queries = json.load(file)

class Votes:
    """
        Model class to handle CRUD operations on the "votes" relation.
    """

    @staticmethod
    def create_vote(cursor, review_id, username, vote_type):
        insert_query = queries["insert_vote_query"]
        cursor.execute(insert_query, [review_id, username, vote_type])

    @staticmethod
    def count_votes(cursor, review_id):
        count_query = queries["count_votes_query"]
        cursor.execute(count_query, [review_id, review_id])
        return cursor.fetchone()

    @staticmethod
    def update_vote_id(cursor):
        cursor.execute(queries["update_voteid_query"])

    @staticmethod
    def check_vote(cursor, username, review_id):
        check_query = queries["check_vote_query"]
        cursor.execute(check_query, [review_id, username])
        return cursor.fetchone()


    @staticmethod
    def edit_vote(cursor, existing_vote_id, vote_type):
        update_query = queries["update_vote_query"]
        cursor.execute(update_query, [vote_type, existing_vote_id])


    @staticmethod
    def delete_vote(cursor, existing_vote_id):
        delete_query = queries["delete_vote_query"]
        cursor.execute(delete_query, [existing_vote_id])
