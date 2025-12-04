from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from connection import get_db_connection

project_showcase_bp = Blueprint('project_showcase', __name__)


# ---------------- Fetch all projects ----------------
def fetch_all_projects():
    mydb = get_db_connection()
    mycur = mydb.cursor(dictionary=True)
    mycur.execute("SELECT title, description, username, created_at FROM project_idea ORDER BY created_at DESC")
    projects = mycur.fetchall()
    mycur.close()
    mydb.close()
    project_count = len(projects)
    return projects, project_count




@project_showcase_bp.route("/project-showcase", methods=["GET", "POST"])
def showcase():
    username = session.get('username')
    
    if not username:
        flash("You must be logged in to share a project.")
        return redirect(url_for('login'))

    if request.method == "POST":
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()

        if not title or not description:
            flash("Please fill in both Title and Description.")
            return redirect(url_for('project_showcase.showcase'))

        mydb = get_db_connection()
        mycur = mydb.cursor()
        mycur.execute(
            "INSERT INTO project_idea (title, description, username) VALUES (%s, %s, %s)",
            (title, description, username)
        )
        mydb.commit()
        mycur.close()
        mydb.close()

        return f"""
        <script>
            alert("{username} Your project idea was added successfully!");
            window.location="{url_for('project_showcase.showcase')}";
        </script>
        """

    # Fetch projects and count
    projects, project_count = fetch_all_projects()
    return render_template("project_showcase.html", projects=projects, project_count=project_count,username=username)
