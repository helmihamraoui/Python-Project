from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db
from flask import flash
class Category:
    def __init__(self,data):
        self.id=data["id"]
        self.title=data["title"]
        self.image=data["image"]
        self.created_at=data["created_at"]
        self.update_at=data["update_at"]
        self.user_id=data["user_id"]
    @classmethod
    def add_new(cls,data):
        query="""insert into category (title,image,user_id) values (%(title)s,%(image)s,%(user_id)s) ;"""
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def delete_category(cls,data):
        query="""delete from category where  id=%(id)s ;"""
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def get_all_images(cls):
        query = "SELECT * from category ;"
        resulta=connectToMySQL(db).query_db(query)
        return resulta
    @staticmethod
    def valid(data):
        if len(data['title']) <=2:
            flash('name of category mut be at least 2 characteres ','title')
            return False            
        return True