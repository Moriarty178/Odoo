from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class Product(models.Model):
    _name = 'pi.product'
    _description = 'Pi Product'

    name = fields.Char(string="Name", required=True)
    price = fields.Float(string="Price")
    discount_price = fields.Float(string="Discount Price", compute="_compute_discount")

    category_id = fields.Many2one('pi.category', string="Category")


    ### Decorator

    @api.depends('price') # Tính toán giá trị dựa trên các trường khác (kiểu như thuộc tính dẫn xuất tron csdl)
    def _compute_discount(self):
        for rec in self:
            if rec.price < 1500:
                rec.discount_price = rec.price * 0.85

    @api.constrains('price') # Kiểm tra tính hợp lệ giá trị của trường
    def _check_price(self):
        if self.price < 10:
            raise ValidationError("Price must be greater than 10")

    @api.onchange('price') # xử lý khi thay đổi dữ liệu của trường
    def _onchange_price(self):
        if self.price >= 1500:
            self.price = self.price - 100

    @api.model # override method
    def export_data(self, fields_to_export):
        data = super(Product, self).export_data(fields_to_export)

        # Thêm cót "Ngày tạo" khi export
        for record in data['datas']:
            record.append(fields.datetime.now())
        return data