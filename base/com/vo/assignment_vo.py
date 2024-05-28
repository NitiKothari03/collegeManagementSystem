from base import db
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.subject_vo import SubjectVO


class AssignmentVO(db.Model):
    __tablename__ = 'assignment_table'
    assignment_id = db.Column('assignment_id', db.Integer, primary_key=True,
                              autoincrement=True)
    assignment_semester_id = db.Column('assignment_semester_id', db.Integer,
                                       db.ForeignKey(SemesterVO.semester_id,
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'),
                                       nullable=False)
    assignment_subject_id = db.Column('assignment_subject_id', db.Integer,
                                      db.ForeignKey(SubjectVO.subject_id,
                                                    ondelete='CASCADE',
                                                    onupdate='CASCADE'),
                                      nullable=False)
    assignment_faculty_id = db.Column('assignment_faculty_id', db.Integer,
                                      nullable=False)
    assignment_title = db.Column('assignment_title', db.String(255),
                                 nullable=False)
    assignment_startdate = db.Column('assignment_startdate', db.String(10),
                                     nullable=False)
    assignment_enddate = db.Column('assignment_enddate', db.String(10),
                                   nullable=False)
    assignment_marks = db.Column('assignment_marks', db.Integer,
                                 nullable=False)
    assignment_description = db.Column('assignment_description', db.Text,
                                       nullable=False)
    assignment_image_name = db.Column('assignment_image_name', db.String(255),
                                      nullable=False)
    assignment_image_path = db.Column('assignment_image_path', db.String(255),
                                      nullable=False)

    def as_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'assignment_subject_id': self.assignment_subject_id,
            'assignment_faculty_id': self.assignment_faculty_id,
            'assignment_title': self.assignment_title,
            'assignment_startdate': self.assignment_startdate,
            'assignment_enddate': self.assignment_enddate,
            'assignment_marks': self.assignment_marks,
            'assignment_description': self.assignment_description,
            'assignment_image_name': self.assignment_image_name,
            'assignment_image_path': self.assignment_image_path
        }


db.create_all()
