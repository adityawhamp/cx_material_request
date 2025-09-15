from odoo import api, fields, models, _


class MaterialRequest(models.Model):
    _name = 'amp.material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Ref', required=True, copy=False, readonly=True,
                       index='trigram', default=lambda self: _('New Material Request'))
    