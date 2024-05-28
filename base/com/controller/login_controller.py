from datetime import timedelta

from flask import render_template, redirect, request, url_for, make_response, \
    flash,session

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from base import app
from base.com.dao.assignment_dao import AssignmentDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.exam_dao import ExamDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.lecture_dao import LectureDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.exam_vo import ExamVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.lecture_vo import LectureVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.student_vo import StudentVO

global_loginvo_list = []
global_login_secretkey_set = {0}


@app.route('/')
def admin_load_home():
    try:
        return render_template('admin/homepage.html')
    except Exception as ex:
        print("admin_load_home route exception occured>>>>>>>>>>", ex)


@app.route('/about')
def admin_load_about():
    try:
        return render_template('admin/about.html')
    except Exception as ex:
        print("admin_load_about route exception occured>>>>>>>>>>", ex)


@app.route('/contact')
def admin_load_contact():
    try:
        return render_template('admin/contact.html')
    except Exception as ex:
        print("admin_load_contact route exception occured>>>>>>>>>>", ex)


@app.route('/login', methods=['GET'])
def admin_load_login():
    try:
        return render_template('admin/login-2.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/validate_login', methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_username = request.form.get('loginUsername')
        login_password = request.form.get('loginPassword')

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username

        login_vo_list = login_dao.check_login_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect('/login')
        elif not login_list[0]['login_status']:
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect('/login')
        else:
            login_id = login_list[0]['login_id']
            login_username = login_list[0]['login_username']
            login_role = login_list[0]['login_role']
            login_secretkey = login_list[0]['login_secretkey']
            database_login_password = login_list[0]['login_password']
            if login_password == database_login_password:
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username,
                                      'login_role': login_role,
                                      'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        temp_list = list(i.keys())
                        global_login_secretkey_set.add(temp_list[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(
                        redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                elif login_role == 'faculty':
                    response = make_response(
                        redirect(url_for('faculty_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                elif login_role == 'student':
                    response = make_response(
                        redirect(url_for('student_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))
            else:
                error_message = 'password is incorrect !'
                flash(error_message)
                return redirect('/login')
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            degree_length = len(degree_vo_list)

            department_dao = DepartmentDAO()
            department_vo_list = department_dao.view_department()
            department_length = len(department_vo_list)

            semester_dao = SemesterDAO()
            semester_vo_list = semester_dao.view_semester()
            semester_length = len(semester_vo_list)

            subject_dao = SubjectDAO()
            subject_vo_list = subject_dao.view_subject()
            subject_length = len(subject_vo_list)

            faculty_dao = FacultyDAO()
            faculty_vo_list = faculty_dao.view_faculty()
            faculty_length = len(faculty_vo_list)

            student_dao = StudentDAO()
            student_vo_list = student_dao.view_student()
            student_length = len(student_vo_list)

            login_username = request.cookies.get('login_username')
            return render_template('admin/index.html',
                                   login_username=login_username,
                                   degree_length=degree_length,
                                   department_length=department_length,
                                   semester_length=semester_length,
                                   subject_length=subject_length,
                                   faculty_length=faculty_length,
                                   student_length=student_length)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/load_dashboard', methods=['GET'])
def faculty_load_dashboard():
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

            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing assignment data based on faculty id
            assignment_vo = AssignmentVO()
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_dao = AssignmentDAO()
            assignment_vo_list = assignment_dao.faculty_view_assignment(
                assignment_vo)
            assignment_length = len(assignment_vo_list)

            lecture_vo = LectureVO()
            lecture_vo.lecture_faculty_id = faculty_id
            lecture_dao = LectureDAO()
            lecture_vo_list = lecture_dao.faculty_view_lecture(lecture_vo)
            lecture_length = len(lecture_vo_list)

            exam_vo = ExamVO()
            exam_vo.exam_faculty_id = faculty_id
            exam_dao = ExamDAO()
            exam_vo_list = exam_dao.faculty_view_exam(exam_vo)
            exam_length = len(exam_vo_list)

            student_dao = StudentDAO()
            student_vo_list = student_dao.view_studentdata(
                faculty_department_id)
            student_length = len(student_vo_list)

            return render_template('faculty/index.html',
                                   assignment_length=assignment_length,
                                   lecture_length=lecture_length,
                                   exam_length=exam_length,
                                   student_length=student_length)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/student/load_dashboard', methods=['GET'])
def student_load_dashboard():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            faculty_dao = FacultyDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing department id
            student_vo.student_id = student_id
            student_department_id = student_dao.find_department_id(student_vo)

            faculty_vo_list = faculty_dao.find_facultydata(
                student_department_id)

            return render_template('student/index.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/admin/login_session')
def admin_login_session():
    try:
        global global_loginvo_list
        login_role_flag = ""
        login_secretkey = request.cookies.get('login_secretkey')
        if login_secretkey is None:
            return redirect('/login')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'faculty':
                    login_role_flag = "faculty"
                elif i[login_secretkey]['login_role'] == 'student':
                    login_role_flag = "student"
        return login_role_flag
    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    break
        return response
    except Exception as ex:
        print("admin_logout_session route exception occured>>>>>>>>>>", ex)

@app.route('/load_forget_password')
def load_forget_password():
    try:
        return render_template('admin/forgetPassword.html')
    except Exception as ex:
        print("load_forget_password route exception occured>>>>>>>>>>", ex)


@app.route('/validate_login_username', methods=['post'])
def validate_login_username():
    try:
        login_username = request.form.get("loginUsername")
        login_dao = LoginDAO()
        login_vo = LoginVO()

        login_vo.login_username = login_username
        login_vo_list = login_dao.login_validate_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'Username is incorrect !'
            flash(error_message)
            return redirect(url_for('student_load_forget_password'))
        else:
            login_id = login_list[0]['login_id']
            session['session_login_id'] = login_id
            login_username = login_list[0]['login_username']
            sender = "pythondemodonotreply@gmail.com"
            receiver = login_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "YOUR ONE TIME PASSWORD IS.."
            otp = random.randint(1000, 9999)
            session['session_otp_number'] = otp
            message = str(otp)
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "qazwsxedcrfvtgb1234567890")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()
            return render_template('admin/otpValidation.html')
    except Exception as ex:
        print("validate_login_username route exception occured>>>>>>>>>>", ex)


@app.route('/validate_otp_number', methods=['POST'])
def validate_otp_number():
    try:
        otp_number = int(request.form.get("otpNumber"))
        session_otp_number = session.get('session_otp_number')
        if otp_number == session_otp_number:
            return render_template('admin/resetPassword.html')
        else:
            session.clear()
            error_message = 'otp is incorrect !'
            flash(error_message)
            return redirect(url_for('load_forget_password'))
    except Exception as ex:
        print("validate_otp_number route exception occured>>>>>>>>>>", ex)


@app.route('/insert_reset_password', methods=['POST'])
def insert_reset_password():
    try:
        login_password = request.form.get("loginPassword")
        login_id = session.get("session_login_id")
        login_dao = LoginDAO()
        login_vo = LoginVO()
        login_vo.login_id = login_id
        login_vo.login_password = login_password
        login_dao.update_login(login_vo)
        return redirect('/')
    except Exception as ex:
        print("insert_reset_password route exception occured>>>>>>>>>>", ex)