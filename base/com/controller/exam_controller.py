from flask import render_template, request, redirect, jsonify,flash

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.exam_dao import ExamDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.dao.student_dao import StudentDAO
from base.com.vo.student_vo import StudentVO
from base.com.vo.exam_vo import ExamVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


@app.route('/faculty/load_exam')
def faculty_load_exam():
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

            # bringing subjects based on department id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_department_id = faculty_department_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            return render_template('faculty/addExamSchedule.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_load_exam route exception occured>>>>>>>>>>>>>>>", ex)

@app.route('/faculty/ajax_subject_exam')
def faculty_ajax_subject_exam():
    try:
        if admin_login_session() == "faculty":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_semester_id = request.args.get('examSemesterId')
            subject_vo.subject_semester_id = subject_semester_id

            subject_vo_list = subject_dao.view_ajax_subject_faculty(subject_vo)
            ajax_exam_subject = [i.as_dict() for i in subject_vo_list]
            return jsonify(ajax_exam_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_ajax_subject_exam route exception "
              "occured>>>>>>>>>>>>>>>>", ex)


@app.route('/faculty/insert_exam', methods=['POST'])
def faculty_insert_exam():
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
            exam_semester_id = request.form.get('examSemesterId')
            exam_subject_id = request.form.get('examSubjectId')
            exam_name = request.form.get('examName')
            exam_date = request.form.get('examDate')
            exam_start_time = request.form.get('examStartTime')
            exam_end_time = request.form.get('examEndTime')

            exam_vo = ExamVO()
            exam_dao = ExamDAO()

            # storing all the data in database
            exam_vo.exam_faculty_id = faculty_id
            exam_vo.exam_semester_id = exam_semester_id
            exam_vo.exam_subject_id = exam_subject_id
            exam_vo.exam_name = exam_name
            exam_vo.exam_date = exam_date
            exam_vo.exam_start_time = exam_start_time
            exam_vo.exam_end_time = exam_end_time

            exam_dao.insert_exam(exam_vo)
            return redirect('/faculty/view_exam')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_insert_exam route exception occured>>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/view_exam')
def faculty_view_exam():
    try:
        if admin_login_session() == "faculty":
            exam_vo = ExamVO()
            exam_dao = ExamDAO()

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
            exam_vo.exam_faculty_id = faculty_id
            exam_vo_list = exam_dao.faculty_view_exam(exam_vo)
            return render_template('faculty/viewExamSchedule.html',
                                   exam_vo_list=exam_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_view_exam route exception occured>>>>>>>>>>>>>>>>>", ex)


@app.route('/faculty/delete_exam')
def faculty_delete_exam():
    try:
        if admin_login_session() == "faculty":
            exam_vo = ExamVO()
            exam_dao = ExamDAO()

            # deleting all the data
            exam_id = request.args.get('examId')
            exam_vo.exam_id = exam_id
            exam_dao.delete_exam(exam_vo)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/faculty/view_exam')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_delete_exam route exception occured>>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/edit_exam')
def faculty_edit_exam():
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

            exam_vo = ExamVO()
            exam_dao = ExamDAO()

            # bringing all the data to edit
            exam_id = request.args.get('examId')
            exam_vo.exam_id = exam_id
            exam_vo_list = exam_dao.edit_exam(exam_vo)
            return render_template('faculty/editExamSchedule.html',
                                   semester_vo_list=semester_vo_list,
                                   faculty_vo_list=faculty_vo_list,
                                   exam_vo_list=exam_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_exam route exception occured>>>>>>>>>>>>>>>>>>",
              ex)


@app.route('/faculty/update_exam', methods=['POST'])
def faculty_update_exam():
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
            exam_id = request.form.get('examId')
            exam_semester_id = request.form.get('examSemesterId')
            exam_subject_id = request.form.get('examSubjectId')
            exam_name = request.form.get('examName')
            exam_date = request.form.get('examDate')
            exam_start_time = request.form.get('examStartTime')
            exam_end_time = request.form.get('examEndTime')

            exam_vo = ExamVO()
            exam_dao = ExamDAO()

            # storing data in database
            exam_vo.exam_id = exam_id
            exam_vo.exam_faculty_id = faculty_id
            exam_vo.exam_semester_id = exam_semester_id
            exam_vo.exam_subject_id = exam_subject_id
            exam_vo.exam_name = exam_name
            exam_vo.exam_date = exam_date
            exam_vo.exam_start_time = exam_start_time
            exam_vo.exam_end_time = exam_end_time

            exam_dao.update_exam(exam_vo)
            return redirect('/faculty/view_exam')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_update_exam route exception "
              "occured>>>>>>>>>>>>>>>>>>", ex)

@app.route('/student/view_exam')
def student_view_exam():
    try:
        if admin_login_session() == "student":
            exam_vo = ExamVO()
            exam_dao = ExamDAO()

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
            exam_vo.exam_semester_id = student_semester_id
            exam_vo_list = exam_dao.student_view_exam(
                exam_vo)

            print("exam_vo_list>>>>>>>>>>>", exam_vo_list)
            return render_template('student/viewExam.html',exam_vo_list=exam_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_view_exam route exception occured>>>>>>>>>>",
              ex)


                # @app.route('/faculty/ajax_department_exam')
# def faculty_ajax_department_exam():
#     try:
#         if admin_login_session() == "faculty":
#             department_vo = DepartmentVO()
#             department_dao = DepartmentDAO()
#             department_degree_id = request.args.get('examDegreeId')
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
#         print("faculty_ajax_department_exam route exception "
#               "occured>>>>>>>>>>>>>>", ex)
#
#
# @app.route('/faculty/ajax_semester_exam')
# def faculty_ajax_semester_exam():
#     try:
#         if admin_login_session() == "faculty":
#             semester_vo = SemesterVO()
#             semester_dao = SemesterDAO()
#             semester_department_id = request.args.get('examDepartmentId')
#             semester_vo.semester_department_id = semester_department_id
#
#             semester_vo_list = semester_dao.view_ajax_semester(semester_vo)
#             ajax_exam_semester = [i.as_dict() for i in semester_vo_list]
#             return jsonify(ajax_exam_semester)
#         else:
#             return admin_logout_session()
#     except Exception as ex:
#         print("faculty_ajax_semester_exam route exception "
#               "occured>>>>>>>>>>>>>>>", ex)