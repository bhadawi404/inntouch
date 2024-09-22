from odoo import models, fields, api
from datetime import datetime, timedelta

from odoo.exceptions import ValidationError


class ResConfigWebhookSaleOrder(models.TransientModel):
    _inherit = 'res.config.settings'

    is_active_webhook_sale = fields.Boolean('Automation Webhook Sale Order', config_parameter="webhook_sale_order.is_active_webhook_sale")
    webhook_sale_order_url = fields.Char('URL Webhook Sale', config_parameter="webhook_sale_order.webhook_sale_order_url")