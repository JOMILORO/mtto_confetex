# -*- coding:utf8 -*-
{
    'name': 'Mantenimiento Confetex',
    'category': 'Manufacturing/Maintenance',
    'version': '14.0.1',
    'author': 'José Miguel López Roano',
    'summary': 'Módulo para ordenes de mantenimiento y control de máquinas y herramientas en grupo Confetex',
    'description': '''Modulo para un control de peticiones de mantenimiento y control de máquinas y herramienta con 
                      impresión de código QR en Odoo14''',
    'website': 'https://www.confetex.com',
    'depends': [
        'base',
        'purchase',
        'hr',
        'maintenance',
        'base_automation',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/acciones_servidor.xml',
        'data/conf_maintenance_mtto_confetex.xml',
        'data/secuencia.xml',
        'wizard/maintenance_equipment_loan_wizard_vw.xml',
        'report/maintenance_reports.xml',
        'report/maintenance_templates.xml',
        'views/maintenance_equipment_menu_vw.xml',
        'views/maintenance_channel_gd_vw.xml',
        'views/maintenance_equipment_document_vw.xml',
        'views/maintenance_equipment_document_type_vw.xml',
        'views/maintenance_equipment_invw.xml',
        'views/maintenance_equipment_review_vw.xml',
        'views/maintenance_equipment_loan_vw.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}