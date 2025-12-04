from flask import Blueprint,render_template

css_tutorial_bp = Blueprint("css_tutorial", __name__)

@css_tutorial_bp.route("/css_tutorial01")
def css_page():
    return render_template("css_tutorial.html")