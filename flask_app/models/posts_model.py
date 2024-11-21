import os
from werkzeug.utils import secure_filename
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db
from flask_app import app
from flask import flash
from flask_app.models import user_model
class Post:
    def __init__(self,data):
        self.id=data['id']
        self.title=data['title']
        self.description=data['description']
        self.image=data['image']
        self.location=data['location']
        self.type=data['type']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.category_id=data['category_id']
        self.poster=user_model.User.get_by_id({'id': self.user_id})

    # Database connection setup using the connectToMySQL function
    @classmethod
    def get_posts(cls):
        query = "SELECT * FROM posts order by created_at desc limit 10;"
        results = connectToMySQL(db).query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts
    @classmethod
    def add_post(cls, data):
        query="INSERT INTO posts (title, description, image, location,type, user_id, category_id) VALUES (%(title)s,%(description)s,%(image)s,%(location)s,%(type)s,%(user_id)s,%(category_id)s );"   
        result=connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def get_all_images(cls):
        query = "SELECT img FROM posts"
        result = connectToMySQL(db).query_db(query)
        return result
    @classmethod
    def get_user_posts(cls,data):
        query="select * from posts join users on posts.user_id=users.id where user_id=%(id)s; "
        result= connectToMySQL(db).query_db(query,data)
        all_posts=[]
        for row in result:
            all_posts.append(cls(row))
        return all_posts
    @classmethod
    def delete(cls,data):
        query="delete from posts where id=%(id)s"
        result=connectToMySQL(db).query_db(query,data)
        return result
    
    @classmethod
    def get_post_by_id(cls,data):
        query="select *from posts join users on posts.user_id=users.id where posts.id=%(id)s; "
        result=connectToMySQL(db).query_db(query,data)
        post=cls(result[0])
        return post
    @classmethod
    def get_all_posts(cls,data):
        query="SELECT * FROM posts JOIN category ON posts.category_id=category.id where category.id=%(id)s;"
        result=connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def view(cls,data):
        query="SELECT * FROM posts WHERE id = %(id)s"
        result=connectToMySQL(db).query_db(query,data)
        return cls(result[0])
    # edit
    @classmethod
    def get_one(cls,data):
        query="select * from posts where id=%(id)s"
        result=connectToMySQL(db).query_db(query,data)
        post=result[0]
        print("*"*200,post)
        return post
    @classmethod
    def update(cls,data):
        query="update posts set title=%(title)s ,description=%(description)s,image=%(image)s,location=%(location)s,type=%(type)s,category_id=%(category_id)s where id=%(id)s;"
        result=connectToMySQL(db).query_db(query,data)
        return result
    # endedit
    @classmethod
    def save(cls,data):
        query="insert into save (user_id,post_id,poster_id) values (%(user_id)s,%(post_id)s,%(poster_id)s);"
        result=connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def unsave_post(cls, data):
        query = """
            DELETE FROM save
            WHERE user_id = %(user_id)s AND post_id = %(post_id)s;
        """
        result=connectToMySQL(db).query_db(query, data)
        return result
    @classmethod
    def add_request(cls,data):
        query="INSERT INTO project_schema.request (post_id, user_id,request) VALUES (%(post_id)s,%(user_id)s,%(request)s);"
        result=connectToMySQL(db).query_db(query, data)
        return result
    @classmethod
    def show_request(cls,data):
        query="select * from request where post_id=%(post_id)s and user_id=%(user_id)s;"
        result=connectToMySQL(db).query_db(query, data)
        if result :
            return result
        return False
    @staticmethod
    def validate_post(posts):
        is_valid = True
        if len(posts['title']) < 4:
            flash("Title must be at least 4 characters","title")
            is_valid = False
        if len(posts['description']) < 10:
            flash("Description must be at least 10 characters","description")
            is_valid = False
        if len(posts['location']) < 3:
            flash("Location must be at least 3 characters","location")
            is_valid = False
        return is_valid