import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_logout_session, \
    admin_login_session
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.student_vo import StudentVO
from base.com.vo.subject_vo import SubjectVO

login_secretkey = ""
FACULTY_FOLDER = 'base/static/adminResources/faculty/'
app.config['FACULTY_FOLDER'] = FACULTY_FOLDER


@app.route('/admin/load_faculty')
def admin_load_faculty():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_dao_list = degree_dao.view_degree()

            return render_template('admin/addFaculty.html',
                                   degree_dao_list=degree_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_department_faculty')
def admin_ajax_department_faculty():
    try:
        if admin_login_session() == "admin":
            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()
            department_degree_id = request.args.get('facultyDegreeId')
            department_vo.department_degree_id = department_degree_id
            department_vo_list = department_dao.view_ajax_department(
                department_vo)
            ajax_faculty_department = [i.as_dict() for i in department_vo_list]
            return jsonify(ajax_faculty_department)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_department_Faculty route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_subject_faculty')
def admin_ajax_subject_faculty():
    try:
        if admin_login_session() == "admin":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_department_id = request.args.get('facultyDepartmentId')
            subject_vo.subject_department_id = subject_department_id
            subject_vo_list = subject_dao.view_ajax_subject(subject_vo)
            ajax_faculty_subject = [i.as_dict() for i in subject_vo_list]
            return jsonify(ajax_faculty_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_Subject_Faculty route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/admin/insert_faculty', methods=['POST'])
def admin_insert_faculty():
    try:
        if admin_login_session() == "admin":
            global login_secretkey
            global login_secretkey_flag
            login_secretkey_flag = False

            login_dao = LoginDAO()
            login_vo = LoginVO()

            faculty_dao = FacultyDAO()
            faculty_vo = FacultyVO()

            faculty_degree_id = request.form.get('facultyDegreeId')
            faculty_department_id = request.form.get('facultyDepartmentId')
            faculty_subject_id = request.form.get('facultySubjectId')
            login_username = request.form.get('loginId')
            faculty_firstname = request.form.get('facultyFirstName')
            faculty_lastname = request.form.get('facultyLastName')
            faculty_gender = request.form.get('facultyGender')
            faculty_qualification = request.form.get('facultyQualification')
            faculty_teaching_experience = request.form.get(
                'facultyTeachingExperience')
            faculty_contact = request.form.get('facultyContact')
            faculty_hod = request.form.get('facultyHod')
            faculty_image = request.files.get('facultyImage')
            faculty_image_name = secure_filename(faculty_image.filename)
            faculty_image_path = os.path.join(app.config['FACULTY_FOLDER'])
            faculty_image.save(
                os.path.join(faculty_image_path, faculty_image_name))

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
            server.sendmail(sender, receiver, text)
            server.quit()

            login_vo.login_username = login_username
            login_vo.login_password = login_password
            login_vo.login_role = "faculty"
            login_vo.login_status = True
            login_vo.login_secretkey = login_secretkey
            login_dao.insert_login(login_vo)

            faculty_vo.faculty_degree_id = faculty_degree_id
            faculty_vo.faculty_department_id = faculty_department_id
            faculty_vo.faculty_subject_id = faculty_subject_id
            faculty_vo.faculty_login_id = login_vo.login_id
            faculty_vo.faculty_firstname = faculty_firstname
            faculty_vo.faculty_lastname = faculty_lastname
            faculty_vo.faculty_gender = faculty_gender
            faculty_vo.faculty_qualification = faculty_qualification
            faculty_vo.faculty_teaching_experience = faculty_teaching_experience
            faculty_vo.faculty_contact = faculty_contact

            if faculty_hod == "Yes":
                faculty_vo.faculty_hod = True
            elif faculty_hod == "No":
                faculty_vo.faculty_hod = False

            faculty_vo.faculty_image_name = faculty_image_name
            faculty_vo.faculty_image_path = faculty_image_path.replace("base",
                                                                       "..")

            faculty_dao.insert_faculty(faculty_vo)

            return redirect('/admin/view_faculty')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_faculty')
def admin_view_faculty():
    try:
        if admin_login_session() == "admin":
            faculty_dao = FacultyDAO()
            faculty_vo_list = faculty_dao.view_faculty()
            return render_template('admin/viewFaculty.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_faculty', methods=['GET'])
def admin_delete_faculty():
    try:
        if admin_login_session() == "admin":
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()

            faculty_id = request.args.get('facultyId')
            faculty_vo.faculty_id = faculty_id
            faculty_vo_list = faculty_dao.delete_faculty(faculty_vo)
            file_path = faculty_vo_list.faculty_image_path.replace("..",
                                                                   "base") + faculty_vo_list.faculty_image_name
            os.remove(file_path)

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_dao.delete_login(login_vo)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_faculty')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_faculty')
def admin_edit_faculty():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            login_dao = LoginDAO()
            login_vo_list = login_dao.view_login()

            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            faculty_id = request.args.get('facultyId')
            faculty_vo.faculty_id = faculty_id
            faculty_vo_list = faculty_dao.edit_faculty(faculty_vo)
            return render_template('admin/editFaculty.html',
                                   degree_vo_list=degree_vo_list,
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_faculty', methods=['POST'])
def admin_update_faculty():
    try:
        if admin_login_session() == "admin":
            faculty_id = request.form.get('facultyId')
            faculty_degree_id = request.form.get('facultyDegreeId')
            faculty_department_id = request.form.get('facultyDepartmentId')
            faculty_subject_id = request.form.get('facultySubjectId')
            faculty_firstname = request.form.get('facultyFirstName')
            faculty_lastname = request.form.get('facultyLastName')
            faculty_gender = request.form.get('facultyGender')
            faculty_qualification = request.form.get('facultyQualification')
            faculty_teaching_experience = request.form.get(
                'facultyTeachingExperience')
            faculty_contact = request.form.get('facultyContact')
            faculty_hod = request.form.get('facultyHod')
            # faculty_image_name = request.form.get('')
            # faculty_image_path = request.form.get('')

            faculty_dao = FacultyDAO()
            faculty_vo = FacultyVO()

            faculty_vo.faculty_id = faculty_id
            faculty_vo.faculty_degree_id = faculty_degree_id
            faculty_vo.faculty_department_id = faculty_department_id
            faculty_vo.faculty_subject_id = faculty_subject_id
            faculty_vo.faculty_firstname = faculty_firstname
            faculty_vo.faculty_lastname = faculty_lastname
            faculty_vo.faculty_gender = faculty_gender
            faculty_vo.faculty_qualification = faculty_qualification
            faculty_vo.faculty_teaching_experience = faculty_teaching_experience
            faculty_vo.faculty_contact = faculty_contact

            if faculty_hod == "Yes":
                faculty_vo.faculty_hod = True
            elif faculty_hod == "No":
                faculty_vo.faculty_hod = False

            faculty_dao.update_faculty(faculty_vo)
            return redirect('/admin/view_faculty')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_Faculty route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/view_profile')
def faculty_view_profile():
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
            # faculty_vo.faculty_id = faculty_id
            # faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)
            return render_template('faculty/viewProfile.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_view_profile route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/edit_profile')
def faculty_edit_profile():
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

            # bringing subjects based on department id
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_vo.subject_department_id = faculty_department_id
            subject_dao_list = subject_dao.view_ajax_subject(subject_vo)

            return render_template('faculty/editProfile.html',
                                   subject_dao_list=subject_dao_list,
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_profile route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/update_profile', methods=['POST'])
def faculty_update_profile():
    try:
        if admin_login_session() == "faculty":
            faculty_id = request.form.get('facultyId')
            # faculty_degree_id = request.form.get('facultyDegreeId')
            # faculty_department_id = request.form.get('facultyDepartmentId')
            faculty_subject_id = request.form.get('facultySubjectId')
            faculty_firstname = request.form.get('facultyFirstName')
            faculty_lastname = request.form.get('facultyLastName')
            faculty_gender = request.form.get('facultyGender')
            faculty_qualification = request.form.get('facultyQualification')
            faculty_teaching_experience = request.form.get(
                'facultyTeachingExperience')
            faculty_contact = request.form.get('facultyContact')
            faculty_hod = request.form.get('facultyHod')

            faculty_dao = FacultyDAO()
            faculty_vo = FacultyVO()

            faculty_vo.faculty_id = faculty_id
            # faculty_vo.faculty_degree_id = faculty_degree_id
            # faculty_vo.faculty_department_id = faculty_department_id
            faculty_vo.faculty_subject_id = faculty_subject_id
            faculty_vo.faculty_firstname = faculty_firstname
            faculty_vo.faculty_lastname = faculty_lastname
            faculty_vo.faculty_gender = faculty_gender
            faculty_vo.faculty_qualification = faculty_qualification
            faculty_vo.faculty_teaching_experience = faculty_teaching_experience
            faculty_vo.faculty_contact = faculty_contact

            if faculty_hod == "Yes":
                faculty_vo.faculty_hod = True
            elif faculty_hod == "No":
                faculty_vo.faculty_hod = False

            faculty_dao.update_faculty(faculty_vo)
            return redirect('/faculty/view_profile')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_update_profile route exception occured>>>>>>>>>>", ex)


@app.route('/student/load_faculty')
def student_load_faculty():
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

            return render_template('student/viewFaculty.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_faculty route exception occured>>>>>>>>>>", ex)


@app.route('/student/load_faculty_profile')
def student_load_faculty_profile():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            faculty_dao = FacultyDAO()

            # bringing student login id
            # login_vo.login_username = request.cookies.get('login_username')
            # student_login_id = login_dao.find_login_id(login_vo)
            #
            # # bringing student id
            # student_vo.student_login_id = student_login_id
            # student_id = student_dao.find_student_id(student_vo)
            #
            # # bringing department id
            # student_vo.student_id = student_id
            # student_department_id = student_dao.find_department_id(student_vo)

            # faculty_id = faculty_dao.find_faculty(student_department_id)

            faculty_id = request.args.get('facultyId')
            print("faculty_id>>>>>>>>>>", faculty_id)

            # bringing faculty degree & department data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)
            print("faculty_vo_list>>>>>>>>>>>", faculty_vo_list)

            return render_template('student/viewFacultyProfile.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_teacher_profile route exception occured>>>>>>>>>>",
              ex)
