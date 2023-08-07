# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceEquipmentCharacteristics(models.Model):
    _name = 'maintenance.equipment.characteristics'
    _description = 'Características del equipo de mantenimiento'
    _order = 'tipo_caracteristica_id,name'

    name = fields.Char(string="Nombre", index=True, copy=True, required=True, default='Nueva característica')
    active = fields.Boolean(string="Activo", default=True, required=True)
    description = fields.Text(string="Descripción", required=False)
    tipo_caracteristica_id = fields.Many2one(
        comodel_name='maintenance.equipment.characteristics.type',
        string='Tipo',
        required=True,
        readonly=False
    )

    _sql_constraints = [
        ('maintenance_equipment_characteristics_unique_1',
         'UNIQUE(name)',
         "El nombre de la categoría debe de ser único, vuelva a intentarlo con otro nombre por favor"),
    ]

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(MaintenanceEquipmentCharacteristics, self).copy(default)


class MaintenanceEquipmentCharacteristicsType (models.Model):
    _name = 'maintenance.equipment.characteristics.type'
    _description = 'Tipo de características del equipo de mantenimiento'

    name = fields.Char(string="Tipo de característica", required=True, index=True)
