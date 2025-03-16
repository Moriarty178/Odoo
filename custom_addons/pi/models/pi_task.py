from odoo import models, fields, api, _

class PiTask(models.Model):
    _name = 'pi.task'
    _description = 'Pi Task'

    name = fields.Char(string="Task Name", required=True)
    # foreign_key ref to -> pi_model
    pi_model_id = fields.Many2one('pi.model', string="Pi Model")
