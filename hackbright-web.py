from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_homepage():
    """Show homepage"""
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    html = render_template("homepage.html", students=students, projects=projects)

    return html

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github")
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)
    #return "%s is the GitHub account for %s %s" % (github, first, last)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github, rows=rows)
    return html


# @app.route("/student-search")
# def get_student_form():
#     """Show form for searching for a student."""

#     return render_template("student_search.html")


@app.route("/add-student-form")
def provide_add_form():
    """Show form for searching for a student."""

    return render_template("student-add.html")


@app.route("/student-add", methods=["POST"])
def student_add():
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('add-student-confirmation.html', github=github)

@app.route("/project")
def display_project_info():
    title = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(title)
    rows = hackbright.get_grades_by_title(title)
    return render_template('project.html', title=title,
                            description=description,
                            max_grade=max_grade,
                            rows=rows)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

