from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError


class WizardCreatePicking(models.TransientModel):
    _name = 'amp.wizard.create.picking'
    _description = 'Wizard to create material request picking'

    x_src_location_id = fields.Many2one("stock.location", string="Source Location")
    x_dest_location_id = fields.Many2one("stock.location", string="Destination Location")
    x_picking_type_id = fields.Many2one("stock.picking.type", string="Picking Type")
    x_mr_id = fields.Many2one('amp.material.request', string='Material Request')
    x_line_ids = fields.One2many('amp.wizard.create.picking.line', 'x_wizard_id', string='Line(s)')

    def action_create_picking(self):
        picking_vals = self._prepare_picking()
        picking = self.env['stock.picking'].with_user(SUPERUSER_ID).create(picking_vals)

    def _prepare_picking(self):
        return {
            'picking_type_id': self.x_picking_type_id.id,
            'partner_id': self.x_mr_id.x_requester_user_id.partner_id.id,
            'user_id': False,
            'date': self.x_mr_id.x_required_date,
            'scheduled_date': self.x_mr_id.x_required_date,
            'x_trans_dttm': self.x_mr_id.x_required_date,
            'origin': self.x_mr_id.name,
            'location_id': self.x_src_location_id.id,
            'location_dest_id': self.x_dest_location_id.id,
            'company_id': self.env.company.id,
            'x_mr_id': self.x_mr_id.id,
            'state': 'draft',
        }

class WizardCreatePickingLine(models.TransientModel):
    _name = 'amp.wizard.create.picking.line'
    _description = 'Wizard to create material request picking line'

    x_wizard_id = fields.Many2one('amp.wizard.create.picking', string='Wizard Create Picking')
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id')
    x_mr_line_id = fields.Many2one('amp.material.request.line', string='Material Request Line')
    x_qty = fields.Float(string='Qty', default=0, digits='Product Unit of Measure')
