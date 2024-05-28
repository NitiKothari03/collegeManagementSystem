from base import app

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000, threaded=True)




























# from flask import *
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def load():
#     return render_template('student/index.html')
#
#
# app.run(debug=True, host='localhost', port=5000, threaded=True)

# @app.route('/login')
# def login():
#     return render_template('admin/login.html')
#
#
# @app.route('/admin/addDegree')
# def addDegree():
#     return render_template('admin/addDegree.html')
#
#
# @app.route('/admin/viewDegree')
# def viewDegree():
#     return render_template('admin/viewDegree.html')
#
#
# @app.route('/admin/addDepartment')
# def addDepartment():
#     return render_template('admin/addDepartment.html')
#
#
# @app.route('/admin/viewDepartment')
# def viewDepartment():
#     return render_template('admin/viewDepartment.html')
#
#
# @app.route('/admin/addSemester')
# def addSemester():
#     return render_template('admin/addSemester.html')
#
#
# @app.route('/admin/viewSemester')
# def viewSemester():
#     return render_template('admin/viewSemester.html')
#
#
# @app.route('/admin/addSubject')
# def addSubject():
#     return render_template('admin/addSubject.html')
#
#
# @app.route('/admin/viewSubject')
# def viewSubject():
#     return render_template('admin/viewSubject.html')
#
#
# @app.route('/admin/addFaculty')
# def addFaculty():
#     return render_template('admin/addFaculty.html')
#
#
# @app.route('/admin/viewFaculty')
# def viewFaculty():
#     return render_template('admin/viewFaculty.html')
#
#
# @app.route('/admin/addStudent')
# def addStudent():
#     return render_template('admin/addStudent.html')
#
#
# @app.route('/admin/viewStudent')
# def viewStudent():
#     return render_template('admin/viewStudent.html')
