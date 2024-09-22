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
        "views/inntouch_waitlist_views.xml",
        "views/inntouch_calendar_availability_views.xml",
        "views/inntouch_preference_type_views.xml",
        "views/inntouch_guest_preferences_views.xml",
        "views/inntouch_room_views.xml",
        "views/inntouch_room_pricing_views.xml",
        "views/inntouch_deposit_policy_views.xml",
        "views/inntouch_cancellation_policy_views.xml",
        "views/inntouch_booking_source_views.xml",
        "views/inntouch_room_type_views.xml",
        "views/menu_items.xml",
        "security/ir.model.access.csv",
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
