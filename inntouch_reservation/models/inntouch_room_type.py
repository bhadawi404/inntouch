from odoo import _, api, fields, models

class InntouchRoomType(models.Model):
    _name = 'inntouch.room.type'
    _description = 'Room Type'

    name = fields.Char('Room Type Name')
    property_id = fields.Many2one('inntouch.property', string='Property')
    description = fields.Text('Description')
    base_price = fields.Float('Base Price', default=1)
    max_occupancy = fields.Integer('Max Occupancy', default=1)
    amenities_ids = fields.One2many('inntouch.room.type.amenities', 'room_type_id', string='Amenities')
    product_categ_id = fields.Many2one(
        "product.category",
        "Product Category",
        delegate=True,
        required=True,
        copy=False,
        ondelete="cascade",
    )
    
    @api.model
    def create(self, vals):
        # Buat kategori produk dengan nama yang sama seperti Room Type Name
        if vals.get('name'):
            product_category = self.env['product.category'].create({
                'name': vals['name'],
                'category_type': 'room_type'
            })
            vals['product_categ_id'] = product_category.id
        return super(InntouchRoomType, self).create(vals)

    def write(self, vals):
        # Update nama kategori produk ketika Room Type Name diubah
        res = super(InntouchRoomType, self).write(vals)
        if vals.get('name'):
            for record in self:
                record.product_categ_id.name = vals['name']
        return res


class InntouchRoomTypeAmenities(models.Model):
    _name = 'inntouch.room.type.amenities'
    _description = 'Default Amenities Room Type'

    room_type_id = fields.Many2one('inntouch.room.type', string='Room Type')
    amenities_id = fields.Many2one('inntouch.amenities', string='Amenities')
