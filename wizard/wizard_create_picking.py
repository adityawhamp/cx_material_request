from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizardCreatePicking(models.TransientModel):
    _name = 'amp.wizard.create.picking'
    _description = 'Wizard to create material request picking'

    x_src_location_id = fields.Many2one("stock.location", string="Source Location")
    x_dest_location_id = fields.Many2one("stock.location", string="Destination Location")
    x_mr_id = fields.Many2one('amp.material.request', string='Material Request')

    def action_create_picking(self):
        pass
    
class WizardCreatePickingLine(models.TransientModel):
    _name = 'amp.wizard.create.picking.line'
    _description = 'Wizard to create material request picking line'
