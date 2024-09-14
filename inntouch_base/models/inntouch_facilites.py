from odoo import _, api, fields, models

class InntouchFacilities(models.Model):
    _name = 'inntouch.facilities'
    _description = 'Facilities'

    name = fields.Char('Facilites Name')
    opening_hours = fields.Float(string='Opening Hours')
    closing_hours = fields.Float(string='Closing Hours')
    description = fields.Text('Description')
    state = fields.Selection([
        ('operational', 'Operational'),
        ('under_maintenance', 'Under Maintenance'),
        ('closed', 'Closed')
    ], string='Status', default='operational')
    maintenance_date = fields.Date('Maintenance Date')
    property_id = fields.Many2one('inntouch.property', string='Property', required=True)

    def action_closed(self):
        self.write({'state': 'closed'})

    