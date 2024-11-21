from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db,app
from flask import flash
import re
from flask_app.models import posts_model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id=data["id"]
        self.user_name=data["user_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.type_user=data["type_user"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.saves=[]

    @classmethod
    def create(cls,data):
        query="insert into users (user_name,email,password,type_user) values(%(user_name)s,%(email)s,%(password)s,0);"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def get_by_id(cls,data):
        query="select * from users where id=%(id)s;"
        res=connectToMySQL(db).query_db(query,data)
        return res[0]
    @classmethod
    def get_by_email(cls,data):
        query="select * from users where email=%(email)s;"
        result=connectToMySQL(db).query_db(query,data)
        if result:
            return cls(result[0])
        return False
    

    @classmethod
    def get_saves_posts(cls, data):
        query = "select * from users join save on users.id = save.user_id join posts  on save.post_id=posts.id where users.id =%(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if results:
            user = cls(results[0])
            for row in results:
                post_dict={
                **row,
                "created_at": row["posts.created_at"],
                "updated_at": row["posts.updated_at"],
                "id": row["posts.id"],
                "user_id": row["posts.user_id"]
                }
                user.saves.append(posts_model.Post(post_dict))
            return user
        else:
            return False
    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM users WHERE id<>%(id)s"""
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def add_message(cls, data):
        query = """INSERT INTO chat (sender_id, receiver_id, message) VALUES (%(sender_id)s, %(receiver_id)s, %(message)s);"""
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_all_messages(cls, data):
        query = """
            SELECT * FROM chat 
            JOIN users ON chat.receiver_id = users.id 
            WHERE (chat.receiver_id = %(receiver_id)s AND chat.sender_id = %(sender_id)s) 
            OR (chat.receiver_id = %(sender_id)s AND chat.sender_id = %(receiver_id)s) 
            ORDER BY chat.created_at;
        """
        result = connectToMySQL(db).query_db(query, data)
        print(result)
        if result:
            all_messages = [message for message in result]
            return all_messages
        return False
    @classmethod
    def get_all_messages_by_user(cls, data):
        query =  """
        SELECT DISTINCT users.*
FROM users
JOIN chat ON (chat.receiver_id = users.id OR chat.sender_id = users.id)
WHERE (chat.receiver_id = %(id)s OR chat.sender_id = %(id)s)
AND users.id != %(id)s
ORDER BY users.user_name;
    """
        result = connectToMySQL(db).query_db(query, data)
        return result
    @classmethod
    def get_one_by_id(cls, data):
        query = """SELECT * FROM users WHERE id=%(id)s"""
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    @classmethod
    def get_feedbacks(cls, data):
        query = """SELECT * FROM project_schema.feedback WHERE user_id=%(user_id)s ORDER BY created_at desc;"""
        result = connectToMySQL(db).query_db(query, data)
        return result if result else []  # Return an empty list if no results are found

    @staticmethod
    def validation( data ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","email_validation")
            is_valid = False
        elif User.get_by_email({"email":data["email"]}):
            flash("User email  found in the database","email_validation")
            is_valid = False
        if len(data['user_name']) < 2:
            flash("user name must be longer then 3","user_name_validation")
            is_valid = False
        if len(data['password']) < 8:
            flash("password must be longer then 8","password_validation")
            is_valid = False
        return is_valid
    @staticmethod
    def validation_password(hashed_password,plain_password):
        if (not bcrypt.check_password_hash(hashed_password,plain_password)):
            flash("wrong password","login_password_validation")
            return False
        else:
            return True