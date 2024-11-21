from flask_app import app
from flask  import render_template,redirect,request,session,flash  
from flask_app.models.admin_model import Admin
from flask_app.models.admin_category import Category
from werkzeug.utils import secure_filename
import os
import uuid
UPLOAD_FOLDER = os.path.join('flask_app', 'static', 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
@app.route('/dashbord/admin/request')
def show_request():
    if 'user_id'  in session:
        user=Admin.get_one_by_id({'id':session["user_id"]})
        print(user)
        if user['type_user']==1:
            return render_template('request.html',requests=Admin.all_request())
        else:
            return redirect('/home')
        
    return redirect('/')
    
@app.route('/delete/<int:post_id>/<int:user_id>',methods=['post'])
def delete_post(post_id,user_id):
    Admin.delete({'post_id':post_id,'user_id':user_id})
    return redirect('/dashbord/admin/request')
@app.route('/dashbord/admin/users')
def all_users():
    if 'user_id'  in session:
        user=Admin.get_one_by_id({'id':session["user_id"]})
        if user['type_user']==1:
            return render_template('all_users.html',users=Admin.all_users())
        else:
            return redirect('/home')
    return redirect('/')
@app.route('/delete/<int:id>',methods=['post'])
def delete_user(id):
    Admin.delete_user({'id':id})
    return redirect("/dashbord/admin/users")
@app.route('/dashbord/admin/category')
def form_category():
    if 'user_id'  in session:
        user=Admin.get_one_by_id({'id':session["user_id"]})
        if user['type_user']==1:
            categories=Category.get_all_images()
            return render_template("add_category.html",categories=categories)
        else:
            return redirect('/home')
    return redirect('/')
@app.route('/add/category',methods=['post'])
def add_category():
    if Category.valid(request.form):
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        # Generate a unique identifier using uuid and combine it with the original filename
            unique_filename = str(uuid.uuid4()) + "_" + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        # Save the file to the static folder
            file.save(file_path)


            data={
            **request.form,
            'image':unique_filename,
            'user_id': session['user_id']
            }
            Category.add_new(data)
            return redirect("/dashbord/admin/category")
    return redirect("/dashbord/admin/category")    
@app.route('/remove/<int:id>',methods=['post'])
def remove_category(id):
    Category.delete_category({'id':id})
    return redirect("/dashbord/admin/category")
@app.route('/feedback/<int:id>',methods=['post'])
def add_feedback(id):
    data={
        'admin_id':session['user_id'],
        'user_id':id,
        **request.form
    }
    Admin.add_feedback(data)
    return redirect("/dashbord/admin/users")