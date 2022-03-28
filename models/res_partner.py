from odoo import api, fields, models


class Anggota(models.Model):
    _inherit = 'res.partner'

    is_anggota = fields.Boolean(string ='Anggota Perpustakaan', deafult=False)
    is_penulis = fields.Boolean(string ='Penulis Buku Perpustakaan', deafult=False)
    is_publisher = fields.Boolean(string ='Publisher Buku Perpustakaan', deafult=False)
