from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.semester_vo import SemesterVO


class SubjectVO(db.Model):
    __tablename__ = 'subject_table'
    subject_id = db.Column('subject_id', db.Integer, primary_key=True,
                           autoincrement=True)
    subject_degree_id = db.Column('subject_degree_id', db.Integer,
                                  db.ForeignKey(DegreeVO.degree_id,
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                                  nullable=False)
    subject_department_id = db.Column('subject_deartment_id', db.Integer,
                                      db.ForeignKey(
                                          DepartmentVO.department_id,
                                          ondelete='CASCADE',
                                          onupdate='CASCADE'), nullable=False)
    subject_semester_id = db.Column('subject_semester_id', db.Integer,
                                    db.ForeignKey(SemesterVO.semester_id,
                                                  ondelete='CASCADE',
                                                  onupdate='CASCADE'),
                                    nullable=False)
    subject_name = db.Column('subject_name', db.String(255), nullable=False)
    subject_code = db.Column('subject_code', db.String(15), nullable=False)
    subject_textbook = db.Column('subject_textbook', db.String(255),
                                 nullable=False)

    def as_dict(self):
        return {
            'subject_id': self.subject_id,
            'subject_degree_id': self.subject_degree_id,
            'subject_department_id': self.subject_department_id,
            'subject_semester_id': self.subject_semester_id,
            'subject_name': self.subject_name,
            'subject_code': self.subject_code,
            'subject_textbook': self.subject_textbook
        }


db.create_all()
