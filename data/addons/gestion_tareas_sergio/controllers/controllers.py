# from odoo import http


# class GestionTareasSergio(http.Controller):
#     @http.route('/gestion_tareas_sergio/gestion_tareas_sergio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_sergio/gestion_tareas_sergio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_sergio.listing', {
#             'root': '/gestion_tareas_sergio/gestion_tareas_sergio',
#             'objects': http.request.env['gestion_tareas_sergio.gestion_tareas_sergio'].search([]),
#         })

#     @http.route('/gestion_tareas_sergio/gestion_tareas_sergio/objects/<model("gestion_tareas_sergio.gestion_tareas_sergio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_sergio.object', {
#             'object': obj
#         })

