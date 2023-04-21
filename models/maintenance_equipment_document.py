# -*- coding:utf-8 -*-

from odoo import fields, models, api

class MaintenanceEquipmentDocument(models.Model):
    _name = 'maintenance.equipment.document'
    _description = 'Documento para equipo de mantenimiento'

    name = fields.Many2one(
        comodel_name="maintenance.equipment.document.type",
        string="Tipo de documento",
        required=False,
        copy=True
    )
    fecha = fields.Date(string="Fecha", required=False)
    id_currency = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        required=False,
        default=lambda self: self.env.company.currency_id.id
    )
    id_equipo_mantenimiento = fields.Many2one(
        comodel_name="maintenance.equipment",
        ondelete='cascade',
        string="Equipo de mantenimiento",
        required=False,
        index=True,
        copy=True
    )
    nota = fields.Text(string="Anotaciones", required=False)
    folio = fields.Char(string="Folio", required=False, index=True)
    id_partner = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        required=False,
        copy=True
    )
    url_google_drive = fields.Char(string="URL Documento", required=False)
    valor = fields.Float(string="Valor", required=False)
    active = fields.Boolean(string='Activo', default=True)