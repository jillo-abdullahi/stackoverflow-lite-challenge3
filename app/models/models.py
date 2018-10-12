"""module for all models of the application"""

from instance.config import conn
from app.utils import fetch_one


class User(object):
    """
    Class representing users
    """

    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def register_user(self, cursor):
        """
        Instance method to create new user
        """

        query = "INSERT INTO users (username, email, password, confirm_password) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (self.username, self.email,
                               self.password, self.confirm_password))
        conn.commit()

    @staticmethod
    def get_users(cursor):
        """
        method to get all users
        """

        query = "SELECT * FROM users;"
        cursor.execute(query)
        all_users = cursor.fetchall()

        results = []
        for user in all_users:
            details = {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "password": user[3],
                "confirm_password": user[4]
            }

            results.append(details)

        return results

    @staticmethod
    def get_user(cursor, username):
        """
        method to get user_id by username
        """
        query = "SELECT id FROM users WHERE username=%s"
        user_id = fetch_one(query, username)
        return user_id

    @staticmethod
    def login_user(cursor, email, password):
        """
        method to check if user can login
        """
        query = "SELECT * FROM users WHERE (email=%s);"
        user = fetch_one(query, email)

        result = {
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
            "password": user[3],
            "confirm_password": user[4]
        }

        return result


class Question(object):
    """
    Class representing questions
    """

    def __init__(self, title, description, user_id, date_created):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date_created = date_created

    def post_question(self, cursor):
        """
        Instance method to post new question
        """

        query = "INSERT INTO questions (title, description, date_created, user_id) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (self.title, self.description,
                               self.user_id, self.date_created))
        conn.commit()

    @staticmethod
    def get_all_questions(cursor):
        """
        Instance method to get all questions
        """
        query = "SELECT * FROM questions;"
        cursor.execute(query)
        all_questions = cursor.fetchall()

        results = []
        for question in all_questions:

            ans_query = "SELECT * FROM answers WHERE question_id=%s"
            cursor.execute(ans_query, (question[0],))
            answers = cursor.fetchall()

            # Get username
            user_query = "SELECT username FROM users WHERE id=%s"
            username = fetch_one(user_query, (question[4],))

            ans_result = []
            if answers:
                for answer in answers:
                    detail = {
                        "date_created": answer[2],
                        "title": answer[1],
                        "preferred": answer[5],
                        "id": answer[0],
                        "user_id": answer[4]
                    }
                    ans_result.append(detail)

            details = {
                "question_id": question[0],
                "title": question[1],
                "description": question[2],
                "date_created": question[3],
                "user_id": question[4]
            }
            details["Answers"] = ans_result
            details["username"] = username
            results.append(details)

        return results

    @staticmethod
    def get_one_question(cursor, qn_id):
        """
        Instance method to fetch a specific question
        """

        qn_query = "SELECT * FROM questions WHERE id=%s;"
        question = fetch_one(qn_query, qn_id)

        ans_query = "SELECT * FROM answers WHERE question_id=%s"
        cursor.execute(ans_query, [qn_id])
        answers = cursor.fetchall()

        # Get username
        user_query = "SELECT username FROM users WHERE id=%s"
        username = fetch_one(user_query, (question[4],))

        ans_result = []
        if answers:
            for answer in answers:
                user_query = "SELECT username FROM users WHERE id=%s"
                ans_username = fetch_one(user_query, (answer[4],))
                details = {
                    "date_created": answer[2],
                    "title": answer[1],
                    "preferred": answer[5],
                    "id": answer[0],
                    "user_id": answer[4],
                    "username": ans_username
                }

                ans_result.append(details)

        if question:
            details = {
                "question_id": question[0],
                "title": question[1],
                "description": question[2],
                "date_created": question[3],
                "user_id": question[4]
            }
            details["username"] = username
            details["Answers"] = ans_result

            return details

    @staticmethod
    def delete_question(cursor, qn_id):
        """
        method to delete a question
        """

        query = "DELETE FROM questions WHERE id=%s;"
        cursor.execute(query, [qn_id])
        conn.commit()

    @staticmethod
    def get_question_author(cursor, qn_id):
        """
        Method to get user id based on question
        """
        query = "SELECT user_id FROM questions WHERE id=%s"
        result = fetch_one(query, qn_id)

        return result

    @staticmethod
    def get_questions_by_user(cursor, user_id):
        """
        method to list questions asked by a given user
        """
        query = "SELECT * FROM questions WHERE user_id=%s;"
        cursor.execute(query, (user_id,))
        all_questions = cursor.fetchall()

        results = []
        for question in all_questions:

            ans_query = "SELECT * FROM answers WHERE question_id=%s"
            cursor.execute(ans_query, (question[0],))
            answers = cursor.fetchall()

            # Get username
            user_query = "SELECT username FROM users WHERE id=%s"
            cursor.execute(user_query, (question[4],))
            username = cursor.fetchone()

            ans_result = []
            if answers:
                for answer in answers:
                    detail = {
                        "date_created": answer[2],
                        "title": answer[1],
                        "preferred": answer[5],
                        "id": answer[0],
                        "user_id": answer[4]
                    }
                    ans_result.append(detail)

            details = {
                "question_id": question[0],
                "title": question[1],
                "description": question[2],
                "date_created": question[3],
                "user_id": question[4]
            }
            details["Answers"] = ans_result
            details["username"] = username
            results.append(details)

        return results


