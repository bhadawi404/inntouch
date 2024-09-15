from odoo import models, fields

class InntouchRoomPricing(models.Model):
    _name = 'inntouch.room.pricing'
    _description = 'Room Pricing'

    name = fields.Char(string="Pricing Name", required=True, help="Name of the pricing policy (e.g. High Season Pricing)")
    room_type_id = fields.Many2one('inntouch.room.type', string="Room Type", required=True, help="Type of room this pricing applies to")
    season = fields.Selection([
        ('low', 'Low Season'),
        ('mid', 'Mid Season'),
        ('high', 'High Season'),
        ('peak', 'Peak Season')
    ], string="Season", required=True, help="Season during which this pricing is valid")
    price_per_night = fields.Float(string="Price per Night", required=True, help="Price for one night stay")
    discount = fields.Float(string="Discount (%)", help="Discount applicable on the base price")
    effective_date = fields.Date(string="Effective Date", required=True, help="Date from which this pricing is applicable")
    end_date = fields.Date(string="End Date", help="Date until which this pricing is valid")
