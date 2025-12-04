from flask import Blueprint, render_template, request
import google.generativeai as genai

ai_code_bp = Blueprint("ai_code_bp", __name__)
genai.configure(api_key="AIzaSyB04nNHipcwlo8PZ8yRMtkFoQEDeKxWoPM")

def is_code_related(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        result = model.generate_content(
            f"Answer only YES or NO: Is this about coding, programming, or debugging?\n\n{prompt}"
        )
        return "yes" in result.text.lower()
    except Exception:
        return False

def generate_code(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        query = f"Write only the code (no explanation, no markdown) for this request:\n{prompt}"
        response = model.generate_content(query)
        return response.text.strip() if hasattr(response, "text") else " Could not generate code."
    except Exception:
        return "Something went wrong. Try again later."

@ai_code_bp.route("/ai_code", methods=["GET", "POST"])
def ai_code():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        if not prompt:
            return render_template("ai_code_output.html", prompt="No input", code_output=" Please enter a prompt.")

        if not is_code_related(prompt):
            return render_template("ai_code_output.html", prompt=prompt, code_output=" Sorry, please enter a code-related query.")

        code_output = generate_code(prompt)
        return render_template("ai_code_output.html", prompt=prompt, code_output=code_output)

    return render_template("ai_code.html")
