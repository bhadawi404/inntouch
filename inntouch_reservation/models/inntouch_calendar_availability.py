from datetime import timedelta
from odoo import models, fields, api, _

class InntouchCalendarAvailability(models.Model):
    _name = 'inntouch.calendar.availability'
    _description = 'Calendar Availability'

    room_id = fields.Many2one('inntouch.room', string="Room", required=True, help="Room associated with this availability record")
    date = fields.Date(string="Date", required=True, help="The date for which the availability is being recorded")
    is_available = fields.Boolean(string="Is Available", default=True, help="Indicates if the room is available on this date")
    notes = fields.Text(string="Notes", help="Additional notes about the room availability")
    date_start = fields.Date(string="Start Date", default=lambda self: self.date)
    date_end = fields.Date(string="End Date", default=lambda self: self.date)

    

    _sql_constraints = [
        ('unique_room_date', 'unique(room_id, date)', 'The room is already booked or unavailable on the selected date.')
    ]

    def mark_as_booked(self, start_date, end_date, room_id):
        """Mark the room as booked in the calendar availability for a date range."""
        for date in self._generate_date_range(start_date, end_date):
            self.env['inntouch.calendar.availability'].create({
                'room_id': room_id,
                'date': date,
                'is_available': False
            })

    def mark_as_available(self, start_date, end_date, room_id):
        """Mark the room as available in the calendar availability for a date range."""
        availabilities = self.env['inntouch.calendar.availability'].search([
            ('room_id', '=', room_id),
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ])
        availabilities.write({'is_available': True})


    def _generate_date_range(self, check_in_date, check_out_date):
        """Helper method to generate date range between check-in and check-out."""
        start_date = fields.Date.from_string(check_in_date)
        end_date = fields.Date.from_string(check_out_date)
        date_list = []
        while start_date <= end_date:
            date_list.append(start_date)
            start_date += timedelta(days=1)
        return date_list
