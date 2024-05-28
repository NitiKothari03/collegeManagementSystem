from base import db
from base.com.vo.degree_vo import DegreeVO


class DepartmentVO(db.Model):
    __tablename__ = 'department_table'
    department_id = db.Column('department_id', db.Integer, primary_key=True,
                              autoincrement=True)
    department_degree_id = db.Column('department_degree_id', db.Integer,
                                     db.ForeignKey(DegreeVO.degree_id,
                                                   ondelete='CASCADE',
                                                   onupdate='CASCADE'),
                                     nullable=False)
    department_name = db.Column('department_name', db.String(255),
                                nullable=False)
    department_code = db.Column('department_code', db.String(3),
                                nullable=False)
    department_description = db.Column('department_description', db.Text,
                                       nullable=False)

    def as_dict(self):
        return {
            'department_id': self.department_id,
            'department_degree_id': self.department_degree_id,
            'department_name': self.department_name,
            'department_code': self.department_code,
            'department_description': self.department_description
        }


db.create_all()
