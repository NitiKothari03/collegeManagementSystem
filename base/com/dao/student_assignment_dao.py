from base import db
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_assignment_vo import StudentAssignmentVO
from base.com.vo.student_vo import StudentVO
from base.com.vo.subject_vo import SubjectVO


class StudentAssignmentDAO:
    def insert_student_assignment(self, student_assignment_vo):
        db.session.add(student_assignment_vo)
        db.session.commit()

    def faculty_view_assignment_grades(self, st_assignment_vo):
        assignment_vo_list = db.session.query(StudentAssignmentVO,
                                              AssignmentVO,
                                              FacultyVO, StudentVO,
                                              SemesterVO, SubjectVO
                                              ).filter_by(
            st_assign_faculty_id=st_assignment_vo.st_assign_faculty_id).filter(
            AssignmentVO.assignment_id == StudentAssignmentVO.st_assignment_id,
            StudentVO.student_id == StudentAssignmentVO.st_assign_student_id,
            FacultyVO.faculty_id == StudentAssignmentVO.st_assign_faculty_id,
            SemesterVO.semester_id == AssignmentVO.assignment_semester_id,
            SubjectVO.subject_id == AssignmentVO.assignment_semester_id
        ).all()
        return assignment_vo_list

    def student_view_assignment_grades(self, st_assignment_vo):
        assignment_vo_list = db.session.query(StudentAssignmentVO,
                                              AssignmentVO,
                                              FacultyVO, StudentVO
                                              ).filter_by(
            st_assign_student_id=st_assignment_vo.st_assign_student_id).filter(
            AssignmentVO.assignment_id == StudentAssignmentVO.st_assignment_id,
            StudentVO.student_id == StudentAssignmentVO.st_assign_student_id,
            FacultyVO.faculty_id == StudentAssignmentVO.st_assign_faculty_id
        ).all()
        return assignment_vo_list

    def delete_assignment_grades(self, st_assignment_vo):
        assignment_vo_list = StudentAssignmentVO.query.get(
            st_assignment_vo.st_assign_id)
        db.session.delete(assignment_vo_list)
        db.session.commit()
        return assignment_vo_list

    def edit_assignment_grades(self, st_assignment_vo):
        assignment_grade_list = StudentAssignmentVO.query.filter_by(
            st_assign_id=st_assignment_vo.st_assign_id)
        return assignment_grade_list

    def update_assignment_marks(self, st_assignment_vo):
        db.session.merge(st_assignment_vo)
        db.session.commit()

    def find_assignment(self,st_assign_id):
        st_assignment_id = StudentAssignmentVO.query.filter_by(
            st_assign_id=st_assign_id).all()[-1].st_assignment_id
        return st_assignment_id

    def find_assign_marks(self,st_assign_id):
        st_assign_marks = StudentAssignmentVO.query.filter_by(
            st_assign_id=st_assign_id).all()[-1].st_assign_marks
        return st_assign_marks