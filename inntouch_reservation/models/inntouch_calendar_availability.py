from odoo import models, fields, api, _

class InntouchCalendarAvailability(models.Model):
    _name = 'inntouch.calendar.availability'
    _description = 'Calendar Availability'

    room_id = fields.Many2one('inntouch.room', string="Room", required=True, help="Room associated with this availability record")
    date = fields.Date(string="Date", required=True, help="The date for which the availability is being recorded")
    is_available = fields.Boolean(string="Is Available", default=True, help="Indicates if the room is available on this date")
    notes = fields.Text(string="Notes", help="Additional notes about the room availability")

    _sql_constraints = [
        ('unique_room_date', 'unique(room_id, date)', 'The room is already booked or unavailable on the selected date.')
    ]

    # Auto-generate Availability ID
    @api.model
    def create(self, vals):
        if vals.get('availability_id', _('New')) == _('New'):
            vals['availability_id'] = self.env['ir.sequence'].next_by_code('inntouch.calendar.availability') or _('New')
        result = super(InntouchCalendarAvailability, self).create(vals)
        return result
