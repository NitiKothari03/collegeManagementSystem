from flask import request, render_template, redirect,flash

from base import app
from base.com.controller.login_controller import admin_logout_session, \
    admin_login_session
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.vo.department_vo import DepartmentVO


@app.route('/admin/load_department')
def admin_load_department():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            return render_template('admin/addDepartment.html',
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_Department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_department', methods=['POST'])
def admin_insert_department():
    try:
        if admin_login_session() == "admin":
            department_degree_id = request.form.get('departmentDegreeId')
            department_name = request.form.get('departmentName')
            department_code = request.form.get('departmentCode')
            department_description = request.form.get('departmentDescription')

            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_vo.department_degree_id = department_degree_id
            department_vo.department_name = department_name
            department_vo.department_code = department_code
            department_vo.department_description = department_description

            department_dao.insert_department(department_vo)
            return redirect('/admin/view_department')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_department')
def admin_view_department():
    try:
        if admin_login_session() == "admin":
            department_dao = DepartmentDAO()
            department_vo_list = department_dao.view_department()
            return render_template('admin/viewDepartment.html',
                                   department_vo_list=department_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_department')
def admin_delete_department():
    try:
        if admin_login_session() == "admin":
            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_id = request.args.get('departmentId')
            department_vo.department_id = department_id
            department_dao.delete_department(department_vo)
            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_department')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_Department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_department')
def admin_edit_department():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_id = request.args.get('departmentId')
            department_vo.department_id = department_id
            department_vo_list = department_dao.edit_department(department_vo)
            print("|")
            print(department_vo_list)
            return render_template('admin/editDepartment.html',
                                   department_vo_list=department_vo_list,
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_Department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_department', methods=['POST'])
def admin_update_department():
    try:
        if admin_login_session() == "admin":
            department_id = request.form.get('departmentId')
            department_degree_id = request.form.get('departmentDegreeId')
            department_name = request.form.get('departmentName')
            department_code = request.form.get('departmentCode')
            department_description = request.form.get('departmentDescription')

            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_vo.department_id = department_id
            department_vo.department_degree_id = department_degree_id
            department_vo.department_name = department_name
            department_vo.department_code = department_code
            department_vo.department_description = department_description

            department_dao.update_department(department_vo)
            return redirect('/admin/view_department')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_Department route exception occured>>>>>>>>>>", ex)
