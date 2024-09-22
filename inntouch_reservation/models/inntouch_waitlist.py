from odoo import models, fields, api
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
    _order = 'priority_level desc, requested_checkin_date'

    name = fields.Char('Waitlist Number', default='New')
    guest_id = fields.Many2one('res.partner', string="Guest", required=True, help="Guest who is on the waitlist")
    room_type_id = fields.Many2one('inntouch.room.type', string="Room Type", required=True, help="Type of room requested")
    requested_checkin_date = fields.Date(string="Requested Check-in Date", required=True, help="Date of requested check-in")
    requested_checkout_date = fields.Date(string="Requested Check-out Date", required=True, help="Date of requested check-out")
    priority_level = fields.Selection(AVAILABLE_PRIORITIES, string="Priority Level", default=AVAILABLE_PRIORITIES[0][0], required=True, help="Priority level of the guest in the waitlist")
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], string="Status", default='waiting', required=True, help="Current status of the waitlist entry")

    @api.model
    def add_to_waitlist(self, reservation):
        """
        Adds a reservation to the waitlist if the room is not available.
        """
        self.create({
            'guest_id': reservation.guest_id.id,
            'room_type_id': reservation.room_id.room_type_id.id,
            'requested_checkin_date': reservation.check_in_date,
            'requested_checkout_date': reservation.check_out_date,
            'priority_level': 1,
        })

    def process_waitlist(self, room_id):
        """
        Process the waitlist when a room becomes available.
        """
        # Get all waitlist entries for this room type with status pending
        waitlist_entries = self.search([('room_type_id', '=', room_id.room_type_id.id), ('status', '=', 'pending')], order='priority_level asc')
        
        if waitlist_entries:
            for entry in waitlist_entries:
                calendar_avail = self.env['inntouch.calendar.availability']
                
                # Check if the room is available for the requested dates
                if calendar_avail.is_room_available(room_id.id, entry.requested_checkin_date, entry.requested_checkout_date):
                    # Create reservation for the first in line and update status
                    self.env['inntouch.reservation'].create({
                        'guest_id': entry.guest_id.id,
                        'room_id': room_id.id,
                        'check_in_date': entry.requested_checkin_date,
                        'check_out_date': entry.requested_checkout_date,
                        'status': 'confirmed'
                    })
                    # Update calendar availability
                    calendar_avail.update_availability(room_id.id, entry.requested_checkin_date, entry.requested_checkout_date, False)
                    # Mark the entry as processed
                    entry.status = 'processed'
                    break  # Only process one waitlist entry at a time
