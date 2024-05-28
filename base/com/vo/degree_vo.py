from base import db


class DegreeVO(db.Model):
    __tablename__ = 'degree_table'
    degree_id = db.Column('degree_id', db.Integer, primary_key=True,
                          autoincrement=True)
    degree_name = db.Column('degree_name', db.String(255), nullable=False)
    degree_description = db.Column('degree_description', db.Text,
                                   nullable=False)

    def as_dict(self):
        return {
            'degree_id': self.degree_id,
            'degree_name': self.degree_name,
            'degree_description': self.degree_description
        }


db.create_all()
