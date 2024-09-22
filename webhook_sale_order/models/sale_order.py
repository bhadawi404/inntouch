import requests
from odoo import _, api, models
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    
    @api.model
    def create(self, vals):
        # Call super to create the record
        record = super(SaleOrderInherit, self).create(vals)

        webhook_sale_active = self.env['ir.config_parameter'].sudo().get_param('webhook_sale_order.is_active_webhook_sale')
        if webhook_sale_active:
            # After creating the record, trigger the webhook
            record._send_webhook(vals)

        return record
    
    def _send_webhook(self, vals):
        """Method to send quotation data to Odoo Enterprise using webhook."""
        # Prepare the payload data

        #partner_data
        partner_data = {
            'name': self.partner_id.name,
            'email': self.partner_id.email,
            'phone': self.partner_id.phone,
            'street': self.partner_id.street,
        }
        


        order_lines_data = [{
            'product': {
                'name': line.product_id.name,
                'default_code': line.product_id.default_code,
                'list_price': line.product_id.lst_price,
                'type': line.product_id.type,
            },
            'product_uom_qty': line.product_uom_qty,
            'price_unit': line.price_unit,
            'lead_time': line.customer_lead,
            'tax_ids': [(6, 0, line.tax_id.ids)]
        } for line in self.order_line]

        # Generate payload with external ID
        payload = {
            'name': self.name,
            'amount_total': self.amount_total,
            'payment_term': self.payment_term_id.name,
            'sale_person_email': self.user_id.email,
            'team_name': self.team_id.name,
            'partner': partner_data,
            'validity_date': self.validity_date.strftime('%Y-%m-%d') if self.validity_date else None,  # Convert to string
            'date_order': self.date_order.strftime('%Y-%m-%d %H:%M:%S') if self.date_order else None,  # Convert to string
            'order_lines': order_lines_data,
        }

        # Send the payload to the external Odoo Enterprise instance
        # webhook_url = 'https://zensoftwareinc-instalimb.odoo.com/web/hook/09737bd8-c8b6-4e34-966e-aebb833d4eab'
        webhook_sale_order_url = self.env['ir.config_parameter'].sudo().get_param('webhook_sale_order.webhook_sale_order_url')

        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_sale_order_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("Data successfully sent to Odoo Enterprise.")
        else:
            print(f"Failed to send data: {response.text}")