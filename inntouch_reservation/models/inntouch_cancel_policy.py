from odoo import models, fields

class InntouchCancelledPolicy(models.Model):
    _name = 'inntouch.cancellation.policy'
    _description = 'Cancellation Policy'

    name = fields.Char(string="Policy Name", required=True)
    property_id = fields.Many2one('inntouch.property', string='Property')
    description = fields.Text(string="Description", help="Detailed description of the cancellation policy.")
    cancellation_fee = fields.Float(string="Cancellation Fee", help="The fee charged for canceling a reservation.")
    refund_policy = fields.Selection([
        ('no_refund', 'No Refund'),
        ('partial_refund', 'Partial Refund'),
        ('full_refund', 'Full Refund')
    ], string="Refund Policy", required=True, help="Policy regarding refunds for canceled reservations.")
    validity = fields.Date(string="Validity", help="The date until this policy is valid.")
