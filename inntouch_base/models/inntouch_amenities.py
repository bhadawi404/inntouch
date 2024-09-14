from odoo import _, api, fields, models

class InntouchAmenities(models.Model):
    _name = 'inntouch.amenities'
    _description = 'Amenities'

    name = fields.Char('Amenities Name')
    is_available = fields.Boolean('Is Available ?', default=True)
    last_maintenance_date = fields.Date('Last Maintenance')
    description = fields.Text('Description')
    property_id = fields.Many2one('inntouch.property', string='Property', required=True)


    