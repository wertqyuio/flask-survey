from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def index():
# name = surveys.surveys["satisfaction"].title
    survey_names = surveys.surveys.keys()
# instructions = surveys.surveys["satisfaction"].instructions
    return render_template("homepage.html", surveys=survey_names)




@app.route("/questions/<int:question_number>", methods=["POST", "GET"])
def question(question_number):
    if request.method == "POST" and question_number == 0:
        session["responses"] = []
        session["survey"] = request.form["survey"]
    if question_number != len(session["responses"]):
        flash("Hey, Please complete the survey in order!")
        return redirect(f"/questions/{len(session['responses'])}")
    

    survey_type = surveys.surveys[session["survey"]]

# survey = surveys.surveys["satisfaction"]  # so that we refer to same survey for questions
    question_reference = survey_type.questions[question_number] if question_number < len(survey_type.questions) else None # Question object
    name = survey_type.title
    if question_reference:
        question = question_reference.question
        choices = question_reference.choices
        allow_text = question_reference.allow_text
        return render_template("questions.html", name=name, question=question, choices=choices, number=question_number)
    else:
        flash("Thank you")
        return redirect("/thanks")


@app.route("/answer",methods=["POST"])
def answer():
    number = int(request.form["number"])
    if request.form.get("answer",None) is None:
        flash("Please enter a valid answer")
        return redirect(f"/questions/{number}")
    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses
    return redirect(f"/questions/{number+1}")


@app.route("/thanks")
def thanks():

    return render_template("thanks.html")