from flask import Flask
from onecode.config import Config
import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def app_create(config = Config):
    app = Flask(__name__)
    app.config.from_object(Config)  

    init_db()

    from onecode.main.routes import main

    app.register_blueprint(main)

    return app