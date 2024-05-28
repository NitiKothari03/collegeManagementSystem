from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.subject_vo import SubjectVO


class FacultyDAO:
    def insert_faculty(self, faculty_vo):
        db.session.add(faculty_vo)
        db.session.commit()

    def view_faculty(self):
        faculty_vo_list = db.session.query(DegreeVO, DepartmentVO,
                                           SubjectVO, LoginVO,
                                           FacultyVO).filter(
            DegreeVO.degree_id == FacultyVO.faculty_degree_id).filter(
            DepartmentVO.department_id ==
            FacultyVO.faculty_department_id).filter(SubjectVO.subject_id
                                                    ==
                                                    FacultyVO.faculty_subject_id).filter(
            LoginVO.login_id == FacultyVO.faculty_login_id).all()
        return faculty_vo_list

    def delete_faculty(self, faculty_vo):
        faculty_vo_list = FacultyVO.query.get(faculty_vo.faculty_id)
        db.session.delete(faculty_vo_list)
        db.session.commit()
        return faculty_vo_list

    def edit_faculty(self, faculty_vo):
        faculty_vo_list = db.session.query(FacultyVO, LoginVO).filter_by(
            faculty_id=faculty_vo.faculty_id).filter(
            LoginVO.login_id == FacultyVO.faculty_login_id).first()
        return faculty_vo_list

    def update_faculty(self, faculty_vo):
        db.session.merge(faculty_vo)
        db.session.commit()

    def view_ajax_faculty(self, faculty_vo):
        faculty_vo_list = FacultyVO.query.filter_by(
            faculty_subject_id=faculty_vo.faculty_subject_id).all()
        return faculty_vo_list

    def find_faculty_id(self, faculty_vo):
        faculty_vo_list = FacultyVO.query.filter_by(
            faculty_login_id=faculty_vo.faculty_login_id).all()[-1].faculty_id
        return faculty_vo_list

    def find_department_id(self, faculty_vo):
        faculty_vo_list = FacultyVO.query.filter_by(
            faculty_id=faculty_vo.faculty_id).all()[-1].faculty_department_id
        return faculty_vo_list

    def view_facultydata(self, faculty_id):
        faculty_vo_list = db.session.query(FacultyVO, DegreeVO,
                                           DepartmentVO,SubjectVO,
                                          LoginVO).filter_by(
            faculty_id=faculty_id).filter(
            DegreeVO.degree_id == FacultyVO.faculty_degree_id).filter(
            DepartmentVO.department_id == FacultyVO.faculty_department_id).filter(
            SubjectVO.subject_id == FacultyVO.faculty_subject_id).filter(
            LoginVO.login_id == FacultyVO.faculty_login_id).all()
        return faculty_vo_list

    def find_faculty(self,student_department_id):
        faculty_vo_list = FacultyVO.query.filter_by(
            faculty_department_id=student_department_id).all()[
            -1].faculty_id
        return faculty_vo_list

    def find_facultydata(self,student_department_id):
        faculty_vo_list = FacultyVO.query.filter_by(
            faculty_department_id=student_department_id).all()
        return faculty_vo_list

    def find_faculty_login_id(self,assignment_faculty_id):
        faculty_login_id = FacultyVO.query.filter_by(
            faculty_id=assignment_faculty_id).all()[-1].faculty_login_id
        return faculty_login_id