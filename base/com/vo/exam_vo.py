from base import db
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


class ExamVO(db.Model):
    __tablename__ = "exam_table"
    exam_id = db.Column('exam_id', db.Integer, primary_key=True,
                        nullable=False)
    exam_faculty_id = db.Column('exam_faculty_id', db.Integer,
                                 db.ForeignKey(FacultyVO.faculty_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)
    exam_semester_id = db.Column('exam_semester_id', db.Integer,
                                 db.ForeignKey(SemesterVO.semester_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)
    exam_subject_id = db.Column('exam_subject_id', db.Integer, db.ForeignKey(
        SubjectVO.subject_id, ondelete='CASCADE', onupdate='CASCADE'),
                                nullable=False)
    exam_name = db.Column('exam_name', db.String(255), nullable=False)
    exam_date = db.Column('exam_date', db.Date, nullable=False)
    exam_start_time = db.Column('exam_start_time', db.Time,
                                nullable=False)
    exam_end_time = db.Column('exam_end_time', db.Time, nullable=False)

    def as_dict(self):
        return {
            'exam_id': self.exam_id,
            'exam_semester_id': self.exam_semester_id,
            'exam_subject_id': self.exam_subject_id,
            'exam_name': self.exam_name,
            'exam_date': self.exam_date,
            'exam_start_time': self.exam_start_time,
            'exam_end_time': self.exam_end_time
        }


db.create_all()
