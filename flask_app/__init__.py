from flask import Flask
from flask_socketio import SocketIO

app=Flask(__name__)
app.secret_key="659851"
db="project_schema"
socketio = SocketIO(app)
