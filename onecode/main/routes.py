from flask import render_template, request, Blueprint, redirect, url_for, flash
from onecode import get_db_connection
import psycopg2

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert the feedback into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO feedbacks (name, email, message) VALUES (%s, %s, %s)',
                           (name, email, message))
            conn.commit()
            flash('Feedback submitted successfully!', 'success')
        except Exception as e:
            print(f"Error inserting data: {e}")  # Print the error for debugging
            flash('There was an error submitting your feedback.', 'danger')
           
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('main.contact'))

    return render_template("contact.html")


@main.route("/softs")
def soft():
    return render_template("softs.html")