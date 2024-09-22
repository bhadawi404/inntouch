# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Zen Webhook Sending Data Sale Order',
    'version': '1.0',
    'category': 'Zensoftware/Sales',
    'author': "Zen Software Solutions",
    'summary': 'Zen Webhook Sending Data Sale Order - v1.0',
    'website': 'https://www.zensoftwaresolutions.com',
    'depends': [
        'base',
        'sale',
    ],
    "data": [
        "views/res_config_settings.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}