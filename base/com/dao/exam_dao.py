from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.exam_vo import ExamVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO
from base.com.vo.faculty_vo import FacultyVO


class ExamDAO():
    def insert_exam(self,exam_vo):
        db.session.add(exam_vo)
        db.session.commit()

    def view_exam(self):
        exam_vo_list = db.session.query(DegreeVO, DepartmentVO, SemesterVO,
                                           SubjectVO,
                                           ExamVO).filter(
            DegreeVO.degree_id == ExamVO.exam_degree_id).filter(
            DepartmentVO.department_id ==
            ExamVO.exam_department_id).filter(SemesterVO.semester_id
                                                    == ExamVO.exam_semester_id
                                                    ).filter(
            SubjectVO.subject_id == ExamVO.exam_subject_id).all()
        return exam_vo_list

    def delete_exam(self,exam_vo):
        exam_vo_list = ExamVO.query.get(exam_vo.exam_id)
        db.session.delete(exam_vo_list)
        db.session.commit()

    def edit_exam(self,exam_vo):
        exam_vo_list = ExamVO.query.filter_by(exam_id = exam_vo.exam_id)
        return exam_vo_list

    def update_exam(self,exam_vo):
        db.session.merge(exam_vo)
        db.session.commit()

    def faculty_view_exam(self, exam_vo):
        exam_vo_list = db.session.query(ExamVO,
                                           SemesterVO,SubjectVO,FacultyVO).filter_by(
            exam_faculty_id=exam_vo.exam_faculty_id).filter(
            SemesterVO.semester_id == ExamVO.exam_semester_id,
            SubjectVO.subject_id == ExamVO.exam_subject_id,
            FacultyVO.faculty_id == ExamVO.exam_faculty_id).all()
        return exam_vo_list

    def student_view_exam(self, exam_vo):
        exam_vo_list = db.session.query(ExamVO,
                                           SemesterVO,SubjectVO,FacultyVO).filter_by(
            exam_semester_id=exam_vo.exam_semester_id).filter(
            SemesterVO.semester_id == ExamVO.exam_semester_id,
            SubjectVO.subject_id == ExamVO.exam_subject_id,
            FacultyVO.faculty_id == ExamVO.exam_faculty_id).all()
        return exam_vo_list