from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


class SubjectDAO:
    def insert_subject(self, subject_vo):
        db.session.add(subject_vo)
        db.session.commit()

    def view_subject(self):
        subject_vo_list = db.session.query(DegreeVO, DepartmentVO, SemesterVO,
                                           SubjectVO).filter(
            DegreeVO.degree_id == SubjectVO.subject_degree_id).filter(
            DepartmentVO.department_id ==
            SubjectVO.subject_department_id).filter(SemesterVO.semester_id
                                                    ==
                                                    SubjectVO.subject_semester_id).all()
        return subject_vo_list

    def delete_subject(self, subject_vo):
        subject_vo_list = SubjectVO.query.get(subject_vo.subject_id)
        db.session.delete(subject_vo_list)
        db.session.commit()

    def edit_subject(self, subject_vo):
        subject_vo_list = SubjectVO.query.filter_by(subject_id=
                                                    subject_vo.subject_id).all()
        return subject_vo_list

    def update_subject(self, subject_vo):
        db.session.merge(subject_vo)
        db.session.commit()

    def view_ajax_subject(self, subject_vo):
        subject_vo_list = SubjectVO.query.filter_by(
            subject_department_id=subject_vo.subject_department_id).all()
        return subject_vo_list

    def view_ajax_subject_faculty(self, subject_vo):
        subject_vo_list = SubjectVO.query.filter_by(
            subject_semester_id=subject_vo.subject_semester_id).all()
        return subject_vo_list

    def find_subject(self,assignment_subject_id):
        subject_name = SubjectVO.query.filter_by(
            subject_id=assignment_subject_id).all()[-1].subject_name
        return subject_name
