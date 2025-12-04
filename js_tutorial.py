from flask import Blueprint,render_template

js_tutorial_bp=Blueprint("js_tutorial01",__name__)
@js_tutorial_bp.route("/js_tutorial")
def jspage():
    return render_template("js_tutorial.html")