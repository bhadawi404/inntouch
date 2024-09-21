from odoo import _, api, fields, models

class InntouchServiceType(models.Model):
    _name = 'inntouch.service.type'
    _description = 'Service Type'


    name = fields.Char('Service Type Name')
    description = fields.Text('Description')