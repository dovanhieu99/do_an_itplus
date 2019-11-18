# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api

class Point_point(models.TransientModel):
    _name = "point_point"

    class_class_ids = fields.Many2many('class_class', string="Sinh Viên")
    diem = fields.Float(string="Điểm Tổng Kết")