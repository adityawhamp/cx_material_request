from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizardCreatePicking(models.TransientModel):
    _name = 'amp.wizard.create.picking'
    _description = 'Wizard to create material request picking'

    x_src_location_id = fields.Many2one("stock.location", string="Source Location")
    x_dest_location_id = fields.Many2one("stock.location", string="Destination Location")
    x_mr_id = fields.Many2one('amp.material.request', string='Material Request')
    x_line_ids = fields.One2many('amp.wizard.create.picking.line', 'x_wizard_id', string='Line(s)')

    def action_create_picking(self):
        pass


class WizardCreatePickingLine(models.TransientModel):
    _name = 'amp.wizard.create.picking.line'
    _description = 'Wizard to create material request picking line'

    x_wizard_id = fields.Many2one('amp.wizard.create.picking', string='Wizard Create Picking')
    x_product_id = fields.Many2one('product.product', string='Product')
    x_uom_id = fields.Many2one(related='x_product_id.uom_id')
    x_mr_line_id = fields.Many2one('amp.material.request.line', string='Material Request Line')
    x_qty = fields.Float(string='Qty', default=0, digits='Product Unit of Measure')
