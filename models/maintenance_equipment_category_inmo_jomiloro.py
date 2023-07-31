from odoo import fields, models, api

class MaintenanceEquipmentCategoryInmoJomiloro(models.Model):
    _inherit = 'maintenance.equipment.category'

    chanel_gd_id = fields.Many2one(
        comodel_name='maintenance.channel.gd',
        string='Canal Google Drive',
        required=False
    )
    url_carpeta_google_drive = fields.Char(string="URL Carpeta GD", store=True,
                                           related="chanel_gd_id.url_carpeta_google_drive", readonly=True)