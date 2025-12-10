import psycopg2
from ..config.db_connection import connect
from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)
from ..models.user import Users
from werkzeug.security import check_password_hash, generate_password_hash

def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        school_year = request.form.get('school_year') or None
        db = connect()
        cursor = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                hashed_pw = generate_password_hash(password)
                print(f"Username: {username}")
                print(f"Hashed password: {hashed_pw}")
                Users.insert_new_user(username, hashed_pw, school_year, cursor)
                db.commit()
            except psycopg2.IntegrityError:
                db.rollback()
                error = f"User {username} is already registered."
            except Exception as e:
                db.rollback()
                error = f"Error: {str(e)}"
            else:
                cursor.close()
                return redirect(url_for("auth.login"))

        flash(error)
        cursor.close()

    return render_template('auth/register.html')


def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect()
        cursor = db.cursor()
        error = None

        user = Users.check_existing_user(username, cursor)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            print(user[0])
            cursor.close()
            return redirect(url_for('index'))

        flash(error)
        cursor.close()

    return render_template('auth/login.html')

def logout():
    """clearing the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))