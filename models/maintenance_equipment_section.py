# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceEquipmentSection(models.Model):
    _name = 'maintenance.equipment.section'
    _description ="Sección del equipo de mantenimiento"
    _order = 'name'

    name = fields.Char(string="Nombre", required=True, index=True)

    _sql_constraints = [
        ('nombre_seccion_unique',
         'UNIQUE(name)',
         "El nombre de la sección debe de ser único, vuelva a intentarlo con otro nombre por favor"),
    ]