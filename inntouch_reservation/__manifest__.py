# -*- coding: utf-8 -*-
{
    'name': 'Inntouch Reservation',
    'category': 'Inntouch/reservation',
    'summary': 'Inntouch Reservation',
    'version': '1.0',
    'description': """Inntouch Reservation""",
    'author': "Inntouch",
    'depends': ['inntouch_base'],
    "data": [
        "views/inntouch_booking_source_views.xml",
        "views/inntouch_room_type_views.xml",
        "views/menu_items.xml",
        "security/ir.model.access.csv",
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
