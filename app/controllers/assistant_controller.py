import os
from flask import request, jsonify, render_template
from ..models.assistant import AssistantRoles
import asyncio
from ..utils.helper import IntentClassifier


assistant_roles = AssistantRoles()

def get_assistant():

    return render_template("assistant.html")


def answer_question(conn):

    try:

        cursor = conn.cursor()

        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided'
            }), 400

        user_message = data['message'].strip()

        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400


        intent_hint = data.get('intent_hint', None)


        print(f"\n{'=' * 60}")
        print(f"[USER QUERY]: {user_message}")
        if intent_hint:
            print(f"[INTENT HINT from frontend]: {intent_hint}")
        print(f"{'=' * 60}")


        if intent_hint and intent_hint in ['compare', 'curriculum', 'qna']:
            intent = intent_hint
            print(f"[USING HINT]: {intent}")
        else:
            intent = IntentClassifier.classify(user_message)
            print(f"[CLASSIFIED INTENT]: {intent}")


        if intent == 'compare':
            print("[ROUTING TO]: compare_two_professors")
            response = asyncio.run(assistant_roles.compare_two_professors(cursor,user_message))

        elif intent == 'curriculum':
            print("[ROUTING TO]: recommend_curriculum")
            response = asyncio.run(assistant_roles.recommend_curriculum(cursor,user_message))

        else:
            print("[ROUTING TO]: QnA")
            response = asyncio.run(assistant_roles.QnA(cursor,user_message))


        return jsonify({
            'response': response,
            'intent': intent
        }), 200

    except Exception as e:
        print(f"[ERROR in answer_question]: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'An error occurred processing your request',
            'details': str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()





