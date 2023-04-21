# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api
logger = logging.getLogger(__name__)


class MaintenanceEquipmentInmo(models.Model):
    _inherit = 'maintenance.equipment'

    # Campos calculados
    def revisiones_fisicas_count(self):
        revisiones_fisicas_obj = self.env['maintenance.equipment.review']
        self.revisiones_numero = revisiones_fisicas_obj.search_count(
            [('equipo_mantenimiento_id', 'in', [a.id for a in self])])

    # Función para acción de servidor Equipo mantenimiento no inventariado
    def set_no_inventariado(self):
        for equipo in self:
            equipo.is_inventariado = False

    codigo_interno = fields.Char(string="Código interno", readonly=True, required=False, index=True, copy=False)
    documentos_ids = fields.One2many(
        comodel_name="maintenance.equipment.document",
        inverse_name="id_equipo_mantenimiento",
        string="Documentos",
        required=False
    )
    id_seccion = fields.Many2one(
        comodel_name="maintenance.equipment.section",
        string="Sección",
        required=False,
        copy=True
    )
    numero_economico = fields.Char(string="Número económico", required=False, index=True, copy=False)
    url_carpeta_google_drive = fields.Char(string="URL carpeta documentos", required=False)
    url_documento_qr = fields.Char(string="URL Documento QR", required=False)
    fecha_compra = fields.Date(string="Fecha de compra", required=False)

    # Agregar campos para revisión física de equipos de mantenimiento
    fecha_revision_equipo = fields.Datetime(string="Fecha de revisión", required=False, readonly=True)
    usuario_reviso_id = fields.Many2one(
        comodel_name='res.users',
        string='Revisado por',
        required=False,
        readonly=True
    )
    comentario_revision = fields.Text(string="Comentario", required=False)
    revisiones_numero = fields.Integer(string='Revisiones', compute='revisiones_fisicas_count', required=False)
    is_inventariado = fields.Boolean(string="Inventariado", default=True, copy=True)

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['codigo_interno'] = self.env['ir.sequence'].next_by_code('secuencia.maintenance.equipment1')
        if values["is_inventariado"]:
            values["fecha_revision_equipo"] = fields.datetime.now()
            values["usuario_reviso_id"] = self.env.uid
            values["comentario_revision"] = 'Revisión física contable realizada en la creación del equipo de mantenimiento.'
        return super(MaintenanceEquipmentInmo, self).create(values)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(MaintenanceEquipmentInmo, self).copy(default)

    def inventariar_equipo_mantenimiento(self):
        logger.info('********** Entro a la función inventariar_equipo_mantenimiento')
        for equipo_mantenimiento in self:
            if not equipo_mantenimiento.is_inventariado:
                if equipo_mantenimiento.fecha_revision_equipo and equipo_mantenimiento.usuario_reviso_id:
                    vals = {
                        'equipo_mantenimiento_id': equipo_mantenimiento.id,
                        'fecha_revision': equipo_mantenimiento.fecha_revision_equipo,
                        'usuario_reviso_id': equipo_mantenimiento.usuario_reviso_id.id,
                        'comentario': equipo_mantenimiento.comentario_revision or False
                    }
                    self.env['maintenance.equipment.review'].create(vals)
                equipo_mantenimiento.is_inventariado = True
                equipo_mantenimiento.fecha_revision_equipo = fields.datetime.now()
                equipo_mantenimiento.usuario_reviso_id = self.env.uid
                comentario_revision = equipo_mantenimiento.comentario_revision
                equipo_mantenimiento.comentario_revision = comentario_revision + "\nRevisión física contable realizada desde formulario o listado de Máquinas y herramientas."