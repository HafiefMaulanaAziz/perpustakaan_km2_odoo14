from odoo import api, fields, models


class Anggota(models.Model):
    _inherit = 'res.partner'

    is_anggota = fields.Boolean(string ='Anggota Perpustakaan', deafult=False)
