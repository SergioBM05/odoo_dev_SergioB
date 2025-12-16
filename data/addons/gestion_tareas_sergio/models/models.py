from odoo import models, fields, api

class tareas_sergio(models.Model):
    _name = 'gestion_tareas_sergio.tareas_sergio'
    _description = 'Modelo de Tareas para Gestión de Proyectos'

    nombre = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")

    fecha_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")

    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")

    finalizado = fields.Boolean(
        string="Finalizado", 
        help="Indica si la tarea ha sido finalizada o no")
    
    sprint = fields.Many2one(
    'gestion_tareas_sergio.sprints_sergio', 
    string='Sprint relacionado', 
    ondelete='set null', 
    help='Sprint al que pertenece esta tarea')
    
    rel_tecnologias = fields.Many2many(
    comodel_name='gestion_tareas_sergio.tecnologias_sergio',
    relation='relacion_tareas_tecnologias',
    column1='rel_tareas',
    column2='rel_tecnologias',
    string='Tecnologías')
    
class sprints_sergio(models.Model):
    _name = 'gestion_tareas_sergio.sprints_sergio'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(
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
    
    tareas = fields.One2many(
    'gestion_tareas_sergio.tareas_sergio', 
    'sprint', 
    string='Tareas del Sprint')
    
class tecnologias_sergio(models.Model):
    _name = 'gestion_tareas_sergio.tecnologias_sergio'
    _description = 'Modelo de Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología")
    
    rel_tareas = fields.Many2many(
    comodel_name='gestion_tareas_sergio.tareas_sergio',
    relation='relacion_tareas_tecnologias',
    column1='rel_tecnologias',
    column2='rel_tareas',
    string='Tareas')