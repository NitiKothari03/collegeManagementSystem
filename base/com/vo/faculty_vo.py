from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.subject_vo import SubjectVO


class FacultyVO(db.Model):
    __tablename__ = 'faculty_table'
    faculty_id = db.Column('faculty_id', db.Integer, primary_key=True,
                           autoincrement=True)
    faculty_degree_id = db.Column('faculty_degree_id', db.Integer,
                                  db.ForeignKey(DegreeVO.degree_id,
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                                  nullable=False)
    faculty_department_id = db.Column('faculty_department_id', db.Integer,
                                      db.ForeignKey(
                                          DepartmentVO.department_id,
                                          ondelete='CASCADE',
                                          onupdate='CASCADE'), nullable=False)
    faculty_subject_id = db.Column('faculty_subject_id', db.Integer,
                                   db.ForeignKey(SubjectVO.subject_id,
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                                   nullable=False)
    faculty_login_id = db.Column('faculty_login_id', db.Integer,
                                 db.ForeignKey(LoginVO.login_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)
    faculty_firstname = db.Column('faculty_firstname', db.String(255),
                                  nullable=False)
    faculty_lastname = db.Column('faculty_lastname', db.String(255),
                                 nullable=False)
    faculty_gender = db.Column('faculty_gender', db.String(10),
                               nullable=False)
    faculty_qualification = db.Column('faculty_qualification', db.String(
        255), nullable=False)
    faculty_teaching_experience = db.Column('faculty_teaching_experience',
                                            db.String(
                                                255), nullable=False)
    faculty_contact = db.Column('faculty_contact', db.String(10),
                                nullable=False)
    faculty_hod = db.Column('faculty_hod', db.Boolean, nullable=False)
    faculty_image_name = db.Column('faculty_image_name', db.String(255),
                                   nullable=False)
    faculty_image_path = db.Column('faculty_image_path', db.String(255),
                                   nullable=False)

    def as_dict(self):
        return {
            'faculty_id': self.faculty_id,
            'faculty_degree_id': self.faculty_degree_id,
            'faculty_department_id': self.faculty_department_id,
            'faculty_login_id': self.faculty_login_id,
            'faculty_subject_id': self.faculty_subject_id,
            'faculty_firstname': self.faculty_firstname,
            'faculty_lastname': self.faculty_lastname,
            'faculty_gender': self.faculty_gender,
            'faculty_qualification': self.faculty_qualification,
            'faculty_teaching_experience': self.faculty_teaching_experience,
            'faculty_contact': self.faculty_contact,
            'faculty_hod': self.faculty_hod,
            'faculty_image_name': self.faculty_image_name,
            'faculty_image_path': self.faculty_image_path
        }


db.create_all()
