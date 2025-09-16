# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CX - Material',
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
        # security
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
