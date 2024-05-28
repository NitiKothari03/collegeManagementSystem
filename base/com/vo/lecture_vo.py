from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


class LectureVO(db.Model):
    __tablename__ = "lecture_table"
    lecture_id = db.Column('lecture_id', db.Integer, primary_key=True,
                           autoincrement=True)
    lecture_semester_id = db.Column('lecture_semester_id', db.Integer,
                                    db.ForeignKey(
                                        SemesterVO.semester_id,
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'), nullable=False)
    lecture_subject_id = db.Column('lecture_subject_id', db.Integer,
                                   db.ForeignKey(SubjectVO.subject_id,
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                                   nullable=False)
    lecture_faculty_id = db.Column('lecture_faculty_id', db.Integer,
                                   db.ForeignKey(FacultyVO.faculty_id,
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                                   nullable=False)
    lecture_date = db.Column('lecture_date', db.Date, nullable=False)
    lecture_start_time = db.Column('lecture_start_time', db.Time,
                                   nullable=False)
    lecture_end_time = db.Column('lecture_end_time', db.Time, nullable=False)
    lecture_day = db.Column('lecture_day', db.String(10), nullable=False)

    def as_dict(self):
        return {
            'lecture_id': self.lecture_id,
            'lecture_semester_id': self.lecture_semester_id,
            'lecture_subject_id': self.lecture_subject_id,
            'lecture_faculty_id': self.lecture_faculty_id,
            'lecture_date': self.lecture_date,
            'lecture_start_time': self.lecture_start_time,
            'lecture_end_time': self.lecture_end_time,
            'lecture_day': self.lecture_day
        }


db.create_all()
