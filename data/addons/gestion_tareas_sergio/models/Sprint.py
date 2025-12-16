from odoo import models, fields, api

class sprints_sergio(models.Model):
    _name = 'gestion_tareas_sergio.sprints_sergio'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    nombre = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del sprint")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del sprint")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del sprint")

    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización del sprint")