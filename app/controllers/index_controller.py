from flask import render_template, request, jsonify
from ..utils.helper import execute_qry
import json
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(current_dir, "utils", "index_queries.json"), "r") as file:
    queries = json.load(file)

def index():
    return render_template('index.html')

def search_page():
    """
    Search Page template displaying all department names
    """

    q = queries["department_name_query"]
    results = execute_qry(q,())
    departments =  [row[0] for row in results]
    return render_template("search.html", departments=departments)

def search():
    """
    search method that calls query in database to look up professors by name or by course. 
    """
    query = request.args.get("q", "").strip()
    mode = request.args.get("mode", "course")
    dept_filter = request.args.get("department", "all")
    sort_order = request.args.get("sort", "desc")

    if not query:
        return jsonify([])
    
    dept_param = None if dept_filter == "all" else dept_filter
    sort_asc = sort_order == "asc"

    if mode == "course":
        q = queries["procedure_call_1"]
    
    else: 
        q = queries["procedure_call_2"]
    
    results = execute_qry(q, (query, dept_param, sort_asc))

    formatted = []
    for prof in results:
        prof_data = {
            "first_name": prof[0],
            "last_name": prof[1],
            "rating": float(prof[2]) if prof[2] else 0,
        }
        
        formatted.append(prof_data)
            
    return jsonify(formatted)