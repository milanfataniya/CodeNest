from flask import Blueprint,render_template,request

python_tutorial=Blueprint("python_tutorial",__name__)
@python_tutorial.route("/python_tutorial",methods=["POST","GET"])
def python_tutorial01():
    return render_template("python_tutorial.html")