from flask import Blueprint,render_template,request

web_tutorial=Blueprint("tutorial01",__name__)
@web_tutorial.route("/web_tutorial",methods=["GET","POST"])
def web_tutorail01():
    return render_template("web_tutorial.html")
