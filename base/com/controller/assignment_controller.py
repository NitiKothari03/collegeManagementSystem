import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.assignment_dao import AssignmentDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_assignment_dao import StudentAssignmentDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_assignment_vo import StudentAssignmentVO
from base.com.vo.student_vo import StudentVO
from base.com.vo.subject_vo import SubjectVO

ASSIGNMENT_FOLDER = 'base/static/adminResources/assignment/'
app.config['ASSIGNMENT_FOLDER'] = ASSIGNMENT_FOLDER

STUDENT_ASSIGNMENT_FOLDER = 'base/static/studentResources/assignments/'
app.config['STUDENT_ASSIGNMENT_FOLDER'] = STUDENT_ASSIGNMENT_FOLDER


@app.route('/faculty/load_assignment')
def faculty_load_assignment():
    try:
        if admin_login_session() == "faculty":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing faculty department id
            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing semester based on department id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_department_id = faculty_department_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            return render_template('faculty/addAssignment.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/insert_assignment', methods=['POST'])
def faculty_insert_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing the data from ui
            assignment_semester_id = request.form.get('assignmentSemesterId')
            assignment_subject_id = request.form.get('assignmentSubjectId')
            assignment_title = request.form.get('assignmentTitle')
            assignment_start_date = request.form.get('assignmentStartDate')
            assignment_end_date = request.form.get('assignmentEndDate')
            assignment_description = request.form.get('assignmentDescription')
            assignment_marks = request.form.get('assignmentMarks')
            assignment_image = request.files.get('assignmentImage')
            assignment_image_name = secure_filename(assignment_image.filename)
            assignment_image_path = os.path.join(
                app.config['ASSIGNMENT_FOLDER'])
            assignment_image.save(os.path.join(assignment_image_path,
                                               assignment_image_name))

            # storing the data in database
            assignment_vo.assignment_semester_id = assignment_semester_id
            assignment_vo.assignment_subject_id = assignment_subject_id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo.assignment_title = assignment_title
            assignment_vo.assignment_startdate = assignment_start_date
            assignment_vo.assignment_enddate = assignment_end_date
            assignment_vo.assignment_description = assignment_description
            assignment_vo.assignment_marks = assignment_marks
            assignment_vo.assignment_image_name = assignment_image_name
            assignment_vo.assignment_image_path = assignment_image_path.replace(
                "base", "..")

            assignment_dao.insert_assignment(assignment_vo)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_insert_assignment route exception "
              "occured>>>>>>>>>>>>>", ex)


@app.route('/faculty/view_assignment')
def faculty_view_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing assignment data based on faculty id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo_list = assignment_dao.faculty_view_assignment(
                assignment_vo)

            return render_template('faculty/viewAssignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_view_assignment route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/view_assignment_grades')
def faculty_view_assignment_grades():
    try:
        if admin_login_session() == "faculty":
            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing assignment data based on faculty id
            st_assignment_vo.st_assign_faculty_id = faculty_id
            assignment_vo_list = \
                st_assignment_dao.faculty_view_assignment_grades(
                    st_assignment_vo)

            return render_template('faculty/viewAssignmentGrades.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "faculty_view_assignment_grades route exception occured>>>>>>>>>>",
            ex)


@app.route('/faculty/delete_assignment')
def faculty_delete_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            # deleting assignment data from database
            assignment_id = request.args.get('assignmentId')
            assignment_vo.assignment_id = assignment_id
            assignment_vo_list = assignment_dao.delete_assignment(
                assignment_vo)

            # deleting assignment file
            file_path = assignment_vo_list.assignment_image_path.replace(
                "..", "base") + assignment_vo_list.assignment_image_name
            os.remove(file_path)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_delete_assignment route exception occured>>>>>>>>>>",
              ex)


@app.route('/faculty/delete_assignment_grades')
def faculty_delete_assignment_grades():
    try:
        if admin_login_session() == "faculty":
            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()

            # deleting assignment data from database
            st_assign_id = request.args.get('AssignmentId')
            st_assignment_vo.st_assign_id = st_assign_id
            assignment_vo_list = st_assignment_dao.delete_assignment_grades(
                st_assignment_vo)

            # deleting assignment file
            file_path = assignment_vo_list.st_assign_image_path.replace(
                "..", "base") + assignment_vo_list.st_assign_image_name
            print("file path>>>>>>>>>>>", file_path)
            os.remove(file_path)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/faculty/view_assignment_grades')
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "faculty_delete_assignment_grades route exception occured>>>>>>>>>>",
            ex)


