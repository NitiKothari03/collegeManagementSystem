import os

# os.mkdir('../../static/studentResources/assignments')
# # os.rmdir('niti')
# if not str(os.path.exists(student_department)):
#     print("//")
#     # os.chdir(student_department)
#     print("///")
#
#     if str(os.path.exists(student_semester)):
#         # os.chdir(student_semester)
#
#         if str(os.path.exists(assignment_subject)):
#             # os.chdir(assignment_subject)
#             print("////")
#             if str(os.path.exists(student_enrollment + "_st")):
#                 # os.chdir(student_enrollment)
#                 print("/////")
#
#                 assignment_image_name = secure_filename(
#                     assignment_image.filename)
#                 print("/////1")
#                 assignment_image_path = os.path.join(
#                     app.config['STUDENT_ASSIGNMENT_FOLDER'])
#                 print("/////2")
#                 assignment_image.save(
#                     os.path.join(assignment_image_path,
#                                  assignment_image_name))
#                 print('?')
#
#                 student_assignment_vo.st_assign_image_name = \
#                     assignment_image_name
#                 print('??')
#                 student_assignment_vo.st_assign_image_path = \
#                     assignment_image_path.replace(
#                         "base", "..")
#                 print('???')
#                 student_assignment_vo.st_assign_student_id = student_id
#                 student_assignment_vo.st_assignment_id = assignment_id
#                 student_assignment_vo.st_assign_faculty_id = \
#                     assignment_faculty_id
#
#                 student_assignment_dao.insert_student_assignment(
#                     student_assignment_vo)
#                 print('????')
#
#                 success_message = 'Assignment submitted ' \
#                                   'Successfully!'
#                 print('?????')
#                 flash(success_message)
#                 print('??????')
#
#             else:
#                 os.mkdir(student_enrollment)
#         else:
#             os.mkdir(assignment_subject)
#     else:
#         os.mkdir(student_semester)
# else:
#     os.mkdir(student_department)

@app.route('/student/insert_assignment',methods=['GET', 'POST'])
def student_insert_assignment():
    try:
        if admin_login_session() == "student":
            assignment_id = request.args.get('assignmentId')
            print('\n>>>>>>>>>>>>>>>', assignment_id)

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            semester_dao = SemesterDAO()
            department_dao = DepartmentDAO()
            subject_dao = SubjectDAO()
            student_assignment_vo = StudentAssignmentVO()
            assignment_dao = AssignmentDAO()
            student_assignment_dao = StudentAssignmentDAO()
            faculty_dao = FacultyDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get(
                'login_username')
            student_login_id = login_dao.find_login_id(login_vo)
            print("student_login_id>>>>>>>>", student_login_id)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)
            student_enrollment = student_dao.find_student_enrollment(student_id)
            print("student_enrollment>>>>>>>>", student_enrollment)

            # bringing department id
            student_vo.student_id = student_id
            student_department_id = student_dao.find_department_id(
                student_vo)
            student_department = department_dao.find_department(student_department_id)
            print("student_department>>>>>>>>", student_department)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(
                student_vo)
            student_semester = semester_dao.find_semester(student_semester_id)
            print("student_semester>>>>>>>>", student_semester)

            # 'base/static/studentResources/assignments/'
            assignment_subject_id = assignment_dao.find_subject_id(
                assignment_id)
            assignment_subject = subject_dao.find_subject(assignment_subject_id)
            print("assignment_subject>>>>>>>>", assignment_subject)

            if request.method == 'POST':
                assignment_image = request.files.get('assignmentFile')
                print("assignment_image?????????",assignment_image)

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
                            student_semester,assignment_subject)) == False:
                    os.mkdir(
                        'base/static/studentResources/assignments/{}/{}/{}'.format(
                            student_department,
                            student_semester, assignment_subject))

                if os.path.exists(
                        'base/static/studentResources/assignments/{}/{}/{}/{}'.format(
                            student_department,
                            student_semester,assignment_subject,student_enrollment)) == \
                        False:
                    add_assignment()
                else:
                    os.mkdir(
                        'base/static/studentResources/assignments/{}/{}/{}/{}'.format(
                            student_department,
                            student_semester,assignment_subject,student_enrollment))
                    add_assignment()

            return redirect('/student/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "student_insert_assignment route exception occured>>>>>>>>>>",
            ex)

def add_assignment():
    print("/////")

    assignment_image_name = secure_filename(
        assignment_image.filename)
    print("/////1")
    assignment_image_path = os.path.join(
        app.config['STUDENT_ASSIGNMENT_FOLDER'])
    print("/////2")
    assignment_image.save(
        os.path.join(assignment_image_path,
                     assignment_image_name))
    print('?')

    student_assignment_vo.st_assign_image_name = \
        assignment_image_name
    print('??')
    student_assignment_vo.st_assign_image_path = \
        assignment_image_path.replace(
        "base", "..")
    print('???')
    student_assignment_vo.st_assign_student_id = student_id
    student_assignment_vo.st_assignment_id = assignment_id
    student_assignment_vo.st_assign_faculty_id =\
        assignment_faculty_id

    student_assignment_dao.insert_student_assignment(student_assignment_vo)
    print('????')

    success_message = 'Assignment submitted ' \
                      'Successfully!'
    print('?????')
    flash(success_message)
    print('??????')