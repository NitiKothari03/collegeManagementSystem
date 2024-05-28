from base import db
from base.com.vo.degree_vo import DegreeVO


class DegreeDAO:
    def insert_degree(self, degree_vo):
        db.session.add(degree_vo)
        db.session.commit()

    def view_degree(self):
        degree_vo_list = DegreeVO.query.all()
        return degree_vo_list

    def delete_degree(self, degree_vo):
        degree_vo_list = DegreeVO.query.get(degree_vo.degree_id)
        db.session.delete(degree_vo_list)
        db.session.commit()

    def edit_degree(self, degree_vo):
        degree_vo_list = DegreeVO.query.filter_by(
            degree_id=degree_vo.degree_id).all()
        return degree_vo_list

    def update_degree(self, degree_vo):
        db.session.merge(degree_vo)
        db.session.commit()
