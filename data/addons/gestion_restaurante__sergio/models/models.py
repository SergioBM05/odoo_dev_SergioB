from odoo import models, fields, api

class PlatosSergio(models.Model):
    _name = 'gestion_restaurante__sergio.platos_sergio'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    name = fields.Char(string="Nombre del plato", required=True)
    description = fields.Text(string="Descripción")
