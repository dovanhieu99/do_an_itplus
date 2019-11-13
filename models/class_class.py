# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api

class Class(models.Model):
    _name = 'class_class'
    _description = "Lớp học"

    READONLY_STATES = {
        'dhx': [('readonly', True)],
    }
    ma_lop = fields.Char(string="Mã Lớp", states=READONLY_STATES)
    name = fields.Char(string='Tên lớp', states=READONLY_STATES,)
    gv = fields.Char(string="Giáo Viên", states=READONLY_STATES,)
    student_id = fields.Many2many('students', string='DS sinh viên', states=READONLY_STATES,)
    mon_hoc_id = fields.Many2one('mon_hoc', string='Môn dạy', states=READONLY_STATES,)

    new_point_ids = fields.One2many(comodel_name="points", inverse_name="class_class_id", string="Điểm")

    count = fields.Integer(string="Số Lượng SV", default=0,
                           compute="def_count_class", store=True)
    date = fields.Datetime(string="Ngày tạo", default= lambda self: fields.Datetime.now())

    state = fields.Selection(string="Trạng thái",
                                     selection=[("mt","Mới tạo"),('dh', 'Đang học'),('dhx','Đã học xong')],
                                     compute='def_lop_hoc', store=True)
    count_point = fields.Integer(string="Điểm Tổng Kết", default=0,
                                compute="def_count_point", store=True)

    @api.model
    def create(self, vals):
        vals["ma_lop"] = vals["ma_lop"]
        vals["gv"] = vals["gv"].title()
        vals["name"] = vals["name"] + '-' + vals["ma_lop"]
        return super(Class, self).create(vals)

    @api.multi
    @api.depends('student_id')
    def def_count_class(self):
        for dems in self:
            dems.count = len(dems.student_id)

    @api.multi
    @api.depends("new_point_ids")
    def def_count_point(self):
        for tinh in self:
            tinh.count_point = len(tinh.new_point_ids)

    @api.multi
    @api.depends('new_point_ids','student_id')
    def def_lop_hoc(self):
        for point in self:
            if point.student_id:
                point.state = 'dh'
            else:
                point.state = 'mt'
            if point.new_point_ids:
                point.state = 'dhx'