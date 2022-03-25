from odoo import api, fields, models
import datetime

class Pengembalian(models.Model):
    _name = 'perpus.pengembalian'
    _description = 'Model Pengembalian'

    name = fields.Char(string='Name')
    peminjaman_id = fields.Many2one('perpus.peminjaman', string='ID Peminjaman')
    tgl_pengembalian = fields.Date('Tanggal Pengembalian', default=fields.Date.today())
    tgl_kembali = fields.Date(compute='_compute_tgl_kembali', string='Tanggal Kembali')
    
    @api.depends('peminjaman_id')
    def _compute_tgl_kembali(self):
        for record in self:
            record.tgl_kembali = record.peminjaman_id.tgl_kembali

    
    denda = fields.Integer(compute='_compute_denda', string='Denda Keterlambatan')
    peminjam_id = fields.Many2one(comodel_name='res.partner', compute='_compute_peminjam_id', string='ID Peminjam')
    # detailpeminjaman_ids = fields.Char(compute='_compute_detailpeminjaman_ids', string='detailpeminjaman_ids')
    
    # @api.depends('peminjaman_id')
    # def _compute_detailpeminjaman_ids(self):
    #     for record in self:
    #         record.detailpeminjaman_ids = self.env['perpus.detailpeminjaman'].search([('peminjaman_id', '=', record.peminjaman_id.id)])
        
    
    @api.depends('peminjaman_id')
    def _compute_peminjam_id(self):
        for record in self:
            record.peminjam_id = record.peminjaman_id.anggota_id
    
    @api.depends('tgl_pengembalian')
    def _compute_denda(self):
        for record in self:
            tgl1 = record.tgl_kembali
            tgl2 = fields.Datetime.to_datetime(record.tgl_pengembalian).date()
            if record.tgl_kembali:
                diff_days = int((tgl2-tgl1).days)
                record.denda = 2000*diff_days if diff_days > 0 else 0
            else :
                record.denda = 0

    @api.model
    def create(self, vals):
        record = super(Pengembalian, self).create(vals)
        if record.tgl_pengembalian:
            self.env['perpus.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).write({'is_kembali':True})
            return record

    def unlink(self):
        for un in self:
            self.env['perpus.peminjaman'].search([('id', '=', un.peminjaman_id.id)]).write({'is_kembali':False})
        super(Pengembalian, self).unlink()
