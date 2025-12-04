from flask import Blueprint, render_template, request, send_file, session
from connection import get_db_connection
import random
import pandas as pd
from io import BytesIO

quiz02 = Blueprint("quiz002", __name__)

# ===== Web Quiz Route =====
@quiz02.route("/web_quiz", methods=["GET", "POST"])
def web_quiz():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "GET":
        # Fetch all questions from the database
        cursor.execute("SELECT id, question, option1, option2, option3, option4, answer FROM web_quiz")
        questions = cursor.fetchall()
        random.shuffle(questions)        # shuffle all questions
        questions = questions[:15]       # take only 15
        session['web_quiz_questions'] = questions  # store order in session
    else:
        # On POST, use the same order as stored in session
        questions = session.get('web_quiz_questions', [])

    total = len(questions)
    result = False
    correct = wrong = 0
    user_answers = {}

    if request.method == "POST":
        result = True
        for q in questions:
            ans = request.form.get(f"q{q['id']}", "").strip()
            user_answers[q['id']] = ans

            correct_ans = str(q['answer']).strip().lower()
            user_ans = ans.lower() if ans else ""

            if user_ans == correct_ans:
                correct += 1
            else:
                wrong += 1

        # Store results in session
        session['web_quiz_results'] = {
            "questions": questions,
            "user_answers": user_answers,
            "total": total,
            "correct": correct,
            "wrong": wrong
        }

    cursor.close()
    conn.close()

    return render_template(
        "web_quiz.html",
        questions=questions,
        result=result,
        correct=correct,
        wrong=wrong,
        total=total,
        user_answers=user_answers
    )

# ===== CSV Export Route =====
@quiz02.route("/export_web_csv")
def export_web_csv():
    data = session.get('web_quiz_results')
    if not data:
        return "<script>alert('No quiz results found!'); window.history.back();</script>"

    filename = request.args.get("filename", "web_quiz_results.csv")
    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    rows = []
    for q in data['questions']:
        qid = str(q['id'])
        rows.append({
            "Question": q['question'],
            "Option1": q['option1'],
            "Option2": q['option2'],
            "Option3": q['option3'],
            "Option4": q['option4'],
            "Your Answer": data['user_answers'].get(qid, ""),
            "Correct Answer": q['answer']
        })

    df = pd.DataFrame(rows)

    # Add summary
    summary = pd.DataFrame([
        {"Question": "Total Questions", "Option1": data['total']},
        {"Question": "Correct Answers", "Option1": data['correct']},
        {"Question": "Wrong Answers", "Option1": data['wrong']}
    ])
    df = pd.concat([df, summary], ignore_index=True)

    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )
