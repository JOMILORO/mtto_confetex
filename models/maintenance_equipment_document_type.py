# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceEquipmentDocumentType(models.Model):
    _name = 'maintenance.equipment.document.type'
    _description = "Tipos de documento para equipo de mantenimiento"
    _order = 'name'

    name = fields.Char(string="Nombre", required=True, copy=True, index=True)
    comentario = fields.Text(string="Comentarios", required=False)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('nombre_tipo_docuemnto_unique',
         'UNIQUE(name)',
         "El nombre del tipo de documento debe de ser único, busque o vuelva " +
         "a intentarlo si no lo encuentra por favor verifique que el nombre del tipo de documento se encuentre activo."),
    ]

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(MaintenanceEquipmentDocumentType, self).copy(default)