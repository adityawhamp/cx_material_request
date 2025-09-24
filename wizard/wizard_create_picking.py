from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError


class WizardCreatePicking(models.TransientModel):
    _name = 'amp.wizard.create.picking'
    _description = 'Wizard to create material request picking'

    x_mr_id = fields.Many2one('amp.material.request', string='Material Request')
    x_line_ids = fields.One2many('amp.wizard.create.picking.line', 'x_wizard_id', string='Line(s)')

    def action_create_picking(self):
        lines_to_process = self.x_line_ids.filtered(lambda l: float_compare(l.x_qty, 0, precision_rounding=l.x_uom_id.rounding) == 1)
        if lines_to_process:
            self.x_mr_id._create_picking(lines_to_process)


class WizardCreatePickingLine(models.TransientModel):
    _name = 'amp.wizard.create.picking.line'
    _description = 'Wizard to create material request picking line'

    x_wizard_id = fields.Many2one('amp.wizard.create.picking', string='Wizard Create Picking')
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id')
    x_mr_line_id = fields.Many2one('amp.material.request.line', string='Material Request Line')
    x_qty = fields.Float(string='Qty', default=0, digits='Product Unit of Measure')
