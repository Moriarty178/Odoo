from odoo import fields, models, api


class Category(models.Model):
    _name = 'pi.category'
    _description = 'Description Category'

    name = fields.Char(string="Name", required=True)
    products = fields.One2many('pi.product', 'category_id', string="Products")

