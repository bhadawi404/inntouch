from odoo import models, fields

class InntouchDepositPolicy(models.Model):
    _name = 'inntouch.deposit.policy'
    _description = 'Deposit Policy'

    name = fields.Char(string="Policy Name", required=True, help="Name of the deposit policy (e.g., Standard Deposit Policy)")
    property_id = fields.Many2one('inntouch.property', string='Property')
    room_type_id = fields.Many2one('inntouch.room.type', string="Room Type", required=True, help="Room type to which this deposit policy applies")
    deposit_percentage = fields.Float(string="Deposit Percentage (%)", required=True, help="Percentage of the total amount to be paid as a deposit")
    due_date_before_checkin = fields.Integer(string="Due Date Before Check-In (Days)", required=True, help="Number of days before check-in by which deposit must be paid")
    policy_description = fields.Text(string="Policy Description", help="Description of the deposit policy")
