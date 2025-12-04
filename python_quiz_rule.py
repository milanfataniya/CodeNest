from flask import Blueprint, render_template

python_quiz_rule_bp = Blueprint("python_rule", __name__)

@python_quiz_rule_bp.route("/python_rule")
def python_rule01():
    return render_template("python_rule.html")