@app.route('/faculty/edit_assignment')
def faculty_edit_assignment():
    try:
        if admin_login_session() == "faculty":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing faculty department id
            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing semester based on department id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_department_id = faculty_department_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            # bringing assignment data to edit
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()
            assignment_id = request.args.get('assignmentId')
            assignment_vo.assignment_id = assignment_id
            assignment_vo_list = assignment_dao.edit_assignment(assignment_vo)
            print("\nassignment_vo_list>>>>>>>>>>>>>>>>>>>",
                  assignment_vo_list)
            return render_template('faculty/editAssignment.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list,
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_assignment route exception occured>>>>>>>>>>>>",
              ex)


@app.route('/faculty/edit_assignment_grades')
def faculty_edit_assignment_grades():
    try:
        if admin_login_session() == "faculty":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing faculty department id
            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing assignment id and forwading it to assignment_dao
            assignment_id = request.args.get('AssignmentId')
            assignment_dao = AssignmentDAO()
            assignment_vo_list = assignment_dao.find_assignment(assignment_id)

            # bringing semester and subject of assignment
            semester_subject_list = assignment_dao.find_semester_subject(assignment_id)

            # bringing assignment data to edit
            st_assign_id = request.args.get('StAssignmentId')

            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()

            st_assignment_vo.st_assign_id = st_assign_id
            assignment_grade_list = st_assignment_dao.edit_assignment_grades(
                st_assignment_vo)

            return render_template('faculty/editAssignmentGrades.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_subject_list=semester_subject_list,
                                   assignment_vo_list=assignment_vo_list,
                                   assignment_grade_list=assignment_grade_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_assignment route exception occured>>>>>>>>>>>>",
              ex)


@app.route('/faculty/update_assignment', methods=['POST'])
def faculty_update_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing assignment data from ui
            assignment_id = request.form.get('assignmentId')

            assignment_semester_id = request.form.get('assignmentSemesterId')
            assignment_subject_id = request.form.get('assignmentSubjectId')
            assignment_title = request.form.get('assignmentTitle')
            assignment_start_date = request.form.get('assignmentStartDate')
            assignment_end_date = request.form.get('assignmentEndDate')
            assignment_description = request.form.get('assignmentDescription')
            assignment_marks = request.form.get('assignmentMarks')

            # storing all the data in database
            assignment_vo.assignment_semester_id = assignment_semester_id
            assignment_vo.assignment_id = assignment_id
            assignment_vo.assignment_subject_id = assignment_subject_id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo.assignment_title = assignment_title
            assignment_vo.assignment_startdate = assignment_start_date
            assignment_vo.assignment_enddate = assignment_end_date
            assignment_vo.assignment_description = assignment_description
            assignment_vo.assignment_marks = assignment_marks

            assignment_dao.update_assignment(assignment_vo)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_insert_assignment route exception "
              "occured>>>>>>>>>>>>>", ex)


