"""module for all models of the application"""
import psycopg2

from instance.config import conn


class User(object):
    """
    Class representing users
    """

    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def register_user(self):
        """
        Instance method to create new user
        """
        try:
            cursor = conn.cursor()
            query = """ INSERT INTO users (username, email, password, confirm_password) VALUES (%s, %s, %s, %s) """
            cursor.execute(query, (self.username, self.email,
                                   self.password, self.confirm_password))
            conn.commit()
            return "User successcully added to database"

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed inserting record into user table {}".format(error)
        finally:
                # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"

    def get_users(self):
        """
        Instance method to get all users
        """
        try:
            cursor = conn.cursor()
            query = """ SELECT * FROM users """
            cursor.execute(query)
            all_users = cursor.fetch_all()

            results = []
            for user in all_users:
                details = {}
                details["user_id"] = user[0]
                details["username"] = user[1]
                details["email"] = user[2]
                details["password"] = user[3]
                details["confirm_password"] = user[4]
                results.append(details)

            return results

        except (Exception, psycopg2.DatabaseError) as error:
            return "Failed fetching record from users table {}".format(error)

        finally:
            # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                print "PostgresSQL connection closed"


class Question(object):
    """
    Class representing questions
    """

    def __init__(self, title, description, user_id, date_created):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date_created = date_created

    def post_question(self):
        """
        Instance method to create new user
        """
        try:
            cursor = conn.cursor()
            query = """ INSERT INTO users (title, description, date_created, user_id) VALUES (%s, %s, %s, %s) """
            cursor.execute(query, (self.title, self.description,
                                   self.date_created, self.user_id))
            conn.commit()
            return "Question successcully added to database"

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed inserting record into questions table {}".format(error)
        finally:
                # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"

    def get_all_questions(self):
        """
        Instance method to get all questions
        """
        try:
            cursor = conn.cursor()
            query = """ SELECT * FROM questions """
            cursor.execute(query)
            all_questions = cursor.fetch_all()

            results = []
            for question in all_questions:
                details = {}
                details["question_id"] = question[0]
                details["title"] = question[1]
                details["description"] = question[2]
                details["date_created"] = question[3]
                details["user_id"] = question[4]
                results.append(details)

            return results

        except (Exception, psycopg2.DatabaseError) as error:
            return "Failed fetching record from questions table {}".format(error)

        finally:
            # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"

    def get_one_question(self, qn_id):
        """
        Instance method to fetch a specific question
        """
        try:
            cursor = conn.cursor()
            query = """ SELECT * FROM questions WHERE id=%s; """
            cursor.execute(query, [qn_id])
            question = cursor.fetch_one()

            details = {}
            details["question_id"] = question[0]
            details["title"] = question[1]
            details["description"] = question[2]
            details["date_created"] = question[3]
            details["user_id"] = question[4]

            return details

        except (Exception, psycopg2.DatabaseError) as error:
            return "Failed fetching record from questions table {}".format(error)

        finally:
            # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"

    def delete_question(self, qn_id):
        """
        Instance method to delete a question
        """
        try:
            cursor = conn.cursor()
            query = """ DELETE FROM questions WHERE id=%s """
            cursor.execute(query, [qn_id])
            conn.commit()
            return "Question successcully deleted from database"

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed to delete question {}".format(error)
        finally:
                # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"


class Answer(object):
    """
    Class representing answers
    """

    def __init__(self, description, date_created, user_id, question_id, preferred=False):
        self.description = description
        self.user_id = user_id
        self.date_created = date_created
        self.preferred = preferred

    def post_answer(self):
        """
        Instance method to post answer
        """
        try:
            cursor = conn.cursor()
            query = """ INSERT INTO answers (description, date_created, user_id, question_id, preferred) VALUES (%s, %s, %s, %s, %s) """
            cursor.execute(query, (self.description, self.date_created,
                                   self.user_id, self.date_created, self.preferred))
            conn.commit()
            return "Answer successcully added to database"

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed posting answer {}".format(error)
        finally:
                # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"

    def accept_answer(self, ans_id):
        """
        Instance method to select answer as preferred
        """
        try:
            cursor = conn.cursor()
            query = """ UPDATE answers SET preferred=%s WHERE (id=%s) """
            cursor.execute(query, [True, ans_id])
            conn.commit()

            return "Answer successcully updated"

            return details

        except (Exception, psycopg2.DatabaseError) as error:
            return "Failed to update answer {}".format(error)

        finally:
            # Close database connection
            if(conn):
                cursor.close()
                conn.close()
                return "PostgresSQL connection closed"
