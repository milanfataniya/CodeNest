from flask import Blueprint, render_template, request

editor = Blueprint("editor01", __name__)

@editor.route("/editor", methods=["GET", "POST"])
def editor01():
    return render_template("editor.html")
