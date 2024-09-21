from odoo import _, api, fields, models

class InntouchSpecialRequest(models.Model):
    _name = 'inntouch.special.request'
    _description = 'Special Requests'

    reservation_id = fields.Many2one('inntouch.reservation', string='Reservation', required=True)
    description = fields.Text('Description', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], string='Status', default='pending')

