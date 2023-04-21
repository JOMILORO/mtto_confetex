# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceChannelGD(models.Model):
    _name = 'maintenance.channel.gd'
    _description = "Canal de Google Drive mantenimiento"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string="Nombre", required=True, index=True, copy=True, tracking=True)
    url_carpeta_google_drive = fields.Char(string="URL Carpeta GD", required=False, tracking=True)
    id_categoria = fields.Many2one(comodel_name="maintenance.channel.gd.category", string="Categoría", required=False, copy=True)
    descripcion = fields.Text(string="Descripción de categoría", required=False)
    directorio_fisico = fields.Char(string="Directorio físico", required=False, copy=True, tracking=True)
    nombre_corto = fields.Char(string="Nombre corto", required=False, copy=True)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('nombre_canal_google_drive_unique',
         'UNIQUE(name)',
         "El nombre del canal para Google Drive debe de ser único, busque o vuelva " +
         "a intentarlo si no lo encuentra por favor verifique que el canal de Google Drive se encuentre activo."),
    ]

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(MaintenanceChannelGD, self).copy(default)