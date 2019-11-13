# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api

class Mon_hoc(models.Model):
    _name = "mon_hoc"
    _description = "Môn học"

    ma_mon = fields.Char(string="Mã Môn Học")
    name = fields.Char(string="Tên Môn")
    mota = fields.Text(string="Mô tả")
    points_ids = fields.One2many(comodel_name="points",
                                 inverse_name="subject_id", string="Điểm")
    _sql_constraints = [
        ('ma_mon_unique', 'unique(ma_mon)', 'Ma Mon Hoc Da Trung. Hay Chon Ma Khac!')
    ]

    @api.multi
    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.name = self.name.title()