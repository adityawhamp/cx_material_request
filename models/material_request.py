from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    _name = 'amp.material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('x_is_confirmed', 'x_is_closed')
    def _compute_state(self):
        for rec in self:
            if rec.x_is_closed:
                rec.status = 'close'
            elif rec.x_is_confirmed:
                rec.status = 'open'
            else:
                rec.status = 'draft'

    name = fields.Char(string='Ref', required=True, copy=False, readonly=True,
                       index='trigram', default=lambda self: _('New Material Request'))
    x_is_confirmed = fields.Boolean(string='Is Confirmed?', default=False, copy=False)
    x_is_closed = fields.Boolean(string='Is Closed?', default=False, copy=False)
    status = fields.Selection(string='State', selection=[
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('close', 'Close'),
    ], default='draft', copy=False, tracking=True, compute='_compute_state', store=True)
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

    def validation(self, action):
        self.ensure_one()
        if action == 'confirm':
            if self.x_type:
                if self.x_type == 'transfer':
                    if not self.x_required_date:
                        raise ValidationError(_('Required date is empty.'))
                        
                    if not self.x_src_location_id:
                        raise ValidationError(_('Source location is empty.'))
                    
                    if not self.x_dest_location_id:
                        raise ValidationError(_('Destination location is empty.'))
                    
                    if self.x_line_ids:
                        invalid_lines = self.x_line_ids.filtered(lambda l: float_compare(l.x_req_qty, 0, precision_rounding=l.x_uom_id.rounding) != 1)
                        if invalid_lines:
                            raise ValidationError(_('There is request qty <= 0.'))    
                    else:
                        raise ValidationError(_('Request line is empty.'))

            else:
                raise ValidationError(_('Request type is empty.'))

    def action_confirm(self):
        for rec in self:
            rec.validation('confirm')
            rec.x_is_confirmed = True
    
    def action_reset_to_draft(self):
        for rec in self:
            rec.x_is_confirmed = False

    def action_create_picking(self):
        title = 'Material Request'
        view = self.env.ref('cx_material_request.wizard_create_picking_view_form')
        return {
            'name': _(title),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'amp.wizard.create.picking',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_x_mr_id': self.id,
                'default_x_src_location_id': self.x_src_location_id.id,
                'default_x_dest_location_id': self.x_dest_location_id.id,
            }
        }


class MaterialRequestLine(models.Model):
    _name = 'amp.material.request.line'
    _description = 'Material Request Line'

    x_request_id = fields.Many2one('amp.material.request', string='Material Request', ondelete='cascade', copy=False)
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id', store=True)

    x_req_qty = fields.Float(string='Request Qty', digits='Product Unit of Measure', copy=False)
    x_processed_qty = fields.Float(string='Processed Qty', digits='Product Unit of Measure',  help="Qty being processed.")
    x_done_qty = fields.Float(string='Done Qty', digits='Product Unit of Measure', copy=False, help="Done Qty")
    x_outstanding_qty = fields.Float(string='Outstanding Qty', digits='Product Unit of Measure', copy=False, help="""Outstanding Qty = Request Qty - Processed Qty - Done Qty""")
    
    # product move
    x_move_ids = fields.One2many('stock.move', 'x_mr_line_id', string='Move(s)', copy=False)
