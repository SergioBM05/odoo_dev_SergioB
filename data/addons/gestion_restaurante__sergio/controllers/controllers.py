# from odoo import http


# class GestionRestauranteSergio(http.Controller):
#     @http.route('/gestion_restaurante__sergio/gestion_restaurante__sergio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante__sergio/gestion_restaurante__sergio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante__sergio.listing', {
#             'root': '/gestion_restaurante__sergio/gestion_restaurante__sergio',
#             'objects': http.request.env['gestion_restaurante__sergio.gestion_restaurante__sergio'].search([]),
#         })

#     @http.route('/gestion_restaurante__sergio/gestion_restaurante__sergio/objects/<model("gestion_restaurante__sergio.gestion_restaurante__sergio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante__sergio.object', {
#             'object': obj
#         })

