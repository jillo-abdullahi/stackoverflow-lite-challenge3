"""module for all models of the application"""

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
            details = {}
            details["user_id"] = user[0]
            details["username"] = user[1]
            details["email"] = user[2]
            details["password"] = user[3]
            details["confirm_password"] = user[4]
            results.append(details)

        return results

    @staticmethod
    def login_user(cursor, email, password):
        """
        method to check if user can login
        """
        query = "SELECT * FROM users WHERE (email=%s);"
        cursor.execute(query, [email])
        user = cursor.fetchone()

        result = {}
        result["user_id"] = user[0]
        result["username"] = user[1]
        result["email"] = user[2]
        result["password"] = user[3]
        result["confirm_password"] = user[4]

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
            details = {}
            details["question_id"] = question[0]
            details["title"] = question[1]
            details["description"] = question[2]
            details["date_created"] = question[3]
            details["user_id"] = question[4]
            results.append(details)

        return results

    @staticmethod
    def get_one_question(cursor, qn_id):
        """
        Instance method to fetch a specific question
        """

        qn_query = "SELECT * FROM questions WHERE id=%s;"
        cursor.execute(qn_query, [qn_id])
        question = cursor.fetchone()

        ans_query = "SELECT * FROM answers WHERE question_id=%s"
        cursor.execute(ans_query, [qn_id])
        answers = cursor.fetchall()

        ans_result = []
        if answers:
            for answer in answers:
                details = {}
                details["date_created"] = answer[2]
                details["title"] = answer[1]
                details["preferred"] = answer[5]
                details["id"] = answer[0]
                details["user_id"] = answer[3]
                ans_result.append(details)

        if question:
            details = {}
            details["question_id"] = question[0]
            details["title"] = question[1]
            details["description"] = question[2]
            details["date_created"] = question[3]
            details["user_id"] = question[4]
            details["Answers"] = ans_result

            return details

    @staticmethod
    def delete_question(cursor, qn_id):
        """
        Instance method to delete a question
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
        cursor.execute(query, [qn_id])
        result = cursor.fetchone()
        conn.commit()

        return result


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
        cursor.execute(ans_query, [qn_id])
        result = cursor.fetchone()

        return result

    @staticmethod
    def delete_answer(cursor, qn_id):
        """
        method to delete answer
        """
        ans_query = "DELETE FROM answers WHERE question_id=%s;"
        cursor.execute(ans_query, [qn_id])

    @staticmethod
    def get_user_by_answer_id(cursor, ans_id):
        """
        Get a specific answer using answer id
        """
        ans_query = "SELECT * FROM answers WHERE user_id=%s;"
        cursor.execute(ans_query, [user_id])
        answers = cursor.fetchall()

        ans_result = []
        if answers:
            for answer in answers:
                details = {}
                details["date_created"] = answer[2]
                details["title"] = answer[1]
                details["preferred"] = answer[5]
                details["id"] = answer[0]
                ans_result.append(details)

        return ans_result

    @staticmethod
    def get_answer_author(cursor, ans_id):
        """
        Method to get answer author
        """
        query = "SELECT user_id FROM answers WHERE id=%s"
        cursor.execute(query, [ans_id])
        result = cursor.fetchone()

        return result
