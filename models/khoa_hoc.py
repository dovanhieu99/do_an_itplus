__author__ = "Hiếu Đỗ"

from odoo import models, fields, api

class Khoa_hoc(models.Model):
    _name = "khoa.hoc"
    _description = "Khóa học"

    READONLY_STATES = {
        'dkt': [('readonly', True)],
    }

    ma_khoa = fields.Char(string="Mã Khóa", states=READONLY_STATES)
    name = fields.Char(string="Tên Khóa", states=READONLY_STATES)
    tgbd = fields.Date(string="Bắt đầu", states=READONLY_STATES)
    tgkt = fields.Date(string="Kết Thúc", states=READONLY_STATES)

    chuyen_nganh_ids = fields.Many2many(comodel_name="chuyen_nganh", string="Các Chuyên Ngành", states=READONLY_STATES)
    count_cn = fields.Integer(string="Số lượng chuyên ngành", default=0,
                              compute="def_countcn", store=True)
    sinh_vien_ids = fields.One2many(comodel_name="students", inverse_name="khoa_id",
                                    string="DS Sinh Viên", states=READONLY_STATES)

    count = fields.Integer(string="Sinh viên", default=0,
                           compute="def_count", store=True)
    state = fields.Selection(string="Trạng thái",
                             selection=[('dh', 'Đang học'), ('dkt', 'Đã kết thúc')], default='dh', store=True)

    @api.multi
    @api.depends('sinh_vien_ids')
    def def_count(self):
        for dem in self:
            dem.count = len(dem.sinh_vien_ids)

    @api.multi
    @api.depends('chuyen_nganh_ids')
    def def_countcn(self):
        for dem in self:
            dem.count_cn = len(dem.chuyen_nganh_ids)

    @api.multi
    def check_khoa_hoc(self):
        self.state = 'dkt'