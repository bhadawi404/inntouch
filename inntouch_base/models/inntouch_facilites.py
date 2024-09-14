from odoo import _, api, fields, models

class InntouchAFacilities(models.Model):
    _name = 'inntouch.facilities'
    _description = 'Facilities'

    name = fields.Char('Facilites Name')
    description = fields.Text('Description')
    state = fields.Selection([
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('deactive', 'Deactive'),
    ], string='State', default='active')
    maintenance_date = fields.Date('Maintenance Date')


    def action_active(self):
        self.write({'state': 'active'})
    
    def action_deactive(self):
        self.write({'state': 'Deactive'})