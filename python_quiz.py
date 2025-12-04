from flask import Blueprint, render_template, request, send_file, session
from connection import get_db_connection
import random
import pandas as pd
from io import BytesIO

quiz01 = Blueprint("quiz1", __name__)
@quiz01.route("/python_quiz", methods=["GET", "POST"])
def python_quiz():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "GET":
        # Fetch all questions from the database
        cursor.execute("SELECT id, question, option1, option2, option3, option4, answer FROM python_quiz")
        questions = cursor.fetchall()
        random.shuffle(questions)  # shuffle all questions
        questions = questions[:15]  # take only 15 questions
        session['quiz_questions'] = questions  # store the shuffled 15 in session
    else:
        # On POST, use the same order as stored in session
        questions = session.get('quiz_questions', [])

    total = len(questions)
    result = False
    correct = wrong = 0
    user_answers = {}

    if request.method == "POST":
        result = True
        correct = wrong = 0
        user_answers = {}

        for q in questions:
            ans = request.form.get(f"q{q['id']}", "").strip()
            user_answers[q['id']] = ans

            correct_ans = str(q['answer']).strip().lower()
            user_ans = ans.lower() if ans else ""

            if user_ans == correct_ans:
                correct += 1
            else:
                wrong += 1
        user_hints = session.get("user_hints", {})



        session['quiz_results'] = {
            "questions": questions,
            "user_answers": user_answers,
            "total": total,
            "correct": correct,
            "wrong": wrong
            
        }

    cursor.close()
    conn.close()

    return render_template(
        "python_quiz.html",
        questions=questions,
        result=result,
        correct=correct,
        wrong=wrong,
        total=total,
        user_answers=user_answers
    )

# ===== CSV Export Route =====
@quiz01.route("/export_csv")
def export_csv():
    data = session.get('quiz_results')
    if not data:
        return "<script>alert('No quiz results found!'); window.history.back();</script>"

    # Prompt filename via GET parameter
    filename = request.args.get("filename", "python_quiz_results.csv")
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

    # Export CSV to memory
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )
