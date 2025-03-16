from pkg_resources import require

from odoo import models, fields

class PiModelExtend(models.Model):
    _inherit = 'pi.model'

    new_field = fields.Char(string="New Field" )