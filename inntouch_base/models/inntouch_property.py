from odoo import models, fields

class InntouchProperty(models.Model):
    _name = 'inntouch.property'
    _description = 'Property'

    name = fields.Char(string='Property Name', required=True)
    location = fields.Char(string='Location', required=True)
    number_of_rooms = fields.Integer(string='Number of Rooms')
    contact_number = fields.Char(string='Contact Number')