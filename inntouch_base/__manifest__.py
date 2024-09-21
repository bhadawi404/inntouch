# -*- coding: utf-8 -*-
{
    'name': 'Inntouch Base',
    'category': 'Inntouch/base',
    'summary': 'Inntouch Base',
    'version': '1.0',
    'description': """Inntouch Base""",
    'author': "Inntouch",
    'depends': ["sale_stock", "account"],
    "data": [
        "views/inntouch_service_type_views.xml",
        "views/inntouch_property_views.xml",
        "views/inntouch_facilities_views.xml",
        "views/inntouch_amenities_views.xml",
        "views/menu_items.xml",
        "security/ir.model.access.csv",
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