@app.route('/faculty/update_assignment_grades', methods=['POST'])
def faculty_update_assignment_grades():
    try:
        if admin_login_session() == "faculty":

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing assignment data from ui
            assignment_id = request.form.get('assignmentId')
            assigned_marks = request.form.get('assignedMarks')
            assignment_remarks = request.form.get('assignmentRemarks')
            st_assign_student_id = request.form.get('studentId')
            st_assign_id = request.form.get('stAssignId')

            print('\n>>>>>>>>>>>>', assignment_remarks, '\n>>>>>>>>>>>>',
                  len(assignment_remarks))

            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()

            st_assignment_vo.st_assign_id = st_assign_id
            st_assignment_vo.st_assignment_id = assignment_id
            st_assignment_vo.st_assign_student_id = st_assign_student_id
            st_assignment_vo.st_assign_marks = assigned_marks
            st_assignment_dao.update_assignment_marks(st_assignment_vo)

            student_dao = StudentDAO()
            student_login_id = student_dao.find_login_id(st_assign_student_id)

            student_login_username = login_dao.find_login_username(
                student_login_id)

            # assignment_id = st_assignment_dao.find_assignment(assignment_id)
            # print("assignment_id>>>>>>>>>>>",assignment_id)

            assignment_dao = AssignmentDAO()
            assignment_subject_id = assignment_dao.find_subject_id(assignment_id)

            subject_dao = SubjectDAO()
            assignment_subject_name = subject_dao.find_subject(assignment_subject_id)

            assignment_title = assignment_dao.find_assignment_title(assignment_id)

            assignment_marks = assignment_dao.find_assignment_marks(assignment_id)

            if assignment_remarks == "":

                sender = "pythondemodonotreply@gmail.com"
                receiver = student_login_username
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = str(assignment_title) + " marks revealed!"

                msg.attach(MIMEText("You have " + str(assigned_marks) + " out "
                                                                      "of "
                                    + str(assignment_marks) + " in "
                                    + str(assignment_title) + " of " +
                                    str(assignment_subject_name) + ".",
                                    'plain'))
                print("msg!!\n",msg)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, "qazwsxedcrfvtgb1234567890")
                text = msg.as_string()
                server.sendmail(sender, receiver, text)
                server.quit()

            else:

                sender = "pythondemodonotreply@gmail.com"
                receiver = student_login_username
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = str(assignment_title) + " marks revealed!"

                msg.attach(MIMEText("You have " + str(assigned_marks) + " out "
                                                                        "of "
                                    + str(assignment_marks) + " in "
                                    + str(assignment_title) + " of " +
                                    str(assignment_subject_name) + "."
                                    "Other remarks : " +
                                    assignment_remarks,
                                    'plain'))

                print("msg!!\n", msg)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, "qazwsxedcrfvtgb1234567890")
                text = msg.as_string()
                server.sendmail(sender, receiver, text)
                server.quit()
            return redirect('/faculty/view_assignment_grades')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_update_assignment_grades route exception "
              "occured>>>>>>>>>>>>>", ex)


