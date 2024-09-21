from odoo import models, fields, api, _

class InntouchPreferenceType(models.Model):
    _name = 'inntouch.preference.type'
    _description = 'Preference Type'

    name = fields.Char(string='Preference Type', required=True, help="The type of guest preference (e.g., Non-Smoking, Floor Preference, etc.)")
    description = fields.Text(string='Description', help="Description of this preference type")


class InntouchGuestPreferences(models.Model):
    _name = 'inntouch.guest.preferences'
    _description = 'Guest Preferences'

    name = fields.Char(string='Preference ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    guest_id = fields.Many2one('res.partner', string='Guest', required=True, help="The guest who has this preference")
    preference_type_id = fields.Many2one('inntouch.preference.type', string='Preference Type', required=True, help="Dynamic preference type for guest")
    description = fields.Text(string='Description', help="Description of the specific preference (e.g., Floor 5 or Mountain view)")

    @api.model
    def create(self, vals):
        if vals.get('preference_id', _('New')) == _('New'):
            vals['preference_id'] = self.env['ir.sequence'].next_by_code('inntouch.guest.preferences') or _('New')
        result = super(InntouchGuestPreferences, self).create(vals)
        return result
