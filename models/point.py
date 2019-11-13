# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError

class Points(models.Model):
    _name = 'points'
    _rec_name = 'display_name'
    _description = "Điểm tổng kết"

    @api.constrains('point')
    def check_point(self):
        for record in self:
            if record.point < 0 or record.point > 10:
                raise ValidationError(_('Số điểm chỉ được nằm trong khoảng từ 0 đến 10. Mời nhập lại'))

    student_id = fields.Many2one('students', string='Sinh Viên')
    class_class_id = fields.Many2one('class_class', string='Lớp học')
    subject_id = fields.Many2one('mon_hoc', string='Môn học', related='class_class_id.mon_hoc_id')
    display_name = fields.Char(string='Display Name', compute='_get_point_name',
                               store=True)
    point = fields.Float(string='Số điểm')

    @api.depends('student_id', 'class_class_id')
    def _get_point_name(self):
        for points in self:
            points.display_name = points.student_id.name + ' - ' + points.class_class_id.name

    # Cách lọc một trường Many2one dựa trên giá trị của một trường khác trong odoo
    @api.onchange('class_class_id')
    def onchange_field_students(self):
        if self.class_class_id:
            sinh_vien_ids = self.class_class_id.student_id.ids
            return {'domain': {'student_id': [('id', 'in', sinh_vien_ids)]}}
        else:
            return {'domain': {'student_id': []}}

    # @api.model
    # def _check_students(self, vals):
    #     if 'class_class_id' in vals:
    #         if 'student_id' in vals:
    #             students = self.env['students']
    #             check_point = students.search([('student_id', '=', vals['student_id'])])
    #             if check_point:
    #                 raise exceptions.ValidationError("Sinh viên này đã có điểm ở lớp này rồi. Mời nhập sinh viên khác!")
    #
    # @api.model
    # def create(self, vals):
    #     self._check_students(vals)
    #     return super(Points, self).create(vals)

