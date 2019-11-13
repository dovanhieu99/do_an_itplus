# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api

class Chuyen_nganh(models.Model):
    _name = "chuyen_nganh"
    _description = "Chuyên Ngành"

    ma_nganh = fields.Char(string="Mã chuyên ngành")
    name = fields.Char(string="Chuyên ngành")
    sinh_vien_ids = fields.One2many(comodel_name="students",
                                    inverse_name="chuyen_nganh_id",
                                    string="DS Sinh viên")
    mota = fields.Text(string="Mô tả")

    @api.multi
    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.name = self.name.title()