from base import db
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.subject_vo import SubjectVO
from base.com.vo.semester_vo import SemesterVO


class AssignmentDAO:
    def insert_assignment(self, assignment_vo):
        db.session.add(assignment_vo)
        db.session.commit()

    # def view_assignment(self):
    #     assignment_vo_list = db.session.query(DegreeVO, DepartmentVO,
    #                                           SubjectVO, FacultyVO,
    #                                           AssignmentVO).filter(
    #         DegreeVO.degree_id == AssignmentVO.assignment_degree_id).filter(
    #         DepartmentVO.department_id ==
    #         AssignmentVO.assignment_department_id).filter(SubjectVO.subject_id
    #                                                       ==
    #                                                       AssignmentVO.assignment_subject_id).filter(
    #         FacultyVO.faculty_id == AssignmentVO.assignment_faculty_id).all()
    #     return assignment_vo_list

    def delete_assignment(self, assignment_vo):
        assignment_vo_list = AssignmentVO.query.get(
            assignment_vo.assignment_id)
        db.session.delete(assignment_vo_list)
        db.session.commit()
        return assignment_vo_list

    def edit_assignment(self, assignment_vo):
        assignment_vo_list = AssignmentVO.query.filter_by(
            assignment_id=assignment_vo.assignment_id)
        return assignment_vo_list

    # def edit_assignment(self, assignment_vo):
    #     assignment_vo_list = AssignmentVO.query.filter_by(
    #         assignment_id=assignment_vo.assignment_id)
    #     return assignment_vo_list

    def update_assignment(self, assignment_vo):
        db.session.merge(assignment_vo)
        db.session.commit()

    def faculty_view_assignment(self, assignment_vo):
        assignment_vo_list = db.session.query(AssignmentVO,
                                             FacultyVO,SubjectVO,
                                              SemesterVO).filter_by(
            assignment_faculty_id=assignment_vo.assignment_faculty_id).filter(
            SubjectVO.subject_id == AssignmentVO.assignment_subject_id,
            SemesterVO.semester_id == AssignmentVO.assignment_semester_id,
            FacultyVO.faculty_id == AssignmentVO.assignment_faculty_id).all()
        return assignment_vo_list

    def student_view_assignment(self, assignment_vo):
        assignment_vo_list = db.session.query(AssignmentVO,
                                             FacultyVO,SubjectVO).filter_by(
            assignment_semester_id=assignment_vo.assignment_semester_id
        ).filter(
            SubjectVO.subject_id == AssignmentVO.assignment_subject_id,
            FacultyVO.faculty_id == AssignmentVO.assignment_faculty_id).all()
        return assignment_vo_list

    def find_assignment(self,assignment_id):
        assignment_vo_list = AssignmentVO.query.filter_by(
            assignment_id=assignment_id).all()
        return assignment_vo_list

    def find_semester_subject(self, assignment_id):
        assignment_vo_list = db.session.query(AssignmentVO,SemesterVO,
                                           SubjectVO).filter_by(
            assignment_id=assignment_id).filter(
            SemesterVO.semester_id == AssignmentVO.assignment_semester_id).filter(
            SubjectVO.subject_id == AssignmentVO.assignment_subject_id).all()
        return assignment_vo_list

    def view_assignmentdata(self, assignment_id):
        faculty_vo_list = db.session.query(AssignmentVO,SemesterVO,
                                           SubjectVO,FacultyVO).filter_by(
            assignment_id=assignment_id).filter(
            SemesterVO.semester_id == AssignmentVO.assignment_semester_id).filter(
            SubjectVO.subject_id == AssignmentVO.assignment_subject_id).filter(
            FacultyVO.faculty_id == AssignmentVO.assignment_faculty_id).all()
        return faculty_vo_list

    def find_subject_id(self,assignment_id):
        assignment_subject_id = AssignmentVO.query.filter_by(
            assignment_id=assignment_id).all()[
            -1].assignment_subject_id
        return assignment_subject_id

    def find_faculty(self,assignment_id):
        assignment_faculty_id = AssignmentVO.query.filter_by(
            assignment_id=assignment_id).all()[
            -1].assignment_faculty_id
        return assignment_faculty_id

    def find_assignment_title(self,assignment_id):
        assignment_title = AssignmentVO.query.filter_by(
            assignment_id=assignment_id).all()[
            -1].assignment_title
        return assignment_title

    def find_assignment_marks(self,assignment_id):
        assignment_marks = AssignmentVO.query.filter_by(
            assignment_id=assignment_id).all()[
            -1].assignment_marks
        return assignment_marks