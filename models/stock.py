from odoo import api, fields, models, _


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    # mr = material request
    x_mr_id = fields.Many2one('amp.material.request', string='Material Request', copy=False)


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    # mr = material request
    x_mr_id = fields.Many2one(related='picking_id.x_mr_id', store=True)
    x_mr_line_id = fields.Many2one('amp.material.request.line', string='Material Request Line', copy=False)
