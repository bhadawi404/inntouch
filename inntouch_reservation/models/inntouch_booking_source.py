from odoo import _, api, fields, models

class InntouchBookingSource(models.Model):
    _name = 'inntouch.booking.source'
    _description = 'Booking Source'

    name = fields.Char('Name')
    description = fields.Text('Description')