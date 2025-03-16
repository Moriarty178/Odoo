from odoo import models, fields, api
import base64
import io
import pandas as pd
import json

class PiImportWizard(models.TransientModel):
    _name = 'pi.import.wizard'
    _description = 'Wizard Import Pi Model'

    file = fields.Binary(string="Upload File (xlsx)", required=True)
    filename = fields.Char(string="Filename")

    # Trường lưu dữ liệu đọc từ file xlsx
    data_preview = fields.Text(string="Data Preview", readonly=True)

    def action_process_file(self):
        """Đọc file xlsx, trích xuất dữ liệu và hiển thị cho người dùng xác nhận"""
        self.ensure_one()

        # Reset data_preview trước khi xử lý file mới
        self.data_preview = False

        if not self.file:
            return

        # Đọc nội dung file
        file_content = base64.b64decode(self.file)
        file_stream = io.BytesIO(file_content)

        try:
            df = pd.read_excel(file_stream, dtype=str)  # Đọc file excel
        except Exception as e:
            raise models.ValidationError(f"Lỗi khi đọc file: {str(e)}")

        # Chuyển dữ liệu thành JSON để hiển thị trên giao diện
        records = df.to_dict(orient="records")

        # Ghi lại dữ liệu mới
        self.write({'data_preview': json.dumps(records, indent=2, ensure_ascii=False)})

        return {
            'name': "Xác nhận dữ liệu import",
            'type': 'ir.actions.act_window',
            'res_model': 'pi.import.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    @api.onchange('file')
    def _onchange_file(self):
        """Tự động cập nhật data_preview khi file thay đổi"""
        if not self.file:
            self.data_preview = False
            return

        # Đọc nội dung file
        file_content = base64.b64decode(self.file)
        file_stream = io.BytesIO(file_content)

        try:
            df = pd.read_excel(file_stream, dtype=str)
        except Exception as e:
            raise models.ValidationError(f"Lỗi khi đọc file: {str(e)}")

        # Chuyển dữ liệu thành JSON
        self.data_preview = json.dumps(df.to_dict(orient="records"), indent=2, ensure_ascii=False)

    def action_confirm_import(self):
        """Xác nhận import dữ liệu"""
        self.ensure_one()
        if not self.data_preview:
            return

        # Parse data từ preview
        try:
            records = json.loads(self.data_preview)
        except json.JSONDecodeError:
            raise models.ValidationError("Lỗi phân tích JSON từ dữ liệu import.")

        # Thêm dữ liệu vào pi.model
        for record in records:
            self.env['pi.model'].create({
                'name': record.get('name'),
                'description': record.get('description'),
                # 'test': record.get('test', 'true'),  # Mặc định là 'true'
                'test': record.get('test') if record.get('test') in ['true', 'false'] else 'true',
            })

        return {'type': 'ir.actions.act_window_close'}  # Đóng wizard
