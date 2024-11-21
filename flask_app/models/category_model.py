from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

class Category:
    def __init__(self,data):
        self.id=data['id']
        self.title=data['title']
        self.image=data['image']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.poster=""
    @classmethod
    def get_all(cls):
        query="SELECT * FROM category ;"
        result=connectToMySQL(db).query_db(query)
        category=[]
        for row in result:
            category.append(cls(row))
        return category 
    