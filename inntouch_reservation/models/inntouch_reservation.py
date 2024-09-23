from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]
class InntouchReservation(models.Model):
    _name = 'inntouch.reservation'
    _description = 'Reservation'

    name = fields.Char('Reservation Number', default='New')
    guest_id = fields.Many2one('res.partner', string="Guest", required=True, help="Guest making the reservation")
    room_id = fields.Many2one('inntouch.room', string="Room", domain="[('state', '=', 'available')]", required=True, help="Room being reserved")
    room_type_id = fields.Many2one('inntouch.room.type', string="Room Type", required=True, help="Type of room reserved")
    check_in_date = fields.Date(string="Check-in Date", required=True)
    check_out_date = fields.Date(string="Check-out Date", required=True)
    number_of_guests = fields.Integer('Number of Guests', compute='_compute_number_of_guest', store=True)
    adult = fields.Integer('Adult')
    child = fields.Integer('Child')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('waiting', 'Waiting'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('canceled', 'Canceled')
    ], string="Status", default="draft", required=True)
    total_price = fields.Float(string="Total Price", compute="_compute_total_price")
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], string="Payment Status", default="unpaid")
    special_requests_ids = fields.One2many('inntouch.special.request', 'reservation_id', string='Special Requests')
    reservation_source_id = fields.Many2one('inntouch.booking.source', string='Source')
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority Level", default=AVAILABLE_PRIORITIES[0][0])
    
    
        
    @api.depends('adult', 'child')
    def _compute_number_of_guest(self):
        self.number_of_guests = self.child + self.adult

    @api.depends('room_id', 'check_in_date', 'check_out_date')
    def _compute_total_price(self):
        """Compute the total price based on room price and duration of stay."""
        for record in self:
            if record.room_id and record.check_in_date and record.check_out_date:
                nights = (record.check_out_date - record.check_in_date).days
                price_per_night = record.room_type_id.get_current_price(record.check_in_date, record.check_out_date)
                record.total_price = price_per_night * nights
            else:
                record.total_price = 0.0
    @api.model
    def create(self, vals):
        """Override create method to handle room availability check and status update."""
        res = super(InntouchReservation, self).create(vals)
        if res.room_id:
            if not res._check_room_availability():
                # Add to waitlist if room is not available
                res.write({'status': 'waiting'})
                self.env['inntouch.waitlist'].create({
                    'guest_id': res.guest_id.id,
                    'room_type_id': res.room_type_id.id,
                    'requested_checkin_date': res.check_in_date,
                    'requested_checkout_date': res.check_out_date,
                    'status': 'waiting'
                })
            else:
                # Mark room as booked in Calendar Availability
                availability_model = self.env['inntouch.calendar.availability']
                availability_model.mark_as_booked(res.check_in_date, res.check_out_date, res.room_id.id)
                res.write({'status': 'confirmed'})
                res.room_id.state = 'occupied'
        return res

    def cancel_reservation(self):
        """Cancel the reservation and free up the room."""
        self.write({'status': 'canceled'})
        availability_model = self.env['inntouch.calendar.availability']
        availability_model.mark_as_available(self.check_in_date, self.check_out_date, self.room_id.id)
        self._process_waitlist()

    def _check_room_availability(self):
        """Check if room is available during the requested dates."""
        availability_records = self.env['inntouch.calendar.availability'].search([
            ('room_id', '=', self.room_id.id),
            ('date', '>=', self.check_in_date),
            ('date', '<=', self.check_out_date),
            ('is_available', '=', False)
        ])
        return not bool(availability_records)

    def _process_waitlist(self):
        """Process the waitlist when a reservation is canceled."""
        waitlist_records = self.env['inntouch.waitlist'].search([
            ('room_type_id', '=', self.room_type_id.id),
            ('status', '=', 'waiting')
        ], order="priority_level asc")
        if waitlist_records:
            for waitlist in waitlist_records:
                if self._check_room_availability():
                    self.env['inntouch.reservation'].create({
                        'guest_id': waitlist.guest_id.id,
                        'room_id': self.room_id.id,
                        'room_type_id': waitlist.room_type_id.id,
                        'check_in_date': waitlist.requested_checkin_date,
                        'check_out_date': waitlist.requested_checkout_date,
                        'status': 'confirmed'
                    })
                    waitlist.write({'status': 'processed'})
                    break
