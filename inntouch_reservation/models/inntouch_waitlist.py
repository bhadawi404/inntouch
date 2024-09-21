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
    def add_to_waitlist(self, guest_id, room_type_id, checkin_date, checkout_date, priority_level='low'):
        """
        Add a guest to the waitlist if the room is not available.
        """
        waitlist_entry = self.create({
            'guest_id': guest_id,
            'room_type_id': room_type_id,
            'requested_checkin_date': checkin_date,
            'requested_checkout_date': checkout_date,
            'priority_level': priority_level,
            'status': 'waiting',
        })
        return waitlist_entry

    @api.model
    def process_waitlist(self):
        """
        Process the waitlist periodically, checking for room availability for each guest.
        """
        waitlist_entries = self.search([('status', '=', 'waiting')])
        for entry in waitlist_entries:
            if self._is_room_available(entry.room_type_id, entry.requested_checkin_date, entry.requested_checkout_date):
                entry.status = 'confirmed'
                self._create_reservation(entry)  # Create a reservation automatically
                self._notify_guest(entry)  # Notify the guest via email or SMS
            else:
                entry.status = 'waiting'

    def _is_room_available(self, room_type, checkin_date, checkout_date):
        """
        A helper method to check if a room of the requested type is available for the requested dates.
        """
        available_rooms = self.env['inntouch.room'].search_count([
            ('room_type_id', '=', room_type.id),
            ('status', '=', 'available'),
            ('date', '>=', checkin_date),
            ('date', '<=', checkout_date)
        ])
        return available_rooms > 0

    def _create_reservation(self, waitlist_entry):
        """
        Automatically create a reservation when a room becomes available.
        """
        self.env['inntouch.reservation'].create({
            'guest_id': waitlist_entry.guest_id.id,
            'room_type_id': waitlist_entry.room_type_id.id,
            'check_in_date': waitlist_entry.requested_checkin_date,
            'check_out_date': waitlist_entry.requested_checkout_date,
            'status': 'confirmed'
        })

    def _notify_guest(self, waitlist_entry):
        """
        Notify the guest via email when their waitlist reservation is confirmed.
        """
        template = self.env.ref('your_module.waitlist_confirmation_email_template')
        self.env['mail.template'].browse(template.id).send_mail(waitlist_entry.id, force_send=True)

