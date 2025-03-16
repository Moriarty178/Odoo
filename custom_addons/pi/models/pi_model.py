from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError
from datetime import datetime

from odoo.release import description


class PiModel(models.Model):
    _name = 'pi.model'
    _description = 'Pi Model'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    # test = fields.Boolean(string="Active", default=True)
    test = fields.Selection([('true', 'True'), ('false', 'False')], string="Action", default='true')

    # Dùng "active" thay "test" sai vì "active" là field đặc biệt của odoo, khi nó = false => odoo sẽ ẩn đi thay vì xóa
    # one2many(class?, byField?)
    task_ids = fields.One2many('pi.task', 'pi_model_id', string="Tasks")

    def action_save_pi(self):
        """Dummy function to handle save action"""
        return True  # Odoo sẽ tự động lưu record, không cần làm gì thêm

    # constrain name is Unique???
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Tên đã tồn tại, vui lòng chọn tên khác!")

    # onchange
    @api.onchange('test')
    def _onchange_active(self):
        if not self.test:
            self.description = "Đã bị vô hiệu hóa"
            self.test = False
            # self.action_save_pi()

    # custom export: + DateTime colm
    @api.model
    def export_data(self, fields_to_export):
        data = super(PiModel, self).export_data(fields_to_export)
        # Custom: Thêm cột "Ngày tạo"
        for record in data['datas']:
            # record.append(fields.Datetime.now())
            record.append(datetime.now().strftime('%Y-%m-%d %H:%M%S'))
        return data

    # custom import
    # @api.model
    # def load(self, fields, data):
    #     for record in data:
    #         name = record[fields.index('name')] if 'name' in fields else None
    #         description = record[fields.index('description')] if 'description' in fields else None
    #
    #         # Kiểm tra nếu "name" bị trùng
    #         existing = self.search([('name', '=', name)], limit=1)
    #         if existing:
    #             raise exceptions.ValidationError(f"Tên '{name}' đã tồn tại!")
    #
    #         #thêm timestamp vào description nếu chưa có
    #         if not description:
    #             record[fields.index(
    #                 'description')] = f"Imported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    #
    #     # Gọi phương thức gốc của Odoo để import
    #     return super().load(fields, data)

    @api.model
    def load(self, fields, data):
        """Ghi đè phương thức load() để kiểm tra giá trị nhập từ file Excel có đúng với dropdown list không"""

        valid_action_values = {'True', 'False'}  # Các giá trị hợp lệ cho dropdown list

        for record in data:
            name = record[fields.index('name')] if 'name' in fields else None
            description = record[fields.index('description')] if 'description' in fields else None
            test = record[fields.index('test')] if 'test' in fields else None

            # Kiểm tra nếu name bị trùng
            existing = self.search([('name', '=', name)], limit=1)
            if existing:
                raise exceptions.ValidationError(f"Tên '{name}' đã tồn tại!")

            # Thêm timestamp vào description nếu chưa có
            if not description:
                record[fields.index('description')] = f"Imported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Chuẩn hóa 'test' -> giá trị hợp lệ, tránh "" hoặc None
            test = str(test).strip() if test else None

            # Kiểm tra giá trị của cột "Action" có hợp lệ không
            if test not in valid_action_values:
                raise exceptions.ValidationError(
                    f"Giá trị '{test}' trong cột 'Action' không hợp lệ! Chỉ chấp nhận: True hoặc False.")

        return super().load(fields, data)
