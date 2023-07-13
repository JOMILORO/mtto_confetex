# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class MaintenanceEquipmentLoan(models.Model):
    _name = 'maintenance.equipment.loan'
    _description = "Préstamo del equipo de mantenimiento"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string="Folio", index=True, copy=False, readonly=True,
                       default='Nuevo préstamo máquinas y herramientas')
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('autorizado', 'Autorizado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', string="Estado", tracking=True, copy=False, readonly=True)
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
        required=False,
        readonly=True,
        tracking=True
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
    fecha_autorizacion = fields.Datetime(string="Fecha autorización", required=False, readonly=True)

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['name'] = self.env['ir.sequence'].next_by_code('secuencia.prestamo.equipo.mantenimiento')
        return super(MaintenanceEquipmentLoan, self).create(values)

    def unlink(self):
        logger.info('Entramos al método unlink')
        for record in self:
            if record.state != 'borrador':
                raise UserError('No se puede cancelar el resgistro porque no se encuentra en estado borrador')
            super(MaintenanceEquipmentLoan, record).unlink()

    def confirmar_prestamo(self):
        logger.info("Entramos al método confirmar_prestamo")
        if self.item_ids:
            for equipo_prestamo in self.item_ids:
                maquina_herramienta = self.env['maintenance.equipment'].browse(equipo_prestamo.name.id)
                if maquina_herramienta:
                    if self.tipo_movimiento == 'salida' and maquina_herramienta.state == 'en_prestamo':
                        raise UserError('No se puede prestar una máquina o herramienta si su estado esta: En préstamo.' +
                                        '\nFavor de verificar máquina o herramienta con código interno:' +
                                        maquina_herramienta.codigo_interno)
                    if self.tipo_movimiento == 'entrada' and maquina_herramienta.state == 'en_sitio':
                        raise UserError('No se puede ingresar una máquina o herramienta si su estado esta: En sitio.' +
                                        '\nFavor de verificar máquina o herramienta con código interno:' +
                                        maquina_herramienta.codigo_interno)
            self.state = 'confirmado'
        else:
            raise UserError('Aún no ha ingresado por lo menos una máquina o herramienta.')

    def autorizar_prestamo(self):
        logger.info("Entramos al método autorizar_prestamo")
        for equipo_prestamo in self.item_ids:
            maquina_herramienta = self.env['maintenance.equipment'].browse(equipo_prestamo.name.id)
            if maquina_herramienta:
                if self.tipo_movimiento == 'salida':
                    nota = maquina_herramienta.note + "\nMáquina o herramienta prestada con folio: " + self.name + \
                           " el " + str(self.fecha_efectiva)
                    maquina_herramienta.write({
                        'location': self.ubicacio_foranea or False,
                        'state': 'en_prestamo',
                        'note': nota
                    })
                if self.tipo_movimiento == 'entrada':
                    nota = maquina_herramienta.note + "\nMáquina o herramienta ingresada con folio: " + self.name + \
                           " el " + str(self.fecha_efectiva)
                    maquina_herramienta.write({
                        'location': self.ubicacion or False,
                        'state': 'en_sitio',
                        'category_id': self.planta_id.id,
                        'note': nota
                    })
        self.fecha_autorizacion = fields.datetime.now()
        self.autoriza_user_id = self.env.uid
        self.state = 'autorizado'

    def cancelar_prestamo(self):
        logger.info("Entramos al método cancelar_prestamo")
        for equipo_prestamo in self.item_ids:
            maquina_herramienta = self.env['maintenance.equipment'].browse(equipo_prestamo.name.id)
            if maquina_herramienta:
                estado_maquina = maquina_herramienta.state
                if self.tipo_movimiento == 'salida' and estado_maquina != 'en_sitio':
                    nota = maquina_herramienta.note + "\nSalida, préstamo máquina o herramienta con folio: " + \
                           self.name + " cancelado el " + str(self.fecha_efectiva)
                    maquina_herramienta.write({
                        'location': self.ubicacion or False,
                        'state': 'en_sitio',
                        'note': nota
                    })
                if self.tipo_movimiento == 'entrada' and estado_maquina != 'en_prestamo':
                    nota = maquina_herramienta.note + "\nEntrada, préstamo máquina o herramienta con folio: " + \
                           self.name + " cancelado el " + str(self.fecha_efectiva)
                    maquina_herramienta.write({
                        'location': self.ubicacio_foranea or False,
                        'state': 'en_prestamo',
                        'category_id': self.planta_id.id,
                        'note': nota
                    })
        self.state = 'cancelado'

    def cambiar_borrador(self):
        logger.info("Entramos al método cambiar_borrador")
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
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañia",
        required=False,
        related='name.company_id',
        store=True
    )
    estado_equipo = fields.Selection(selection=[
        ('en_sitio', 'En sitio'),
        ('en_prestamo', 'En préstamo'),
    ], string="Estado equipo", related='name.state', store=True)
