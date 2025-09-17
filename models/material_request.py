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
    x_required_date = fields.Datetime(string='Required on', default=fields.Datetime.now, copy=False, tracking=True)
    x_requester_user_id = fields.Many2one('res.users', string='Requester', default=lambda self: self.env.user, copy=False, tracking=True)
    x_type = fields.Selection([
        ('consumption', 'Consumption'),
        ('transfer', 'Transfer'),
    ], string='Request Type', copy=False)
    x_consume_type = fields.Selection([
        ('out', 'Out'),
        ('in', 'In'),
    ], string='Consume Type', copy=False, default=False)
    x_src_location_id = fields.Many2one('stock.location', string='Source Location', copy=False)
    x_dest_location_id = fields.Many2one('stock.location', string='Destination Location', copy=False)
    x_line_ids = fields.One2many('amp.material.request.line', 'x_request_id', string='Line(s)', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New Material Request') == 'New Material Request':
                vals['name'] = self.env['ir.sequence'].next_by_code('material.request.seq')
        res = super(MaterialRequest, self).create(vals_list)
        return res


class MaterialRequestLine(models.Model):
    _name = 'amp.material.request.line'
    _description = 'Material Request Line'

    x_request_id = fields.Many2one('amp.material.request', string='Material Request', ondelete='cascade', copy=False)
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id', store=True)

    x_req_qty = fields.Float(string='Request Qty', digits='Product Unit of Measure', copy=False)
    x_processed_qty = fields.Float(string='Processed Qty', digits='Product Unit of Measure', copy=False, help="Qty being processed.")
    x_done_qty = fields.Float(string='Done Qty', digits='Product Unit of Measure', copy=False, help="Done Qty")
    x_outstanding_qty = fields.Float(string='Outstanding Qty', digits='Product Unit of Measure', copy=False, help="""Outstanding Qty = Request Qty - Processed Qty - Done Qty""")
    
    # product move
    x_move_ids = fields.One2many('stock.move', 'x_mr_line_id', string='Move(s)')