class Answer(object):
    """
    Class representing answers
    """

    def __init__(self, desc, date_created, user_id, qn_id, preferred=False):
        self.desc = desc
        self.user_id = user_id
        self.date_created = date_created
        self.preferred = preferred
        self.qn_id = qn_id

    def post_answer(self, cursor):
        """
        Instance method to post answer
        """

        query = "INSERT INTO answers (description, date_created, user_id, question_id, preferred) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, (self.desc, self.date_created,
                               self.user_id, self.qn_id, self.preferred))
        conn.commit()

    @staticmethod
    def accept_answer(cursor, ans_id):
        """
        method to select answer as preferred
        """

        query = "UPDATE answers SET preferred=%s WHERE (id=%s);"
        cursor.execute(query, [True, ans_id])
        conn.commit()

    @staticmethod
    def update_answer(cursor, description, ans_id):
        """
        method to update details of an answer
        """

        query = "UPDATE answers SET description=%s WHERE (id=%s);"
        cursor.execute(query, [description, ans_id])
        conn.commit()

    @staticmethod
    def get_answer_by_question_id(cursor, qn_id):
        """
        method to get a specific answer using question id
        """
        ans_query = "SELECT * FROM answers WHERE question_id=%s;"
        result = fetch_one(ans_query, qn_id)

        return result

    @staticmethod
    def get_answer_title(cursor, ans_id):
        """
        method to get answer body
        """
        query = "SELECT description FROM answers WHERE (id=%s);"
        cursor.execute(query, [ans_id])
        description = cursor.fetchone()

        return description

    @staticmethod
    def delete_answer(cursor, ans_id):
        """
        method to delete answer
        """
        ans_query = "DELETE FROM answers WHERE question_id=%s;"
        cursor.execute(ans_query, [ans_id])

    @staticmethod
    def get_answers_by_user(cursor, user_id):
        """
        Get answers posted by a given user
        """
        ans_query = "SELECT * FROM answers WHERE user_id=%s;"
        cursor.execute(ans_query, [user_id])
        answers = cursor.fetchall()

        ans_result = []
        if answers:
            for answer in answers:
                details = {
                    "date_created": answer[2],
                    "title": answer[1],
                    "preferred": answer[5],
                    "id": answer[0]
                }

                ans_result.append(details)

        return ans_result

    @staticmethod
    def get_answer_author(cursor, ans_id):
        """
        Method to get answer author
        """
        query = "SELECT user_id FROM answers WHERE id=%s"
        result = fetch_one(query, ans_id)

        return result
