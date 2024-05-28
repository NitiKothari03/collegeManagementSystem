from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.lecture_vo import LectureVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


class LectureDAO():
    def insert_lecture(self, lecture_vo):
        db.session.add(lecture_vo)
        db.session.commit()

    def view_lecture(self):
        lecture_vo_list = db.session.query(DegreeVO, DepartmentVO, SemesterVO,
                                           SubjectVO, FacultyVO,
                                           LectureVO).filter(
            DegreeVO.degree_id == LectureVO.lecture_degree_id).filter(
            DepartmentVO.department_id ==
            LectureVO.lecture_department_id).filter(SemesterVO.semester_id
                                                    == LectureVO.lecture_semester_id
                                                    ).filter(
            SubjectVO.subject_id == LectureVO.lecture_subject_id).filter(
            FacultyVO.faculty_id == LectureVO.lecture_faculty_id).all()
        return lecture_vo_list

    def delete_lecture(self,lecture_vo):
        lecture_vo_list = LectureVO.query.get(
            lecture_vo.lecture_id)
        db.session.delete(lecture_vo_list)
        db.session.commit()

    def edit_lecture(self,lecture_vo):
        lecture_vo_list = LectureVO.query.filter_by(
            lecture_id =lecture_vo.lecture_id)
        return lecture_vo_list

    def update_lecture(self, lecture_vo):
        db.session.merge(lecture_vo)
        db.session.commit()

    def faculty_view_lecture(self, lecture_vo):
        lecture_vo_list = db.session.query(LectureVO,
                                           SemesterVO,SubjectVO,FacultyVO).filter_by(
            lecture_faculty_id=lecture_vo.lecture_faculty_id).filter(
            SemesterVO.semester_id == LectureVO.lecture_semester_id,
            SubjectVO.subject_id == LectureVO.lecture_subject_id,
            FacultyVO.faculty_id == LectureVO.lecture_faculty_id).all()
        return lecture_vo_list

    def student_view_lecture(self, lecture_vo):
        lecture_vo_list = db.session.query(LectureVO,
                                           SemesterVO,SubjectVO,FacultyVO).filter_by(
            lecture_semester_id=lecture_vo.lecture_semester_id).filter(
            SemesterVO.semester_id == LectureVO.lecture_semester_id,
            SubjectVO.subject_id == LectureVO.lecture_subject_id,
            FacultyVO.faculty_id == LectureVO.lecture_faculty_id).all()
        return lecture_vo_list