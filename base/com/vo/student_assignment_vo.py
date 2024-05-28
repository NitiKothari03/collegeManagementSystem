from base import db
from base.com.vo.student_vo import StudentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.assignment_vo import AssignmentVO


class StudentAssignmentVO(db.Model):
    __tablename__ = 'student_assignment_table'
    st_assign_id = db.Column('st_assign_id', db.Integer,
                                  primary_key=True,
                              autoincrement=True)
    st_assign_student_id = db.Column('st_assign_student_id', db.Integer,
                                       db.ForeignKey(StudentVO.student_id,
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'),
                                       nullable=False)
    st_assign_faculty_id = db.Column('st_assign_faculty_id',
                                            db.Integer,
                                      db.ForeignKey(FacultyVO.faculty_id,
                                                    ondelete='CASCADE',
                                                    onupdate='CASCADE'),
                                      nullable=False)
    st_assignment_id = db.Column('st_assignment_id',
                                         db.Integer,
                                         db.ForeignKey(AssignmentVO.assignment_id,
                                                       ondelete='CASCADE',
                                                       onupdate='CASCADE'),
                                         nullable=False)
    st_assign_marks = db.Column('st_assign_marks',db.Integer)
    st_assign_image_name = db.Column('st_assign_image_name', db.String(
        255),
                                      nullable=False)
    st_assign_image_path = db.Column('st_assign_image_path', db.String(
        255),
                                      nullable=False)

    def as_dict(self):
        return {
            'st_assign_id': self.st_assign_id,
            'st_assign_marks': self.st_assign_marks,
            'st_assign_student_id': self.st_assign_student_id,
            'st_assign_faculty_id': self.st_assign_faculty_id,
            'st_assignment_id': self.st_assignment_id,
            'st_assign_image_name': self.st_assign_image_name,
            'st_assign_image_path': self.st_assign_image_path,
        }


db.create_all()
