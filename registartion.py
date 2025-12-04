from flask import Blueprint, render_template, session, request
import re
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from connection import get_db_connection


registration_bp = Blueprint("registration_bp", __name__)

# ----------------- SEND EMAIL -----------------
def send_registration_email(to_email, username, password):
    sender_email = "milanfataniya2021@gmail.com"
    sender_password = "brnh favw pkzt tnul"

    subject = "Welcome to CodeNest!"
    body = f"""
Hello {username},

Thank you for registering at CodeNest!
Your account has been created successfully.

Login details:
- Username: {username}
- Email: {to_email}
- Password: {password}

Happy Coding! 🚀
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Email sending failed:", e)



# ----------------- JS ALERT -----------------
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
                position: fixed; top:0; left:0; width:100%; height:100%;
                background: rgba(0,0,0,0.5);
                display:flex; justify-content:center; align-items:center; z-index:9999;
            }}
            .modal {{
                background:#fff; padding:25px 35px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);
                text-align:center; font-family:Arial, sans-serif; max-width:450px;
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


# ----------------- REGISTRATION ROUTE -----------------
@registration_bp.route("/register", methods=["GET", "POST"])
def registration():

    if "username" in session:
        return render_template("index.html")

    if request.method == "POST":
        try:
            name = request.form["nm1"].strip()
            email = request.form["nm2"].strip()
            password = request.form["nm3"]
            confirm = request.form["nm4"]

            # ------------- NAME VALIDATION -------------
            if not name:
                return js_alert("Username cannot be empty!", "Invalid Username", type="error")
            if len(name) < 3:
                return js_alert("Username must be at least 3 characters long!", "Invalid Username", type="error")
            if not re.match(r"^[A-Za-z0-9_]+$", name):
                return js_alert("Username must contain only letters, numbers or underscores!", "Invalid Username", type="error")

            # ------------- EMAIL VALIDATION -------------
            email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
            if not re.match(email_pattern, email):
                return js_alert("Enter valid Gmail address like example@gmail.com!", "Invalid Email", type="error")

            # ------------- PASSWORD VALIDATION -------------
            if password != confirm:
                return js_alert("Passwords do not match!", "Password Error", type="error")

            pwd_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
            if not re.match(pwd_pattern, password):
                return js_alert("""
                    <b>Password requirements:</b>
                    <ul style='text-align:left; margin-left:20px; color:#e74c3c;'>
                        <li>At least 6 characters</li>
                        <li>One uppercase letter</li>
                        <li>One lowercase letter</li>
                        <li>One number</li>
                        <li>One special character (@$!%*?&)</li>
                    </ul>
                """, "Weak Password", type="error")

            # ------------- CHECK USER EXISTS? -------------
            db = get_db_connection()
            cursor = db.cursor(buffered=True)
            cursor.execute("SELECT * FROM registration WHERE name=%s OR email=%s", (name, email))
            user = cursor.fetchone()

            if user:
                cursor.close()
                db.close()
                if user[1] == name:
                    return js_alert("This username is already taken!", "Username Exists", type="error")
                if user[2] == email:
                    return js_alert("This email is already registered!", "Email Exists", type="error")

            # ------------- HASH PASSWORD -------------
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # ------------- INSERT USER (ONLY IF ALL VALID) -------------
            cursor.execute(
                "INSERT INTO registration (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            db.commit()
            cursor.close()
            db.close()

            # ------------- SEND EMAIL -------------
            send_registration_email(email, name, password)

            # ------------- SUCCESS MESSAGE -------------
            return js_alert(
                f"<h4>Welcome to CodeNest!</h4><h3 style='color:#32CD32'><i>{name.capitalize()}</i></h3>",
                "Registration Successful",
                "/login",
                type="success"
            )

        except Exception as e:
            return js_alert(f"Error: {e}", "Error", type="error")

    return render_template("registartion.html")
