# -*- coding: utf-8 -*-
__author__ = "Hiếu Đỗ"

from odoo import models, fields, api, exceptions

class Students(models.Model):
    _name = "students"
    _description = "Sinh viên"

    masv = fields.Char(string="Mã Sinh Viên", readonly="1")
    name = fields.Char(string="Tên Sinh Viên", required="1")
    bod = fields.Date(string="Ngày sinh")
    address = fields.Text(string="Địa chỉ")
    phone= fields.Char(string='Số điện thoại')
    mail = fields.Char(string="Email")
    gioitinh = fields.Selection(string="Giới tính", selection=[('female', 'Nam'),('male', 'Nữ')], default="female")

    state = fields.Selection(string='Trạng thái',
                             selection=[('mh','Mới nhập học'),('hd','Học đi'),('dhx','Đã Học Xong')],
                                compute='def_state', store=True)

    chuyen_nganh_id = fields.Many2one(comodel_name="chuyen_nganh", string="Chuyên ngành")
    class_class_ids = fields.Many2many(comodel_name="class_class", string="Lớp học", )
    point_ids = fields.One2many('points', 'student_id', string='Điểm')
    khoa_id = fields.Many2one(comodel_name="khoa.hoc", string="Khóa Học")
    points = fields.Float(string="Điểm")

    _sql_constraints = [
        ('phone_unique', 'unique(phone)', 'Số điện thoại trùng rồi. Hãy nhập số khác!')
    ]
    _sql_constraints = [
        ('email_unique', 'unique(mail)', 'Email trùng rồi. Hãy nhập email khác!')
    ]


    @api.multi
    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.name = self.name.title()

    @api.multi
    @api.depends('class_class_ids')
    def def_state(self):
        for states in self:
            if states.class_class_ids:
                states.state = 'hd'
            else:
                states.state = 'mh'

    @api.multi
    def check_hoc(self):
        self.state = 'dhx'

    @api.model
    def create(self, vals):
        vals['masv'] = self.env['ir.sequence'].next_by_code('SEQ_SINH_VIEN')
        return super(Students, self).create(vals)

    @api.onchange('khoa_id')
    def onchange_field_chuyen_nganh(self):
        if self.khoa_id:
            # filter chuyen_nganh_id by khoa_id
            chuyen_nganh_ids = self.khoa_id.chuyen_nganh_ids.ids
            return {'domain': {'chuyen_nganh_id': [('id', 'in', chuyen_nganh_ids)]}}
        else:
            # filter all chuyen_nganh_id -> remove domain
            return {'domain': {'chuyen_nganh_id': []}}


