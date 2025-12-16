# from odoo import http


# class RestauranteSergio(http.Controller):
#     @http.route('/restaurante_sergio/restaurante_sergio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restaurante_sergio/restaurante_sergio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restaurante_sergio.listing', {
#             'root': '/restaurante_sergio/restaurante_sergio',
#             'objects': http.request.env['restaurante_sergio.restaurante_sergio'].search([]),
#         })

#     @http.route('/restaurante_sergio/restaurante_sergio/objects/<model("restaurante_sergio.restaurante_sergio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restaurante_sergio.object', {
#             'object': obj
#         })

