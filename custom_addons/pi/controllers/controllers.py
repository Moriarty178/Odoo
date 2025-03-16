# -*- coding: utf-8 -*-
# from odoo import http


# class Pi(http.Controller):
#     @http.route('/pi/pi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pi/pi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pi.listing', {
#             'root': '/pi/pi',
#             'objects': http.request.env['pi.pi'].search([]),
#         })

#     @http.route('/pi/pi/objects/<model("pi.pi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pi.object', {
#             'object': obj
#         })

