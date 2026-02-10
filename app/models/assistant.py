import psycopg2
from tqdm import tqdm
from ..models.intructors import Instructor
from ..config.db_connection import connect
from ..utils.helper import validate_instructor
from ..utils.query_parser import  extract_two_prof_names
from sentence_transformers import SentenceTransformer
from ..models.context_pydantic import CourseContext, CourseRecommendationContext, ProfessorComparisonContext, ReviewContext, MiscellaneousInfoContext
from transformers import pipeline
from dotenv import load_dotenv
import json
import re


class AssistantRoles:
    """
        Model class to carry out all AI assistant related functionality by
            fetching relevant information from the database.

        Functionality includes:
            Generating consensus summary
            Recommending curriculum based on user preferences
            Answering miscellaneous questions
            Comparing two professors
    """

    def __init__(self):
        load_dotenv()
        with open("./app/utils/assistant_queries.json", "r") as file:
            self.assistant_queries = json.load(file)

        with open("./app/utils/prompts.json", "r") as file:
            self.prompts = json.load(file)
        self.model_id="meta-llama/Llama-3.2-1B-Instruct"
        self.system_prompt=self.prompts["system_prompt"]
        self.embedding_model = SentenceTransformer("google/embeddinggemma-300m")
        self.pipe = pipeline(
                "text-generation",
                model=self.model_id,
                dtype="auto",
                device_map="auto",
                )
        self.messages =[
            {"role": "system", "content": self.system_prompt}
        ]


    def get_database_results_for_relevant_reviews(self, cursor, user_query:str):
        query_embedding = self.embedding_model.encode_query(user_query)

        try:
            cursor.execute(self.assistant_queries["relevant_reviews_query"], ((query_embedding.tolist(),)))

            return cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(f"Error: {e}")
            return None


    def get_database_results_for_curriculum(self, cursor, user_query:str):

        query_embedding = self.embedding_model.encode_query(user_query)


        query = self.assistant_queries["curriculum_query"]
        try:
            cursor.execute(query, (query_embedding.tolist(),))
            courses = cursor.fetchall()
            return courses
        except psycopg2.ProgrammingError as e:
            print(f"Error: {e}")
            return None

    def get_database_results_for_profcomparison(self, cursor, prof1_fname:str, prof1_lname:str, prof2_fname:str, prof2_lname:str):


        try:
            cursor.execute(self.assistant_queries["prof_all_reviews_query"], (prof1_fname, prof1_lname))

            prof1_review_rows = cursor.fetchall()

            cursor.execute(self.assistant_queries["prof_course_info_query"], (prof1_fname, prof1_lname))

            prof1_courses = cursor.fetchall()


            cursor.execute(self.assistant_queries["prof_all_reviews_query"], (prof2_fname, prof2_lname))
            prof2_review_rows = cursor.fetchall()

            cursor.execute(self.assistant_queries["prof_course_info_query"], (prof2_fname, prof2_lname))
            prof2_courses = cursor.fetchall()


            return prof1_review_rows, prof1_courses, prof2_review_rows, prof2_courses

        except psycopg2.ProgrammingError as e:
            cursor.close()
            print(f"error: {e}")
            return None, None


    async def chat(self, messages: list[str]):


        self.messages.append(
            {"role": "user", "content": ("\n".join(messages))},
        )

        outputs = self.pipe(
            messages,
            max_new_tokens=900,
            temperature=0.1,
            return_full_text=False,
        )

        assistant_reply = outputs[0][-1]["generated_text"].strip()
        assistant_reply = re.sub(r'\*\*', '', assistant_reply)
        assistant_reply = re.sub(r'\*', '', assistant_reply)

        self.messages.append(
            {"role": "assistant", "content": assistant_reply},
        )
        print(assistant_reply)
        return assistant_reply

    def create_summary_prompt(self, contents: list[str]):
        messages = []

        messages.append(self.prompts["summary_prompt"])
        for content in contents[0]:
            messages.append(content)

        return messages

    async def generate_consensus_summary(self, instructor_first: str, instructor_last: str):
        conn = connect()
        try:
            comments = Instructor.get_all_comments_for_instructor(conn.cursor(), instructor_first, instructor_last)

            if not comments:
                return "No reviews yet"

            else:
                messages = self.create_summary_prompt(comments)

                result = await self.chat(messages)
                return result
        finally:
            conn.close()


    async def generate_summary_for_all_instructors(self,rows):
        results = []
        for row in tqdm(rows, total=len(rows)):
            result = await self.generate_consensus_summary(row[0], row[1])
            results.append({"first": row[0], "last": row[1], "summary": result})
        return results

    async def recommend_curriculum(self, cursor, user_query: str):

        database_results = self.get_database_results_for_curriculum(cursor, user_query)
        formatted_context = ""
        if not database_results:
            formatted_context += "No courses found related your field"
        else:
            course_contexts = [
                CourseContext(
                course_code=row[0],
                course_desc=row[1]
                )
                for row in database_results]


            context = CourseRecommendationContext(
                user_preferences=user_query,
                matching_courses=course_contexts,
            )

            formatted_context += context.format_for_llm()

        messages = [self.prompts["curriculum_prompt"].format(formatted_context=formatted_context)]


        return await self.chat(messages)

    async def QnA(self, cursor, user_query: str):

        relevant_reviews_rows = self.get_database_results_for_relevant_reviews(cursor, user_query)

        relevant_courses_rows = self.get_database_results_for_curriculum(cursor, user_query)

        if not relevant_reviews_rows:
            message = "no reviews yet"
            review_context = [ReviewContext(
                professor_fname=message,
                professor_lname=message,
                course_code=message,
                comment=message,
            )]
        else:
            review_context = [ReviewContext(
                professor_fname=row[0],
                professor_lname=row[1],
                course_code=row[2],
                comment=row[3]
            ) for row in relevant_reviews_rows]


        if not relevant_courses_rows:
            course_context = [CourseContext(
                course_code="no courses found",
                course_desc="no courses found"
            )]

        else:
            course_context = [CourseContext(
                course_code=row[0],
                course_desc=row[1]
            ) for row in relevant_courses_rows]


        context = MiscellaneousInfoContext(
            question=user_query,
            relevant_reviews=review_context,
            relevant_courses=course_context
        )

        formatted_context = context.format_for_llm()

        messages = [self.prompts["qna_prompt"].format(formatted_context=formatted_context)]


        return await self.chat(messages)


    async def compare_two_professors(self, cursor, user_query: str):

        prof_names = extract_two_prof_names(user_query)
        print(prof_names)

        prof1_fname, prof1_lname = validate_instructor(cursor, prof_names[0].title())
        prof2_fname, prof2_lname = validate_instructor(cursor, prof_names[1].title())

        print(prof1_fname, prof1_lname)
        print(prof2_fname, prof2_lname)


        prof1_review_rows, prof1_courses, prof2_review_rows, prof2_courses = self.get_database_results_for_profcomparison(cursor, prof1_fname, prof1_lname, prof2_fname, prof2_lname)


        if not prof1_courses:
            message = "no courses found for this professor"
            prof1_course_context = [CourseContext(
                course_code=message,
                course_desc=message,
            )]
        else:

            prof1_course_context = [CourseContext(
                course_code=course[0],
                course_desc=course[1],
            ) for course in prof1_courses]


        if not prof2_courses:
            message = "no courses found for this professor"
            prof2_course_context = [CourseContext(
                course_code=message,
                course_desc=message,
            )]
        else:

            prof2_course_context = [CourseContext(
                course_code=course[0],
                course_desc=course[1],
            ) for course in prof2_courses]

        if not prof1_review_rows:
            prof1_reviews = [
                ReviewContext(
                    professor_fname=prof1_fname,
                    professor_lname=prof1_lname,
                    course_code="N/A",
                    comment=f"No reviews for this professor or invalid professor {prof1_fname} {prof1_lname}"
                )
            ]
        else:
            prof1_reviews = [
                ReviewContext(
                    professor_fname=row[0],
                    professor_lname=row[1],
                    course_code=row[2],
                    comment=row[3]
                )
                for row in prof1_review_rows
            ]

        if not prof2_review_rows:

            prof2_reviews = [
                ReviewContext(
                    professor_fname=prof2_fname,
                    professor_lname=prof2_lname,
                    course_code="N/A",
                    comment=f"No reviews for this professor or invalid professor {prof2_fname} {prof2_lname}"
                )
            ]
        else:
            prof2_reviews = [
                ReviewContext(
                    professor_fname=row[0],
                    professor_lname=row[1],
                    course_code=row[2],
                    comment=row[3]
                )
                for row in prof2_review_rows
            ]
        context = ProfessorComparisonContext(
            professor1_fname=prof1_fname,
            professor2_fname=prof2_fname,
            professor1_courses=prof1_course_context,
            professor1_lname=prof1_lname,
            professor2_lname=prof2_lname,
            professor1_reviews=prof1_reviews,
            professor2_reviews=prof2_reviews,
            professor2_courses=prof2_course_context
        )

        formatted_context = context.format_for_llm()

        messages = [self.prompts["comparison_prompt"].format(formatted_context=formatted_context)]

        return await self.chat(messages)



