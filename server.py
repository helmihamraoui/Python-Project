from flask_app import app
from flask_app.controllers import category_controller,user_controller,posts_controller,admin_controller,chatbot_controller

if __name__=="__main__":
    app.run(debug=True)