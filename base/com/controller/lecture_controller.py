from flask import render_template, request, redirect, jsonify,flash

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.lecture_dao import LectureDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.dao.student_dao import StudentDAO
from base.com.vo.student_vo import StudentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.lecture_vo import LectureVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


@app.route('/faculty/load_lecture')
def faculty_load_lecture():
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

            # bringing department id
            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing semester based on department id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_department_id = faculty_department_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            return render_template('faculty/addLectureSchedule.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_load_lecture route exception occured>>>>>>>>>>>>>>", ex)


@app.route('/faculty/insert_lecture', methods=['POST'])
def faculty_insert_lecture():
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

            # bringing lecture data from ui
            lecture_semester_id = request.form.get('lectureSemesterId')
            lecture_subject_id = request.form.get('lectureSubjectId')
            lecture_date = request.form.get('lectureDate')
            lecture_day = request.form.get('lectureDay')
            lecture_start_time = request.form.get('lectureStartTime')
            lecture_end_time = request.form.get('lectureEndTime')

            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            # storing all the data in database
            lecture_vo.lecture_semester_id = lecture_semester_id
            lecture_vo.lecture_subject_id = lecture_subject_id
            lecture_vo.lecture_semester_id = lecture_semester_id
            lecture_vo.lecture_faculty_id = faculty_id
            lecture_vo.lecture_date = lecture_date
            lecture_vo.lecture_day = lecture_day
            lecture_vo.lecture_start_time = lecture_start_time
            lecture_vo.lecture_end_time = lecture_end_time

            lecture_dao.insert_lecture(lecture_vo)
            return redirect('/faculty/view_lecture')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_load_lecture route exception occured>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/ajax_subject_lecture')
def faculty_ajax_subject_lecture():
    try:
        if admin_login_session() == "faculty":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_semester_id = request.args.get('lectureSemesterId')
            print("subject_semester_id>>>>>", subject_semester_id)
            subject_vo.subject_semester_id = subject_semester_id

            subject_vo_list = subject_dao.view_ajax_subject_faculty(subject_vo)
            ajax_lecture_subject = [i.as_dict() for i in subject_vo_list]
            return jsonify(ajax_lecture_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_ajax_subject_lecture route exception "
              "occured>>>>>>>>>>>>>>", ex)


@app.route('/student/ajax_semester_subject')
def student_ajax_semester_subject():
    try:
        if admin_login_session() == "student":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_semester_id = request.args.get('subjectSemesterId')
            print("subject_semester_id>>>>>", subject_semester_id)
            subject_vo.subject_semester_id = subject_semester_id

            subject_vo_list = subject_dao.view_ajax_subject_faculty(subject_vo)
            print("subject_vo_list>>>>>", subject_vo_list)

            ajax_lecture_subject = [i.as_dict() for i in subject_vo_list]
            print("ajax_lecture_subject>>>>>", ajax_lecture_subject)
            return jsonify(ajax_lecture_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_ajax_subject_lecture route exception "
              "occured>>>>>>>>>>>>>>", ex)


@app.route('/faculty/view_lecture')
def faculty_view_lecture():
    try:
        if admin_login_session() == "faculty":
            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing all the data
            lecture_vo.lecture_faculty_id = faculty_id
            lecture_vo_list = lecture_dao.faculty_view_lecture(
                lecture_vo)

            return render_template('faculty/viewLectureSchedule.html',
                                   lecture_vo_list=lecture_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_view_lecture route exception occured>>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/delete_lecture')
def faculty_delete_lecture():
    try:
        if admin_login_session() == "faculty":
            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            # deleting all the data
            lecture_id = request.args.get('lectureId')
            lecture_vo.lecture_id = lecture_id
            lecture_dao.delete_lecture(lecture_vo)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/faculty/view_lecture')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_delete_lecture route exception "
              "occured>>>>>>>>>>>>>>>>", ex)


@app.route('/faculty/edit_lecture')
def faculty_edit_lecture():
    try:
        if admin_login_session() == "faculty":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty login id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            # bringing department id
            faculty_vo.faculty_id = faculty_id
            faculty_department_id = faculty_dao.find_department_id(faculty_vo)

            # bringing faculty degree & department data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing subjects based on department id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_department_id = faculty_department_id
            semester_vo_list = semester_dao.view_ajax_semester(semester_vo)

            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            # bringing all the data to edit
            lecture_id = request.args.get('lectureId')
            lecture_vo.lecture_id = lecture_id
            lecture_vo_list = lecture_dao.edit_lecture(lecture_vo)
            return render_template('faculty/editLectureSchedule.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_vo_list=semester_vo_list,
                                   lecture_vo_list=lecture_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_lecture route excepton occured>>>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/update_lecture', methods=['POST'])
def faculty_update_lecture():
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

            # bringing all the data from ui
            lecture_id = request.form.get('lectureId')
            lecture_degree_id = request.form.get('lectureDegreeId')
            lecture_department_id = request.form.get('lectureDepartmentId')
            lecture_semester_id = request.form.get('lectureSemesterId')
            lecture_subject_id = request.form.get('lectureSubjectId')
            lecture_date = request.form.get('lectureDate')
            lecture_day = request.form.get('lectureDay')
            lecture_start_time = request.form.get('lectureStartTime')
            lecture_end_time = request.form.get('lectureEndTime')

            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            # storing all the data in database
            lecture_vo.lecture_id = lecture_id
            lecture_vo.lecture_degree_id = lecture_degree_id
            lecture_vo.lecture_department_id = lecture_department_id
            lecture_vo.lecture_semester_id = lecture_semester_id
            lecture_vo.lecture_subject_id = lecture_subject_id
            lecture_vo.lecture_semester_id = lecture_semester_id
            lecture_vo.lecture_faculty_id = faculty_id
            lecture_vo.lecture_date = lecture_date
            lecture_vo.lecture_day = lecture_day
            lecture_vo.lecture_start_time = lecture_start_time
            lecture_vo.lecture_end_time = lecture_end_time

            lecture_dao.update_lecture(lecture_vo)
            return redirect('/faculty/view_lecture')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_update_lecture route exception "
              "occured>>>>>>>>>>>>>>>", ex)

@app.route('/student/view_lecture')
def student_view_lecture():
    try:
        if admin_login_session() == "student":
            lecture_vo = LectureVO()
            lecture_dao = LectureDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(student_vo)

            # bringing all the data
            lecture_vo.lecture_semester_id = student_semester_id
            lecture_vo_list = lecture_dao.student_view_lecture(
                lecture_vo)

            return render_template('student/viewLecture.html',
                                   lecture_vo_list=lecture_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_about route exception occured>>>>>>>>>>", ex)

# @app.route('/faculty/ajax_department_lecture')
# def faculty_ajax_department_lecture():
#     try:
#         if admin_login_session() == "faculty":
#             department_vo = DepartmentVO()
#             department_dao = DepartmentDAO()
#             department_degree_id = request.args.get('lectureDegreeId')
#             department_vo.department_degree_id = department_degree_id
#
#             department_vo_list = department_dao.view_ajax_department(
#                 department_vo)
#             ajax_lecture_department = [i.as_dict() for i in
#                                        department_vo_list]
#             return jsonify(ajax_lecture_department)
#         else:
#             return admin_logout_session()
#     except Exception as ex:
#         print("faculty_ajax_department_lecture route exception "
#               "occured>>>>>>>>>>>>", ex)
#
#
# @app.route('/faculty/ajax_semester_lecture')
# def faculty_ajax_semester_lecture():
#     try:
#         if admin_login_session() == "faculty":
#             semester_vo = SemesterVO()
#             semester_dao = SemesterDAO()
#             semester_department_id = request.args.get('lectureDepartmentId')
#             semester_vo.semester_department_id = semester_department_id
#
#             semester_vo_list = semester_dao.view_ajax_semester(semester_vo)
#             ajax_lecture_semester = [i.as_dict() for i in semester_vo_list]
#             return jsonify(ajax_lecture_semester)
#         else:
#             return admin_logout_session()
#     except Exception as ex:
#         print("faculty_ajax_semester_lecture route exception "
#               "occured>>>>>>>>>>>>>>>", ex)
#

# @app.route('/faculty/ajax_faculty_lecture')
# def faculty_ajax_faculty_lecture():
#     try:
#         if admin_login_session() == "faculty":
#             faculty_vo = FacultyVO()
#             faculty_dao = FacultyDAO()
#             faculty_subject_id = request.args.get('lectureSubjectId')
#             faculty_vo.faculty_subject_id = faculty_subject_id
#
#             faculty_vo_list = faculty_dao.view_ajax_faculty(faculty_vo)
#             ajax_lecture_faculty = [i.as_dict() for i in faculty_vo_list]
#             return jsonify(ajax_lecture_faculty)
#         else:
#             return admin_logout_session()
#     except Exception as ex:
#         print("faculty_ajax_faculty_lecture route exception "
#               "occured>>>>>>>>>>>>>>", ex)
