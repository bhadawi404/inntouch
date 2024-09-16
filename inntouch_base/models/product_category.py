from odoo import _, api, fields, models

class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    category_type = fields.Selection([
        ('room_type', 'Room Type'),
        ('product', 'Products'),
    ], string='Category Type')