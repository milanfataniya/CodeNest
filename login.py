from flask import Blueprint, render_template, request, session, redirect, url_for
import bcrypt  
from connection import get_db_connection

login_bp = Blueprint("login_bp", __name__)


def js_alert(message, title="Notice", redirect_url=None, type="info"):
    redirect_script = f"window.location.href='{redirect_url}'" if redirect_url else "window.history.back()"

    if type == "success":
        title_color = "#27ae60"
        button_color = "#27ae60"
        button_hover = "#1e8449"
        icon_class = "bi-check-circle-fill"
        animation_class = "animate__tada"
    elif type == "error":
        title_color = "#e74c3c"
        button_color = "#e74c3c"
        button_hover = "#c0392b"
        icon_class = "bi-x-circle-fill"
        animation_class = "animate__shakeX"
    else:
        title_color = "#2980b9"
        button_color = "#2980b9"
        button_hover = "#1f618d"
        icon_class = "bi-info-circle-fill"
        animation_class = "animate__fadeIn"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <style>
            .overlay {{
                position: fixed; top:0; left:0;
                width:100%; height:100%;
                background: rgba(0,0,0,0.5);
                display:flex;
                justify-content:center;
                align-items:center;
                z-index:9999;
            }}
            .modal {{
                background:#fff; padding:25px 35px; border-radius:12px;
                box-shadow:0 4px 15px rgba(0,0,0,0.3); text-align:center;
                font-family:Arial, sans-serif; max-width:450px;
            }}
            .modal h2 {{ margin-bottom:15px; color:{title_color}; display:flex; align-items:center; justify-content:center; gap:10px; font-size:24px; }}
            .modal h2 i {{ font-size:32px; }}
            .modal p {{ margin-bottom:20px; color:#333; line-height:1.4; }}
            .modal button {{ background:{button_color}; color:#fff; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-size:14px; transition: background 0.3s; }}
            .modal button:hover {{ background:{button_hover}; }}
        </style>
    </head>
    <body>
        <div class="overlay">
            <div class="modal animate__animated {animation_class}">
                <h2><i class="bi {icon_class}"></i> {title}</h2>
                <p>{message}</p>
                <button onclick="{redirect_script}">OK</button>
            </div>
        </div>
    </body>
    </html>
    """



# ----------------- Login Route -----------------
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password_text = request.form['password'] 
        password = request.form['password'].encode('utf-8')  # encode password
        
        if email == "admin@gmail.com" and password_text == "Admin@90166":
         session['username'] = "Admin"
         return redirect(url_for("admin_panel.admin"))


        # ----- USER LOGIN -----
        mydb = get_db_connection()
        mycur = mydb.cursor()
        mycur.execute("SELECT name, password FROM registration WHERE email=%s", (email,))
        user = mycur.fetchone()
        mycur.close()
        mydb.close()

        if user:
            stored_name, stored_password = user
            stored_password_bytes = stored_password.encode('utf-8')

            if bcrypt.checkpw(password, stored_password_bytes):
                session['username'] = stored_name
                
                return render_template("index.html", username=stored_name)
            else:
                return js_alert("Password is incorrect. Please try again.", "Login Error", type="error")
        else:
            return js_alert(f"No account found with the email: {email}.<br>Please check your email and try again.", "Login Error", type="error")

    return render_template("login.html")
