from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

class InntouchWaitlist(models.Model):
    _name = 'inntouch.waitlist'
    _description = 'Waitlist Management'

    name = fields.Char('aitlist Number',default='New')
    guest_id = fields.Many2one('res.partner', string="Guest", required=True, help="Guest waiting for the reservation")
    room_type_id = fields.Many2one('inntouch.room.type', string="Room Type", required=True, help="Type of room requested")
    requested_checkin_date = fields.Date(string="Requested Check-in Date", required=True)
    requested_checkout_date = fields.Date(string="Requested Check-out Date", required=True)
    priority_level = fields.Selection(AVAILABLE_PRIORITIES, string="Priority Level", default=AVAILABLE_PRIORITIES[0][0])
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('processed', 'Processed'),
        ('canceled', 'Canceled')
    ], string="Status", default="waiting", required=True)

    _sql_constraints = [
        ('unique_guest_room_type', 'unique(guest_id, room_type_id)', 'Guest is already in the waitlist for this room type.')
    ]
