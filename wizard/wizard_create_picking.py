from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizardCreatePicking(models.TransientModel):
    _name = 'amp.wizard.create.picking'
    _description = 'Wizard to create material request picking'

    
