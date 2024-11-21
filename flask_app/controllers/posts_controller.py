from flask_app import app
from flask import render_template,redirect,request,session,flash,url_for
import os
import uuid
from werkzeug.utils import secure_filename  
from flask_app.models.posts_model import Post
from flask_app.models.user_model import User
from flask_app.models.category_model import Category
# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join('flask_app', 'static', 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/profile')
def show():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    all_cata=Category.get_all()
    posts=Post.get_user_posts(data)
    return render_template("profile.html",posts=posts,user=user,all_cata=all_cata,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
@app.route("/post/<int:id>/delete")
def delete(id):
    data={
        "id":id
    }
    Post.delete(data)
    return redirect('/profile')
@app.route('/add/posts')
def add_posts():
    if 'user_id' not in session:
        return redirect('/')
    all_cata=Category.get_all()
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    return render_template('add_posts.html',all_cata=all_cata,user=user,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))

@app.route('/create/post', methods=['POST'])
def create_post():
    if Post.validate_post(request.form):
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']

        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique identifier using uuid and combine it with the original filename
            unique_filename = str(uuid.uuid4()) + "_" + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            # Save the file to the static folder
            file.save(file_path)

            # Insert image filename into the database
            data = {
            **request.form,
            "image": unique_filename,
            'user_id': session['user_id']
            }
            Post.add_post(data)
            return redirect('/profile')
    return redirect('/add/posts')
@app.route("/post/edit/<int:id>")
def update_form(id):
    data={
        "id":id
    }
    post=Post.get_post_by_id(data)
    all_cata=Category.get_all()
    vdata = {
        'id':session['user_id']
    }
    user=User.get_by_id(vdata)
    return render_template("update.html",post=post,all_cata=all_cata,user=user,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
@app.route("/post/update/<int:id>",methods=["POST"])
def update_post(id):
    if Post.validate_post(request.form):
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']

        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique identifier using uuid and combine it with the original filename
            unique_filename = str(uuid.uuid4()) + "_" + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            # Save the file to the static folder
            file.save(file_path)

            # Insert image filename into the database
            data = {
            **request.form,
            "id":id,
            "image": unique_filename,
            'user_id': session['user_id']
            }
            Post.update(data)
            return redirect("/profile")
    return redirect(f'/post/edit/{id}')
@app.route('/view/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        "id":id
    }
    request_id={
        "user_id":session['user_id'],
        "post_id":id
    }
    request=Post.show_request(request_id)
    all_cata=Category.get_all()
    user=User.get_by_id({'id':session['user_id']})
    post=Post.get_post_by_id(data)
    return render_template("view.html",post=post,user=user,all_cata=all_cata,request=request,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
@app.route('/posts/<int:id>')
def all_posts(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
        }
    all_cata = Category.get_all()
    posts = Post.get_all_posts(data)
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    return render_template("all_post.html", posts=posts, user=user,all_cata=all_cata,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
# image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/saved')
def saved():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {'id': session['user_id']}
    name=User.get_by_id(data)
    all_cata = Category.get_all()
    user = User.get_saves_posts(data)
    data = {
        'id':session['user_id']
    }
    conect=User.get_by_id(data)# Returns a User object with populated saves

    if user:
        saves = user.saves  # Get the list of saved posts
    else:
        saves = []  # No saved posts found
    
    return render_template("saved.html", saves=saves, conect=conect,all_cata=all_cata,name=name,user=user,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
@app.route('/saved/<int:id>',methods=['post'])
def saved_post(id):
    post=Post.get_one({'id':id})
    data={
        'user_id':session['user_id'],
        'post_id':id,
        'poster_id':post['user_id']
    }
    Post.save(data)
    return redirect('/saved')
@app.route('/post/<int:post_id>/unsave', methods=['POST'])
def unsave_post(post_id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    Post.unsave_post(data)  
    return redirect('/saved')
@app.route('/request/<int:id>',methods=['post'])
def request_post(id):
    data={
        'user_id':session['user_id'],
        'post_id':id,
        **request.form
    }
    Post.add_request(data)
    return redirect('/view/'+str(id))