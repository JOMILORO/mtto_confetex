# -*- coding:utf-8 -*-
import logging
from odoo import fields, models, api

logger = logging.getLogger(__name__)

class MaintenanceEquipmentReview(models.Model):
    _name = 'maintenance.equipment.review'
    _description = "Revisión física de equipos de mantenimiento"
    _order = 'fecha_revision desc'

    name = fields.Char(string="Código", readonly=True, required=False, index=True)
    equipo_mantenimiento_id = fields.Many2one(
        comodel_name='maintenance.equipment',
        string='Equipo de mantenimiento',
        ondelete='cascade',
        index=True,
        required=False
    )
    fecha_revision = fields.Datetime(string="Fecha", required=False, readonly=True)
    active = fields.Boolean(string='Activo', default=True)
    usuario_reviso_id = fields.Many2one(
        comodel_name='res.users',
        string='Revisado por',
        required=True,
        readonly=True
    )
    comentario = fields.Text(string="Comentario", required=False)
    codigo_interno = fields.Char(string="Código maquinaria", readonly=True, store=True, related="equipo_mantenimiento_id.codigo_interno", index=True)

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['name'] = self.env['ir.sequence'].next_by_code('secuencia.maintenance.equipment.review1')
        return super(MaintenanceEquipmentReview, self).create(values)