from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.category_model import Category
from flask_app.models.user_model import User
from flask_app.models.posts_model import Post
import json

with open('questions.json', 'r') as f:
    qa_data = json.load(f)
@app.route("/about")
def about():
    return render_template('about_page.html')
@app.route("/home")
def home():
    all_cata=Category.get_all()
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    feedbacks=User.get_feedbacks({'user_id':session['user_id']})
    posts = Post.get_posts()
    return render_template('home.html',all_cata=all_cata,feedbacks=feedbacks,user=user,questions=qa_data,posts =posts)




