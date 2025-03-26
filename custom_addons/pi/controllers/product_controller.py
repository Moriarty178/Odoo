import json

from win32com.universal import Method

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class ProductController(http.Controller):
    @http.route('/api/v1/products', auth="user", type='http', methods=['GET'], csrf=False)
    def get_products(self):
        records = request.env['pi.product'].sudo().search([])
        data = records.read(['id', 'name', 'price', 'discount_price'])
        return json.dumps({'products': data})

    @http.route('/api/v1/product', auth='user', type='http', methods=['POST'], csrf=False)
    def post_product(self):
        data = request.httprequest.get_json()
        if not data or 'name' not in data:
            raise json.dumps({'error': 'Data not found or name not in data.'})

        record = request.env['pi.product'].sudo().create(data)
        return json.dumps({'message': 'Created record.', 'id': record.id})

    @http.route('/api/v1/product/<int:record_id>', auth='user', type='http', methods=['PUT'], csrf=False)
    def update_product(self, record_id):
        # get body json from request
        data = request.httprequest.get_json()
        if not data:
            raise json.dumps({'error': 'No data to update.'})

        # find record
        record = request.env['pi.product'].sudo().search([("id", "=", record_id)])

        if not record:
            raise json.dumps({'error': 'Not found record to update.'})

        # update record with data
        record.write(data)
        return json.dumps({'message': 'Updated successfully.', 'id': record.id})

    @http.route('/api/v1/product/<int:record_id>', auth='user', type='http', methods=['DELETE'], csrf=False)
    def delete_product(self, record_id):
        record = request.env['pi.product'].sudo().browse(record_id)

        if not record:
            raise json.dumps({'error': "Not found data to delete."})

        record.unlink()
        return json.dumps({'message': 'Deleted data.', 'id': record.id})

    # @http.route('/api/v1/products/search', auth="user", type='http', methods=['GET'], csrf=False)
    # def search_products(self):
    #     params = request.params
    #     name = params.get('name')
    #     price_from = params.get('price_from')
    #     price_to = params.get('price_to')
    #
    #     domain = []
    #     if name:
    #         domain.append(('name', 'ilike', name))
    #     if price_from:
    #         domain.append(('price', '>=', float(price_from)))
    #     if price_to:
    #         domain.append(('price', '<=', float(price_to)))
    #
    #     records = request.env['pi.product'].sudo().search(domain)
    #     data = records.read(['id', 'name', 'price', 'discount_price'])
    #     return json.dumps({'products': data})
    #
    # @http.route('/api/v1/products/category/<int:category_id>', auth="user", type='http', methods=['GET'], csrf=False)
    # def get_products_by_category(self, category_id):
    #     category = request.env['pi.category'].sudo().browse(category_id)
    #     if not category:
    #         raise json.dumps({'error': 'Not found category.'})
    #
    #     records = request.env['pi.product'].sudo().search([('category_id', '=', category_id)])
    #     data = records.read(['id', 'name', 'price', 'discount_price'])
    #     return json.dumps({'products': data})
    #
    # @http.route('/api/v1/cart/add', auth='user', type='http', methods=['POST'], csrf=False)
    # def add_to_cart(self):
    #     data = request.httprequest.get_json()
    #     if not data or 'product_id' not in data:
    #         raise json.dumps({'error': 'Data not found or product_id not in data.'})
    #
    #     product_id = data['product_id']
    #     product = request.env['pi.product'].sudo().browse(product_id)
    #     if not product:
    #         raise json.dumps({'error': 'Not found product.'})
    #
    #     cart = request.env['pi.cart'].sudo().create({'product_id': product_id, 'quantity': 1})
    #     return json.dumps({'message': 'Added to cart.', 'cart_id': cart.id})
    #
    # @http.route('/api/v1/cart', auth='user', type='http', methods=['GET'], csrf=False)
    # def view_cart(self):
    #     cart = request.env['pi.cart'].sudo().search([('user_id', '=', request.uid)])
    #     data = cart.read(['id', 'product_id', 'quantity'])
    #     return json.dumps({'cart': data})

# search(["id", "=", record_id]) <=> browse(record_id)
