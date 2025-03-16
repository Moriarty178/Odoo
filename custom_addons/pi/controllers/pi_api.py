from os.path import exists

from Demos.win32ts_logoff_disconnected import session
import json

from win32con import FALSE

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class PiAPIController(http.Controller):

    @http.route('/api/pi', auth="user", type='http', methods=['GET'], csrf=False)
    def get_pi_models(self):
        records = request.env['pi.model'].sudo().search([])
        data = records.read(['id', 'name', 'description', 'test'])
        # return request.make_response(json.dumps({'data': data}), headers=[('Content-Type', 'application/json')])
        return request.make_response(json.dumps({'data': data}))

    @http.route('/api/pi', auth='user', type='http', methods=['POST'], csrf=False)
    def post_pi_model(self):
        data = request.httprequest.get_json()  # Đọc JSON body từ request
        if not data or 'name' not in data:
            return request.make_response(json.dumps({'error': 'Name is required'}),
                                         [('Content-Type', 'application/json')])

        record = request.env['pi.model'].sudo().create(data)
        return request.make_response(json.dumps({'message': 'Ok record created', 'id': record.id}),
                                     [('Content-Type', 'application/json')])

    # API PUT
    @http.route('/api/pi/<int:record_id>', auth='user', type='http', methods=['PUT'], csrf=False)
    def put_pi_model(self, record_id):
        data = request.httprequest.get_json()

        if not data:
            return request.make_response(json.dumps({'message': 'No data provided'}))

        record = request.env['pi.model'].sudo().browse(record_id)

        if not record.exists():
            return request.make_response(json.dumps({'error': 'Not found record to update.'}))

        record.write(data)
        return request.make_response(json.dumps({'Message': 'Updated record.', 'id': record.id}))

    # API DELETE
    @http.route('/api/pi/<int:record_id>', auth='user', type='http', methods=['DELETE'], csrf=False)
    def delete_pi_model(self, record_id):
        record = request.env['pi.model'].sudo().browse(record_id)
        if not record.exists():
            return request.make_response(json.dumps({'error': 'Not found data to delete.'}))

        record.unlink()
        return request.make_response(json.dumps({'message': 'Deleted data.', 'id': record.id}))