import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_dao import StudentDAO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_vo import StudentVO

login_secretkey = ""
STUDENT_FOLDER = 'base/static/adminResources/student/'
app.config['STUDENT_FOLDER'] = STUDENT_FOLDER


@app.route('/admin/load_student', methods=['GET'])
def admin_load_student():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_dao_list = degree_dao.view_degree()

            return render_template('admin/addStudent.html',
                                   degree_dao_list=degree_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Student route exception occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_department_student')
def admin_ajax_department_student():
    try:
        if admin_login_session() == "admin":
            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()
            department_degree_id = request.args.get('studentDegreeId')
            department_vo.department_degree_id = department_degree_id
            department_vo_list = department_dao.view_ajax_department(
                department_vo)
            ajax_student_department = [i.as_dict() for i in department_vo_list]
            return jsonify(ajax_student_department)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_department_student route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_semester_student')
def admin_ajax_semester_student():
    try:
        if admin_login_session() == "admin":
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_department_id = request.args.get('studentDepartmentId')
            semester_vo.semester_department_id = semester_department_id
            semester_vo_list = semester_dao.view_ajax_semester(semester_vo)
            ajax_student_semester = [i.as_dict() for i in semester_vo_list]
            return jsonify(ajax_student_semester)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_semester_student route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/admin/insert_student', methods=['POST'])
def admin_insert_student():
    try:
        if admin_login_session() == "admin":
            global login_secretkey
            global login_secretkey_flag
            login_secretkey_flag = False

            login_dao = LoginDAO()
            login_vo = LoginVO()

            student_dao = StudentDAO()
            student_vo = StudentVO()

            student_degree_id = request.form.get('studentDegreeId')
            student_department_id = request.form.get('studentDepartmentId')
            student_semester_id = request.form.get('studentSemesterId')
            login_username = request.form.get('loginId')
            student_enrollment = request.form.get('studentEnrollment')
            student_firstname = request.form.get('studentFirstname')
            student_lastname = request.form.get('studentLastname')
            student_gender = request.form.get('studentGender')
            student_contact = request.form.get('studentContact')
            student_parent_contact = request.form.get('studentParentContact')
            student_dob = request.form.get('studentDob')
            student_qualification = request.form.get('studentQualification')
            student_status = request.form.get('studentStatus')
            student_image = request.files.get('studentImage')
            student_image_name = secure_filename(student_image.filename)
            student_image_path = os.path.join(app.config['STUDENT_FOLDER'])
            student_image.save(
                os.path.join(student_image_path, student_image_name))

            login_vo_list = login_dao.view_login()
            login_secretkey_list = [i.as_dict()['login_secretkey'] for i in
                                    login_vo_list]
            login_username_list = [i.as_dict()['login_username'] for i in
                                   login_vo_list]

            if login_username in login_username_list:
                error_message = "The username is already exists !"
                flash(error_message)
                return render_template('admin/register.html')

            while not login_secretkey_flag:
                login_secretkey = ''.join(
                    (random.choice(string.ascii_letters + string.digits)) for x
                    in
                    range(32))
                if login_secretkey not in login_secretkey_list:
                    login_secretkey_flag = True
                    break

            login_password = ''.join(
                (random.choice(string.ascii_letters + string.digits)) for x in
                range(8))

            sender = "pythondemodonotreply@gmail.com"
            receiver = login_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "YOUR SYSTEM GENERATED LOGIN PASSWORD IS:"
            msg.attach(MIMEText(login_password, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "qazwsxedcrfvtgb1234567890")
            text = msg.as_string()
            print("sender : ", sender)
            print("receiver : ", receiver)
            print("text : ", text)
            server.sendmail(sender, receiver, text)
            server.quit()

            login_vo.login_username = login_username
            login_vo.login_password = login_password
            login_vo.login_role = "student"
            login_vo.login_status = True
            login_vo.login_secretkey = login_secretkey
            login_dao.insert_login(login_vo)

            student_vo.student_degree_id = student_degree_id
            student_vo.student_department_id = student_department_id
            student_vo.student_semester_id = student_semester_id
            student_vo.student_login_id = login_vo.login_id
            student_vo.student_enrollment = student_enrollment
            student_vo.student_firstname = student_firstname
            student_vo.student_lastname = student_lastname
            student_vo.student_gender = student_gender
            student_vo.student_contact = student_contact
            student_vo.student_parent_contact = student_parent_contact
            student_vo.student_dob = student_dob
            student_vo.student_qualification = student_qualification
            student_vo.student_status = student_status
            student_vo.student_image_name = student_image_name
            student_vo.student_image_path = student_image_path.replace("base",
                                                                       "..")

            student_dao.insert_student(student_vo)

            return redirect('/admin/view_student')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_student', methods=['GET'])
def admin_view_student():
    try:
        if admin_login_session() == "admin":
            student_dao = StudentDAO()
            student_vo_list = student_dao.view_student()
            return render_template('admin/viewStudent.html',
                                   student_vo_list=student_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Student route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/view_student', methods=['GET'])
def faculty_view_student():
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

            student_dao = StudentDAO()
            student_vo_list = student_dao.view_studentdata(
                faculty_department_id)
            return render_template('faculty/viewStudent.html',
                                   student_vo_list=student_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Student route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_student', methods=['GET'])
def admin_delete_student():
    try:
        if admin_login_session() == "admin":
            student_vo = StudentVO()
            student_dao = StudentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()

            student_id = request.args.get('studentId')
            student_vo.student_id = student_id
            student_vo_list = student_dao.delete_student(student_vo)
            file_path = student_vo_list.student_image_path.replace("..",
                                                                   "base") + student_vo_list.student_image_name
            os.remove(file_path)

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_dao.delete_login(login_vo)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_student')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_student route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_student')
def admin_edit_student():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            login_dao = LoginDAO()
            login_vo_list = login_dao.view_login()

            student_vo = StudentVO()
            student_dao = StudentDAO()

            student_id = request.args.get('studentId')
            student_vo.student_id = student_id
            student_vo_list = student_dao.edit_student(student_vo)
            return render_template('admin/editStudent.html',
                                   degree_vo_list=degree_vo_list,
                                   login_vo_list=login_vo_list,
                                   student_vo_list=student_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_Student route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_student', methods=['POST'])
def admin_update_student():
    try:
        if admin_login_session() == "admin":
            student_dao = StudentDAO()
            student_vo = StudentVO()

            student_id = request.form.get('studentId')
            student_degree_id = request.form.get('studentDegreeId')
            student_department_id = request.form.get('studentDepartmentId')
            student_semester_id = request.form.get('studentSemesterId')
            student_enrollment = request.form.get('studentEnrollment')
            student_firstname = request.form.get('studentFirstname')
            student_lastname = request.form.get('studentLastname')
            student_gender = request.form.get('studentGender')
            student_contact = request.form.get('studentContact')
            student_parent_contact = request.form.get('studentParentContact')
            student_dob = request.form.get('studentDob')
            student_qualification = request.form.get('studentQualification')
            student_status = request.form.get('studentStatus')

            student_vo.student_id = student_id
            student_vo.student_degree_id = student_degree_id
            student_vo.student_department_id = student_department_id
            student_vo.student_semester_id = student_semester_id
            student_vo.student_enrollment = student_enrollment
            student_vo.student_firstname = student_firstname
            student_vo.student_lastname = student_lastname
            student_vo.student_gender = student_gender
            student_vo.student_contact = student_contact
            student_vo.student_parent_contact = student_parent_contact
            student_vo.student_dob = student_dob
            student_vo.student_qualification = student_qualification
            student_vo.student_status = student_status

            student_dao.update_student(student_vo)
            return redirect('/admin/view_student')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_Student route exception occured>>>>>>>>>>", ex)


@app.route('/student/view_profile')
def student_view_profile():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing faculty degree & department data
            student_vo_list = student_dao.load_studentdata(student_id)
            print("student_vo_list>>>>>>>>>>>>>", student_vo_list)
            return render_template('student/viewProfile.html',
                                   student_vo_list=student_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_view_profile route exception occured>>>>>>>>>>", ex)


@app.route('/student/edit_profile')
def student_edit_profile():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing faculty degree & department data
            student_vo_list = student_dao.load_studentdata(student_id)

            return render_template('student/editProfile.html',
                                   student_vo_list=student_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_edit_profile route exception occured>>>>>>>>>>", ex)


@app.route('/student/update_profile', methods=['POST'])
def student_update_profile():
    try:
        if admin_login_session() == "student":
            student_id = request.form.get('studentId')
            # student_firstname = request.form.get('studentFirstName')
            # student_lastname = request.form.get('studentLastName')
            student_gender = request.form.get('studentGender')
            student_qualification = request.form.get('studentQualification')
            student_parent_contact = request.form.get(
                'studentParentContact')
            student_contact = request.form.get('studentContact')
            student_dob = request.form.get('studentDob')
            # student_enrollment = request.form.get('studentEnrollment')

            student_dao = StudentDAO()
            student_vo = StudentVO()

            student_vo.student_id = student_id
            # student_vo.student_firstname = student_firstname
            # student_vo.student_lastname = student_lastname
            student_vo.student_gender = student_gender
            student_vo.student_qualification = student_qualification
            student_vo.student_parent_contact = student_parent_contact
            student_vo.student_contact = student_contact
            student_vo.student_dob = student_dob
            # student_vo.student_enrollment = student_enrollment

            student_dao.update_student(student_vo)
            return redirect('/student/view_profile')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_update_profile route exception occured>>>>>>>>>>", ex)


@app.route('/student/about')
def student_about():
    try:
        if admin_login_session() == "student":
            return render_template("student/about.html")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_about route exception occured>>>>>>>>>>", ex)


@app.route('/student/contact')
def student_contact():
    try:
        if admin_login_session() == "student":
            return render_template("student/contact-style-one.html")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_contact route exception occured>>>>>>>>>>", ex)
