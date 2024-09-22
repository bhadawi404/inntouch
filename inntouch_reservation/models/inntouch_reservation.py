from odoo import _, api, fields, models
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
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True,default=AVAILABLE_PRIORITIES[0][0])
    guest_id = fields.Many2one('res.partner', string='Guest', required=True)
    room_id = fields.Many2one('inntouch.room', string='Room', required=True)
    check_in_date = fields.Datetime('Check-in Date', required=True)
    check_out_date = fields.Datetime('Check-out Date', required=True)
    number_of_guests = fields.Integer('Number of Guests', compute='_compute_number_of_guest', store=True)
    adult = fields.Integer('Adult')
    child = fields.Integer('Child')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('canceled', 'Canceled'),
    ], string='Status', default='pending', required=True)
    booking_date = fields.Datetime('Booking Date', default=fields.Datetime.now, readonly=True)
    special_requests_ids = fields.One2many('inntouch.special.request', 'reservation_id', string='Special Requests')
    reservation_source_id = fields.Many2one('inntouch.booking.source', string='Source')
    total_price = fields.Float('Total Price', compute='_compute_total_price', readonly=True, store=True)
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
    ], string='Payment Status', default='unpaid')

    @api.depends('check_in_date', 'check_out_date', 'room_id')
    def _compute_total_price(self):
        for reservation in self:
            nights = (reservation.check_out_date - reservation.check_in_date).days
            price_per_night = reservation.room_type_id.get_current_price(reservation.check_in_date, reservation.check_out_date)
            reservation.total_price = price_per_night * nights

    @api.depends('adult', 'child')
    def _compute_number_of_guest(self):
        self.number_of_guests = self.child + self.adult
    
    @api.model
    def create(self, vals):
        reservation = super(InntouchReservation, self).create(vals)
        calendar_avail = self.env['inntouch.calendar.availability']
        
        # Check availability of the room
        if reservation.status == 'confirmed':
            if not calendar_avail.is_room_available(reservation.room_id.id, reservation.check_in_date, reservation.check_out_date):
                self.env['inntouch.waitlist'].add_to_waitlist(reservation)
            else:
                calendar_avail.update_availability(reservation.room_id.id, reservation.check_in_date, reservation.check_out_date, False)
        
        return reservation
    
    def write(self, vals):
        res = super(InntouchReservation, self).write(vals)
        calendar_avail = self.env['inntouch.calendar.availability']
        
        if 'status' in vals and vals['status'] == 'canceled':
            calendar_avail.update_availability(self.room_id.id, self.check_in_date, self.check_out_date, True)
            self.env['inntouch.waitlist'].process_waitlist(self.room_id.id)
        
        return res


