# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api

logger = logging.getLogger(__name__)


class MaintenanceEquipmentLoanWizard(models.TransientModel):
    _name = 'maintenance.equipment.loan.wizard'
    _description = 'Wizard préstamo del equipo de mantenimiento'

    def get_tipo_movimiento(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        state = maquina_herramienta_brw.state
        tipo_movimiento = ""
        if state == 'en_sitio':
            tipo_movimiento = 'salida'
        if state == 'en_prestamo':
            tipo_movimiento = 'entrada'
        return tipo_movimiento

    def get_company_id(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        company_id = maquina_herramienta_brw.company_id.id
        if company_id:
            return company_id
        else:
            return lambda self: self.env.company

    def get_category_id(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        category_id = maquina_herramienta_brw.category_id.id
        return category_id

    def get_ubicacion(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        state = maquina_herramienta_brw.state
        location = ""
        if state == 'en_sitio':
            location = maquina_herramienta_brw.location
        return location

    def get_department_id(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        department_id = maquina_herramienta_brw.department_id.id
        return department_id

    name = fields.Char(string="Nombre", readonly=True, required=True, copy=False,
                       default='Nuevo préstamo máquinas y herramientas')
    tipo_movimiento = fields.Selection(selection=[
        ('salida', 'Salida'),
        ('entrada', 'Entrada'),
    ], default=get_tipo_movimiento, string="Tipo de movimiento", readonly=True, required=True, copy=False)
    company_id = fields.Many2one(
        'res.company',
        default=get_company_id,
        string='Compañía',
        readonly=True,
        required=True,
        copy=False
    )
    # Agregar poner categoria_id el 23-07-2023
    category_id = fields.Many2one(
        comodel_name='maintenance.equipment.category',
        default=get_category_id,
        string="Categoría",
        readonly=True,
        required=True,
        copy=False
    )
    ubicacion = fields.Char(default=get_ubicacion, string="Ubicación", copy=False)
    proveedor_id = fields.Many2one(
        comodel_name='res.partner',
        string="Proveedor",
        check_company=True,
        copy=False
    )
    proveedor_ref = fields.Char(string="Referencia proveedor", copy=False)
    responsable_foraneo = fields.Char(string="Responsable foráneo", copy=False)
    ubicacio_foranea = fields.Char(string='Ubicación foránea', copy=False)
    nota = fields.Text(string="Anotaciones", required=False)
    department_id = fields.Many2one(
        comodel_name='hr.department',
        default=get_department_id,
        string="Departamento",
        readonly=True,
        copy=False
    )

    def crear_prestamo(self):
        logger.info("********** Entramos al método crear_prestamo *********")
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        maquina_herramienta_brw = self.env['maintenance.equipment'].browse(active_id)
        if maquina_herramienta_brw:
            item_myh = []
            item_myh.append([0, 0, {
                'name': maquina_herramienta_brw.id
            }])
            vals = {
                'tipo_movimiento': self.tipo_movimiento,
                'company_id': self.company_id.id,
                'category_id': self.category_id.id,
                'department_id': self.department_id or False,
                'ubicacion': self.ubicacion,
                'proveedor_id': self.proveedor_id.id,
                'proveedor_ref': self.proveedor_ref,
                'responsable_foraneo': self.responsable_foraneo,
                'ubicacio_foranea': self.ubicacio_foranea,
                'nota': self.nota,
                'item_ids': item_myh
            }
            self.env['maintenance.equipment.loan'].create(vals)
            maquina_herramienta_brw.write({
                'state': 'en_proceso'
            })