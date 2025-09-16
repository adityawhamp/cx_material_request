from odoo import api, fields, models, _
from odoo.tools import float_compare


class MaterialRequest(models.Model):
    _name = 'amp.material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # @api.depends('x_line_ids', 'x_line_ids.x_actual_qty', 'x_picking_ids')
    # def _compute_state(self):
    #     for rec in self:
    #         if rec.x_state in ('open', 'progress', 'close'):
    #             # outstanding
    #             ostd_lines = rec.x_line_ids.filtered(
    #                 lambda l: float_compare(l.x_request_qty - l.x_actual_qty, 0.0000, precision_digits=4) == 1)
    #             active_pickings = rec.x_picking_ids.filtered(lambda p: p.state != 'cancel')
    #             if ostd_lines:
    #                 if active_pickings:
    #                     rec.x_state = 'progress'
    #                 else:
    #                     rec.x_state = 'open'
    #             else:
    #                 rec.x_state = 'close'

    name = fields.Char(string='Ref', required=True, copy=False, readonly=True,
                       index='trigram', default=lambda self: _('New Material Request'))
    # status = fields.Selection(string='State', selection=[
    #     ('draft', 'Draft'),
    #     ('open', 'Open'),
    #     ('progress', 'In Progress'),
    #     ('close', 'Close'),
    # ], default='draft', copy=False, tracking=True, compute='_compute_state', store=True)
    x_line_ids = fields.One2many('amp.material.request.line', 'x_request_id', string='Line(s)', copy=False)


class MaterialRequestLine(models.Model):
    _name = 'amp.material.request.line'
    _description = 'Material Request Line'

    x_request_id = fields.Many2one('amp.material.request', string='Material Request', ondelete='cascade', copy=False)
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id', store=True)
