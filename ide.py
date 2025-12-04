from flask import Blueprint as b1
from flask import render_template as rt
from flask import request
import sys
import io

s1 = b1("ide01", __name__)


def get_default_code():
    return '''#     CodeNest Python Editor
def welcome():
    print("                  Welcome to CodeNest!")
    print("        Your Smart Python Learning Playground")
    print("==================================================")
    print("Tips:")
    print(" • Write Python code in the editor")
    print(" • Click RUN to execute your code")
    print(" • Use CLEAR to reset the editor")
    print(" • Use SAVE to download your code")
    print(" • Use OPEN FILE to load existing .py files")
    print(" • Start learning, start coding!")
   
welcome()
'''
# -------------------------------------------
#   ROUTE: PYTHON IDE PAGE
# -------------------------------------------

@s1.route("/ide", methods=["GET", "POST"])
def python_idle():
    code = get_default_code()  # default launching screen code
    output = ""

    if request.method == "POST":
        code = request.form["code"]

        # Capture stdout & stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = sys.stderr = io.StringIO()

        try:
            exec(code, {})
        except Exception as e:
            output = str(e)
        else:
            output = sys.stdout.getvalue()

        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return rt("ide01.html", code=code, output=output)
