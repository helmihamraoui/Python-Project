from flask import render_template,redirect,session,request,flash
from flask_app import app,socketio
from flask_app.models.user_model import User
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_bcrypt import Bcrypt 
bcrypt=Bcrypt(app)


@app.route('/')
def index ():
    return render_template("signup.html")
@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/register', methods=['POST'])
def regist():
    if  User.validation(request.form):

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data={
            **request.form,'password':pw_hash
            
        }
        
        user_id=User.create(data)
        session['user_id']=user_id
        return redirect('/home')
    return redirect('/')
@app.route("/login/user",methods=["POST"])
def login_processing():
    data={
        "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)
        # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email","email_validation_login")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password","login_password_validation")
        return redirect('/login')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
        # never render on a post!!!
    return redirect("/home")

@app.route("/logout")
def log_out():
    
    session.clear()
    return redirect('/login')
@app.route('/messages')
def show_users():
    if 'user_id' in session:
        receiver = User.get_one_by_id({'id': id})
        users = User.get_all_messages_by_user({'id': session['user_id']})
        return render_template('chat_template.html', messages=False, receiver=receiver,users=users,feedbacks=User.get_feedbacks({'user_id':session['user_id']}))
    else:
        return redirect('/')
@app.route('/messages/<int:id>')
def chat(id):
    if 'user_id' in session:
        data = {
            'receiver_id': id,
            'sender_id': session['user_id']
        }
        receiver = User.get_one_by_id({'id': id})
        messages = User.get_all_messages(data)
        users = User.get_all_messages_by_user({'id': session['user_id']})
        feedbacks=User.get_feedbacks({'user_id':session['user_id']})
        return render_template('chat.html', messages=messages, receiver=receiver,users=users,feedbacks=feedbacks)
    else:
        return redirect('/')

# Real-time messaging using Socket.IO
@socketio.on('join_room')
def join_user_room(data):
    """
    When a user joins a chat room, based on sender and receiver IDs
    """
    room = f"chat_{min(data['sender_id'], data['receiver_id'])}_{max(data['sender_id'], data['receiver_id'])}"
    join_room(room)
    print(f"User {data['sender_id']} joined room {room}")

@socketio.on('send_message')
def handle_message(data):
    """
    Handle sending message to specific user room.
    """
    room = f"chat_{min(data['sender_id'], data['receiver_id'])}_{max(data['sender_id'], data['receiver_id'])}"
    # Save the message in the database
    User.add_message(data)
    # Send the message to the specific room
    emit('receive_message', data, room=room)
    
@socketio.on('leave_room')
def leave_user_room(data):
    """
    Handle a user leaving a room.
    """
    room = f"chat_{min(data['sender_id'], data['receiver_id'])}_{max(data['sender_id'], data['receiver_id'])}"
    leave_room(room)
    print(f"User {data['sender_id']} left room {room}")
