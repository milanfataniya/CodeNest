from flask import Blueprint, render_template

web_quiz_rule_bp = Blueprint("web_rule", __name__)

@web_quiz_rule_bp.route("/web_rule")
def python_rule01():
    return render_template("web_rule.html")
