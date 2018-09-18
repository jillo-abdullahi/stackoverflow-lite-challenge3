"""Module to create all relevant tables"""

from instance.config import conn


def migration():
    """
    Function to create database tables
    """
    cursor = conn.cursor()

    try:
        # delete tables if they already exist
        cursor.execute("DROP TABLE IF EXISTS users, questions, answers;")

        # create users table
        users = """CREATE TABLE users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(70) UNIQUE NOT NULL,
            password VARCHAR(250) NOT NULL,
            confirm_password VARCHAR(250) NOT NULL

        );"""

        # create questions table
        questions = """CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            date_created VARCHAR(50) NOT NULL,
            user_id INT references users(id)
        );"""

        # create answers table
        answers = """CREATE TABLE answers (
            id SERIAL PRIMARY KEY,
            description TEXT,
            date_created VARCHAR(50),
            question_id INT references questions(id),
            user_id INT references users(id),
            preferred BOOLEAN NOT NULL
        );"""

        cursor.execute(users)
        cursor.execute(questions)
        cursor.execute(answers)

        conn.commit()
        print("Tables successfully created")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL tables", error)


migration()
