from flask import Blueprint, render_template, session, redirect, url_for, request
from connection import get_db_connection
from datetime import datetime, timedelta

# Create Blueprint
admin_bp = Blueprint("admin_panel", __name__)



# ----------------- Admin Dashboard -----------------
@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or session["username"] != "Admin":
        return redirect(url_for("login_bp.login"))

    mydb = get_db_connection()
    mycur = mydb.cursor(dictionary=True)

    # ----- Delete User -----
    delete_user_id = request.args.get("delete_user")
    if delete_user_id:
     
        mycur.execute("DELETE FROM registration WHERE id = %s", (delete_user_id,))
        mydb.commit()
        return redirect(url_for("admin_panel.admin"))

    # ----- Delete Project -----
    delete_project_id = request.args.get("delete_project")
    if delete_project_id:
        mycur.execute("DELETE FROM project_idea WHERE id = %s", (delete_project_id,))
        mydb.commit()
        return redirect(url_for("admin_panel.admin"))

    # ----- Fetch All Users -----
    mycur.execute("SELECT id, name, email FROM registration")
    users = mycur.fetchall()
    user_count = len(users)

    # ----- Fetch All Projects -----
    mycur.execute("SELECT id, title FROM project_idea")
    projects = mycur.fetchall()
    project_count = len(projects)
    


    mycur.close()
    mydb.close()

    return render_template(
        "dashboard.html",
        users=users,
        projects=projects,
        user_count=user_count,
        project_count=project_count
   
    )
