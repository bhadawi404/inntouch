from odoo import _, api, fields, models

class InntouchRoom(models.Model):
    _name = 'inntouch.room'
    _description = 'Room'

    name = fields.Char('Room Name')
    room_number = fields.Char('Room Number', required=True)
    room_type_id = fields.Many2one('inntouch.room.type', string='Room Type', required=True)
    floor = fields.Integer('Floor')
    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
        ('unavailable', 'Unavailable'),
    ], string='State', default='available', required=True)
    max_occupancy = fields.Integer('Max Occupancy', related='room_type_id.max_occupancy', readonly=True)
    price = fields.Float('Price', related='room_type_id.base_price', readonly=True)
    amenities_ids = fields.One2many(
        'inntouch.room.type.amenities', 
        compute='_compute_amenities_ids', 
        string='Amenities', 
        readonly=True
    )
    description = fields.Text('Description')
    product_id = fields.Many2one('product.product', string="Product", delegate=True, required=True, ondelete="cascade")
    availability_ids = fields.One2many('inntouch.calendar.availability', 'room_id', string="Availability")
    
    @api.model
    def create(self, vals):
        # Buat product yang terkait dengan kamar
        if vals.get('room_number'):
            product_vals = {
                'name': 'Room ' + vals['room_number'],
                'type': 'service',  # Menandakan bahwa kamar adalah produk jasa
            }
            product = self.env['product.product'].create(product_vals)
            vals['product_id'] = product.id
        return super(InntouchRoom, self).create(vals)

    def write(self, vals):
        # Perbarui nama produk saat nomor kamar berubah
        if vals.get('room_number'):
            for record in self:
                if record.product_id:
                    record.product_id.name = 'Room ' + vals['room_number']
        return super(InntouchRoom, self).write(vals)

    @api.depends('room_type_id')
    def _compute_amenities_ids(self):
        for record in self:
            if record.room_type_id:
                record.amenities_ids = record.room_type_id.amenities_ids
            else:
                record.amenities_ids = False