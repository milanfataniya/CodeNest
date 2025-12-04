from flask import Blueprint, render_template, request
from connection import get_db_connection
import re
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

update_password_bp = Blueprint("update_password", __name__)

# ----------------- ALERT POPUP FUNCTION -----------------
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
                background: rgba(0,0,0,0.5); display:flex;
                justify-content:center; align-items:center; z-index:9999;
            }}
            .modal {{
                background:#fff; padding:25px 35px; border-radius:12px;
                box-shadow:0 4px 15px rgba(0,0,0,0.3); text-align:center;
                font-family:Arial, sans-serif; max-width:450px;
            }}
            .modal h2 {{ margin-bottom:15px; color:{title_color}; display:flex;
                align-items:center; justify-content:center; gap:10px; font-size:24px; }}
            .modal h2 i {{ font-size:32px; }}
            .modal p {{ margin-bottom:20px; color:#333; line-height:1.4; }}
            .modal button {{
                background:{button_color}; color:#fff; border:none;
                padding:10px 20px; border-radius:6px; cursor:pointer;
                font-size:14px; transition: background 0.3s;
            }}
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


# -----------------email function-----------------
def send_password_update_email(to_email,new_password):
    sender_email = "milanfataniya2021@gmail.com"
    sender_password = "brnh favw pkzt tnul"  

    subject = "Password Updated Successfully"
    body = f"""
    <html>
    <body style="font-family:Arial; color:#333;">
        <h2>Password Updated Successfully ✅</h2>
       
        <p>Your password on <b>CodeNest</b> has been successfully updated.</p>
        <hr>
        <p><b>Account Email:</b> {to_email}</p>
     
        <p><b>New Password:</b> {new_password}</p>
        <hr>
        <p>If you did not perform this action, please reset your password immediately or contact support.</p>
        <br>
        <p>Thank you,<br><b>CodeNest...</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Password update email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)




# ----------------- FORGOT PASSWORD ROUTE -----------------
@update_password_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email").strip()
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # DB connect
        mydb = get_db_connection()
        mycur = mydb.cursor()
        mycur.execute("SELECT password FROM registartion WHERE email=%s", (email,))
        user = mycur.fetchone()

        if not user:
            mycur.close()
            mydb.close()
            return js_alert(f"No account found with email: <b>{email}</b>", "Email Not Found", type="error")

        stored_hashed_password = user[0]

        # Password match validation
        if new_password != confirm_password:
            mycur.close()
            mydb.close()
            return js_alert("Passwords do not match!", "Password Error", type="error")

        #  check passowrd is same as old ?
        if bcrypt.checkpw(new_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            mycur.close()
            mydb.close()
            return js_alert("New password cannot be the same as your current password!", "Password Error", type="error")

        # Password validfdtion
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
        if not re.match(pattern, new_password):
            return js_alert(
                """
                <b>Password must meet these requirements:</b>
                <ul style='color:#e74c3c; text-align:left; margin-left:20px;'>
                    <li>At least 6 characters long</li>
                    <li>At least one uppercase letter</li>
                    <li>At least one lowercase letter</li>
                    <li>At least one number</li>
                    <li>At least one special character (@$!%*?&)</li>
                </ul>
                """,
                "Weak Password", type="error"
            )

        # Hash and update new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mycur.execute("UPDATE registartion SET password=%s WHERE email=%s", (hashed_password, email))
        mydb.commit()
        mycur.close()
        mydb.close()

        # send email
        send_password_update_email(email, new_password=new_password)


        return js_alert(f"Password updated successfully for <b>{email}</b>!", "Success", "/login", type="success")

    return render_template("update_password.html")