@app.route('/faculty/ajax_subject_assignment')
def faculty_ajax_subject_assignment():
    try:
        if admin_login_session() == "faculty":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_semester_id = request.args.get('assignmentSemesterId')
            subject_vo.subject_semester_id = subject_semester_id

            subject_vo_list = subject_dao.view_ajax_subject_faculty(subject_vo)
            ajax_assignment_subject = [i.as_dict() for i in subject_vo_list]
            return jsonify(ajax_assignment_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_ajax_subject_assignment route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/student/view_assignment')
def student_view_assignment():
    try:
        if admin_login_session() == "student":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing login id
            login_vo.login_username = request.cookies.get(
                'login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(
                student_vo)

            # bringing all the data
            assignment_vo.assignment_semester_id = student_semester_id
            assignment_vo_list = assignment_dao.student_view_assignment(
                assignment_vo)

            return render_template('student/viewassignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_view_assignment route exception occured>>>>>>>>>>",
              ex)


@app.route('/student/upload_assignment')
def student_upload_assignment():
    try:
        if admin_login_session() == "student":

            assignment_dao = AssignmentDAO()
            assignment_id = request.args.get('assignmentId')

            # bringing faculty degree & department data
            assignment_vo_list = assignment_dao.view_assignmentdata(
                assignment_id)

            return render_template('student/uploadAssignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "student_upload_assignment route exception occured>>>>>>>>>>",
            ex)


def add_assignment(assignment_image, student_id, assignment_faculty_id,
                   assignment_id, assignment_path, student_department,
                   student_enrollment, student_semester, assignment_subject):
    faculty_dao = FacultyDAO()
    assignment_dao = AssignmentDAO()
    login_dao = LoginDAO()
    student_assignment_vo = StudentAssignmentVO()
    student_assignment_dao = StudentAssignmentDAO()

    assignment_image_name = secure_filename(
        assignment_image.filename)

    assignment_image_path = os.path.join(
        app.config['STUDENT_ASSIGNMENT_FOLDER'] + assignment_path)

    assignment_image.save(
        os.path.join(assignment_image_path,
                     assignment_image_name))

    student_assignment_vo.st_assign_image_name = \
        assignment_image_name
    student_assignment_vo.st_assign_image_path = \
        assignment_image_path.replace(
            "base", "..")

    student_assignment_vo.st_assign_student_id = student_id
    student_assignment_vo.st_assignment_id = assignment_id
    student_assignment_vo.st_assign_faculty_id = \
        assignment_faculty_id

    student_assignment_dao.insert_student_assignment(student_assignment_vo)

    success_message = 'Assignment submitted ' \
                      'Successfully!'
    flash(success_message)

    faculty_login_id = faculty_dao.find_faculty_login_id(assignment_faculty_id)
    faculty_username = login_dao.find_login_username(faculty_login_id)

    assignment_title = assignment_dao.find_assignment_title(assignment_id)

    sender = "pythondemodonotreply@gmail.com"
    receiver = faculty_username
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = str(student_enrollment) + " has submitted " + \
                     str(assignment_title)
    msg.attach(MIMEText(str(student_enrollment) + " of semester " +
                        str(student_semester) + " of department " +
                        str(student_department) + " has "
                                                  "submitted " +
                        str(assignment_title) + " of subject " +
                        str(assignment_subject), 'plain'))

    filename = assignment_image_name
    attachment = open(assignment_image_path + assignment_image_name, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "qazwsxedcrfvtgb1234567890")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


@app.route('/student/insert_assignment', methods=['GET', 'POST'])
def student_insert_assignment():
    try:
        if admin_login_session() == "student":
            assignment_id = request.args.get('assignmentId')

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            semester_dao = SemesterDAO()
            department_dao = DepartmentDAO()
            subject_dao = SubjectDAO()
            assignment_dao = AssignmentDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get(
                'login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)
            student_enrollment = student_dao.find_student_enrollment(
                student_id)

            # bringing department id
            student_vo.student_id = student_id
            student_department_id = student_dao.find_department_id(
                student_vo)

            # department name
            student_department = department_dao.find_department(
                student_department_id)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(
                student_vo)

            # Semester number
            student_semester = semester_dao.find_semester(student_semester_id)

            assignment_subject_id = assignment_dao.find_subject_id(
                assignment_id)

            # Subject name
            assignment_subject = subject_dao.find_subject(
                assignment_subject_id)

            assignment_faculty_id = assignment_dao.find_faculty(assignment_id)

            if request.method == 'POST':
                assignment_image = request.files.get('assignmentFile')

                if os.path.exists(
                                'base/static/studentResources/assignments/' +
                                student_department) == False:
                    os.mkdir('base/static/studentResources/assignments/' +
                             student_department)

                if os.path.exists(
                        'base/static/studentResources/assignments/{}/{}'.format(
                            student_department, student_semester)) == False:
                    os.mkdir(
                        'base/static/studentResources/assignments/{}/{}'.format(
                            student_department, student_semester))

                if os.path.exists(
                        'base/static/studentResources/assignments/{}/{}/{}'.format(
                            student_department,
                            student_semester, assignment_subject)) == False:
                    os.mkdir(
                        'base/static/studentResources/assignments/{}/{}/{}'.format(
                            student_department,
                            student_semester, assignment_subject))

                if os.path.exists(
                        'base/static/studentResources/assignments/{}/{}/{}/{}'.format(
                            student_department,
                            student_semester, assignment_subject,
                            student_enrollment)) == False:

                    print("in")
                    os.mkdir(
                        'base/static/studentResources/assignments/{}/{}/{}/{}'.format(
                            student_department,
                            student_semester, assignment_subject,
                            student_enrollment))

                    assignment_path = '{}/{}/{}/{}/'.format(
                        student_department,
                        student_semester, assignment_subject,
                        student_enrollment)

                    add_assignment(assignment_image, student_id,
                                   assignment_faculty_id, assignment_id,
                                   assignment_path, student_department,
                                   student_enrollment, student_semester,
                                   assignment_subject)
                else:

                    assignment_path = '{}/{}/{}/{}/'.format(
                        student_department,
                        student_semester, assignment_subject,
                        student_enrollment)

                    add_assignment(assignment_image, student_id,
                                   assignment_faculty_id, assignment_id,
                                   assignment_path, student_department,
                                   student_enrollment, student_semester,
                                   assignment_subject)

            return redirect('/student/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "student_insert_assignment route exception occured>>>>>>>>>>",
            ex)



        # @app.route('/faculty/ajax_department_assignment')
        # def faculty_ajax_department_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             department_vo = DepartmentVO()
        #             department_dao = DepartmentDAO()
        #             department_degree_id = request.args.get('assignmentDegreeId')
        #             department_vo.department_degree_id = department_degree_id
        #
        #             department_vo_list = department_dao.view_ajax_department(
        #                 department_vo)
        #             ajax_assignment_department = [i.as_dict() for i in
        #                                           department_vo_list]
        #             return jsonify(ajax_assignment_department)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_department_assignment route exception "
        #               "occured>>>>>>>>>>", ex)
        #
        #
        # @app.route('/faculty/ajax_subject_assignment')
        # def faculty_ajax_subject_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             subject_vo = SubjectVO()
        #             subject_dao = SubjectDAO()
        #             subject_department_id = request.args.get('assignmentDepartmentId')
        #             subject_vo.subject_department_id = subject_department_id
        #
        #             subject_vo_list = subject_dao.view_ajax_subject(subject_vo)
        #             ajax_assignment_subject = [i.as_dict() for i in subject_vo_list]
        #             return jsonify(ajax_assignment_subject)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_subject_assignment route exception "
        #               "occured>>>>>>>>>>", ex)
        #
        #
        # @app.route('/faculty/ajax_faculty_assignment')
        # def faculty_ajax_faculty_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             faculty_vo = FacultyVO()
        #             faculty_dao = FacultyDAO()
        #             faculty_subject_id = request.args.get('assignmentSubjectId')
        #             faculty_vo.faculty_subject_id = faculty_subject_id
        #
        #             faculty_vo_list = faculty_dao.view_ajax_faculty(faculty_vo)
        #             ajax_assignment_faculty = [i.as_dict() for i in faculty_vo_list]
        #             return jsonify(ajax_assignment_faculty)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_faculty_assignment route exception "
        #               "occured>>>>>>>>", ex)
        #
        #


@app.route('/student/view_submitted_assignments')
def student_view_submitted_assignments():
    try:
        if admin_login_session() == "student":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing login id
            login_vo.login_username = request.cookies.get(
                'login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(
                student_vo)

            # bringing all the data
            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()
            st_assignment_vo.st_assign_student_id = student_id
            assignment_vo_list = st_assignment_dao.student_view_assignment_grades(
                st_assignment_vo)
            print("assignment_vo_list!!>>>>>>>>>>>>>>>",assignment_vo_list)

            return render_template('student/viewSubmittedAssignments.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            admin_logout_session()
    except Exception as ex:
        print("student_view_submitted_assignments exception "
              "occured>>>>>>>>>>>>>>>>>",ex)

@app.route('/student/delete_assignment')
def student_delete_assignment():
    try:
        if admin_login_session() == "student":
            st_assignment_vo = StudentAssignmentVO()
            st_assignment_dao = StudentAssignmentDAO()

            # deleting assignment data from database
            st_assign_id = request.args.get('assignmentId')
            st_assign_marks = st_assignment_dao.find_assign_marks(st_assign_id)

            if st_assign_marks == None:
                st_assignment_vo.st_assign_id = st_assign_id
                assignment_vo_list = st_assignment_dao.delete_assignment_grades(st_assignment_vo)

                # deleting assignment file
                file_path = assignment_vo_list.st_assign_image_path.replace(
                    "..", "base") + assignment_vo_list.st_assign_image_name
                os.remove(file_path)

                success_message = 'Record Deleted Successfully!'
                flash(success_message)
            else:
                fail_message = 'Sorry! You cannot delete this assignment ' \
                            'because ' \
                    'marks have already been assigned!'
                flash(fail_message)

            return redirect('/student/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_delete_assignment route exception occured>>>>>>>>>>",
              ex)
