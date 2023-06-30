# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api
logger = logging.getLogger(__name__)


class MaintenanceEquipmentLoan(models.Model):
    _name = 'maintenance.equipment.loan'
    _description ="Préstamo del equipo de mantenimiento"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string="Folio", index=True, copy=False, readonly=True, default='Nuevo préstamo máquinas y herramientas')
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('autorizado', 'Autorizado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', string="Estado", tracking=True, copy=False)
    tipo_movimiento = fields.Selection(selection=[
        ('salida', 'Salida'),
        ('entrada', 'Entrada'),
    ], required=True, default='salida', string="Tipo de movimiento", copy=False)
    planta_id = fields.Many2one(
        comodel_name='maintenance.equipment.category',
        string="Planta",
        tracking=True,
        copy=True
    )
    ubicacion = fields.Char(string="Ubicación", tracking=True, copy=True)
    ubicacio_foranea = fields.Char(string='Ubicación foránea')
    fecha_efectiva = fields.Date(string="Fecha", required=True, default=fields.Date.context_today)
    autoriza_user_id = fields.Many2one(
        comodel_name='res.users',
        string="Autoriza",
        required=True,
        default=lambda self: self.env.user,
        readonly=True
    )
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string="Responsable",
        required=True,
        default=lambda self: self.env.user,
        readonly=True
    )
    responsable_foraneo = fields.Char(string="Responsable foráneo", required=False, tracking=True, copy=False)
    proveedor_id = fields.Many2one(
        comodel_name='res.partner',
        string="Proveedor",
        check_company=True,
        tracking=True
    )
    proveedor_ref = fields.Char(string="Referencia proveedor")
    nota = fields.Text(string="Anotaciones", required=False)
    item_ids = fields.One2many(
        comodel_name="maintenance.equipment.loan.item",
        inverse_name="equipment_loan_id",
        string="Item",
        required=False
    )
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company, tracking=True)

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['name'] = self.env['ir.sequence'].next_by_code('secuencia.prestamo.equipo.mantenimiento')
        return super(MaintenanceEquipmentLoan, self).create(values)

    def confirmar_prestamo(self):
        logger.info("Entramos al método confirmar_prestamo")
        self.state = 'confirmado'

    def autorizar_prestamo(self):
        logger.info("Entramos al método autorizar_prestamo")
        self.state = 'autorizado'

    def cancelar_prestamo(self):
        logger.info("Entramos al método cancelar_prestamo")
        self.state = 'borrador'

class MaintenanceEquipmentLoanItem(models.Model):
    _name = 'maintenance.equipment.loan.item'
    _description = "Movimiento de préstamo del equipo de mantenimiento"

    name = fields.Many2one(
        comodel_name="maintenance.equipment",
        string="Máquina o herramienta",
        required=True,
        index=True,
        copy=False
    )
    equipment_loan_id = fields.Many2one(
        comodel_name="maintenance.equipment.loan",
        string="Máquina en préstamo",
        required=False,
        ondelete='cascade',
    )
    codigo_interno = fields.Char(string="Código interno", related='name.codigo_interno', index=True, store=True)
    numero_economico = fields.Char(string="Número económico", related='name.numero_economico', store=True)
    model = fields.Char(string="Modelo", related='name.model', store=True)
    serial_no = fields.Char(string="No. de Serie", related='name.serial_no', store=True)
    note = fields.Text(string="Nota", related='name.note', store=True)