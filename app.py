from flask import Flask as f1, request, session, redirect, url_for, render_template as f2
import re

import socket
from ide import s1
from web_tutorial import web_tutorial as wb
from python_tutorial import python_tutorial as pt
from css_tutorial import css_tutorial_bp
from js_tutorial import js_tutorial_bp
from editor import editor as s3
from python_quiz import quiz01 as s4
from web_quiz import quiz02 as s5
from registartion import registration_bp
from login import login_bp
from update_password import update_password_bp
from logout import logout_bp
from admin import admin_bp
from ai_code_bp import ai_code_bp
from ai_chat_bp import ai_chat_bp
from project_showcase import project_showcase_bp
from python_quiz_rule import python_quiz_rule_bp
from web_quiz_rule import web_quiz_rule_bp
app = f1(__name__)
app.secret_key = "codenest001"


# Register Blueprints
app.register_blueprint(s1)
app.register_blueprint(wb)
app.register_blueprint(pt)
app.register_blueprint(css_tutorial_bp)
app.register_blueprint(js_tutorial_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(update_password_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(s3)
app.register_blueprint(s4)
app.register_blueprint(s5)
app.register_blueprint(admin_bp)
app.register_blueprint(ai_code_bp)
app.register_blueprint(ai_chat_bp)
app.register_blueprint(project_showcase_bp)
app.register_blueprint(python_quiz_rule_bp)
app.register_blueprint(web_quiz_rule_bp)
# ---------------- Internet Check ----------------
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except:
        return False


# ======================== ROUTES ========================
@app.route("/")
def start():
    if "username" in session:
        return f2("index.html")
    
    if check_internet():
        return f2("registartion.html")
    else:
        return f2("error.html")


# ---------------- Home ----------------
@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return f2("index.html")

