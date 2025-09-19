# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CX - Material Request',
    'version': '1.0.0',
    'summary': 'Material Request',
    'sequence': 10,
    'description': """
        Costum module from AMP to request material for Odoo\'s community edition.
    """,
    'author': 'AMP - AWH',
    'category': 'AMP Module',
    'depends': ['cx_stock_period'],
    'data': [
        # data
        'data/ir_sequence_data.xml',

        # security
        'security/groups.xml',
        'security/ir.model.access.csv',

        # views
        'views/material_request_views.xml',

        # wizard
        'wizard/wizard_create_picking_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
