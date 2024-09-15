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



class InntouchRoomTypeAmenities(models.Model):
    _name = 'inntouch.room.type.amenities'
    _description = 'Default Amenities Room Type'

    room_type_id = fields.Many2one('inntouch.room.type', string='Room Type')
    amenities_id = fields.Many2one('inntouch.amenities', string='Amenities')
