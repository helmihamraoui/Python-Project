from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

class Admin:
    def __init__(self,data):
        self.id=data['id']
        self.user_name=data['user_name']
        self.password=data['password']
        self.type_user=data['type_user']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    @classmethod
    def all_request(cls):
        query="select * from project_schema.users join request on users.id = request.user_id join posts on posts.id = request.post_id;"
        result=connectToMySQL(db).query_db(query)
        if result:
            return result
        return False
    @classmethod
    def delete(cls,data):
        query="delete from request where post_id=%(post_id)s and user_id=%(user_id)s;"
        result=connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def all_users(cls):
        query="select * from project_schema.users where type_user=0;"
        result=connectToMySQL(db).query_db(query)
        if result:
            return result
        return False
    @classmethod
    def delete_user(cls,data):
        query="delete from users where id=%(id)s;"
        result=connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def add_feedback(cls,data):
        query="""INSERT INTO project_schema.feedback ( admin_id, user_id, feedback) VALUES (%(admin_id)s,%(user_id)s, %(feedback)s);"""
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def get_one_by_id(cls,data):
        query="select * from project_schema.users where id=%(id)s;"
        result=connectToMySQL(db).query_db(query,data)
        return result [0]