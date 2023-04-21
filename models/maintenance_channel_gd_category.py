# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceChannelGDCategory(models.Model):
    _name = 'maintenance.channel.gd.category'
    _description = "Categoría de canal de Google Drive mantenimiento"
    _order = 'name'

    name = fields.Char(string="Nombre", required=True, index=True)

    _sql_constraints = [
        ('nombre_categoria_google_drive_unique',
         'UNIQUE(name)',
         "El nombre de la categoría debe de ser único, vuelva a intentarlo con otro nombre por favor"),
    ]