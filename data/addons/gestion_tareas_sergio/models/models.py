from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError #type:ignore
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


#PROYECTO *****************************
class proyectos_sergio(models.Model):
    _name = 'gestion_tareas_sergio.proyectos_sergio'
    _description = 'Modelo de Tareas para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre del proyecto")

    descripcion = fields.Text(
        string="Descripción", 
        help="Descripción del proyecto")

    historias = fields.One2many(
        'gestion_tareas_sergio.historias_sergio', 
        'proyecto', 
        string='Historias de Usuario')
    
    sprints = fields.One2many(
        'gestion_tareas_sergio.sprints_sergio', 
        'proyecto', 
        string='Sprints de Usuario')


#HISTORIAS DE USUARIOS*******************************
class historias_sergio(models.Model):
    _name = 'gestion_tareas_sergio.historias_sergio'
    _description = 'Modelo de Tareas para Gestión de Proyectos'
    
    
    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la historia")

    descripcion = fields.Text(
        string="Descripción", 
        help="Descripción de la historia")

    proyecto = fields.Many2one(
        'gestion_tareas_sergio.proyectos_sergio', 
        string='Proyecto',
        ondelete = 'set null',
        help='Proyecto al que pertenece el proyecto')

    tareas = fields.One2many(
        'gestion_tareas_sergio.tareas_sergio', 
        'historia', 
        string='Tareas de la Historia')



#TAREAS*******************************
class tareas_sergio(models.Model):
    _name = 'gestion_tareas_sergio.tareas_sergio'
    _description = 'Modelo de Tareas para Gestión de Proyectos'
    
    # En el modelo tareas_sergio
    codigo = fields.Char(compute="_get_codigo")

    name = fields.Char(
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
        string='Sprint Activo', 
        compute='_compute_sprint', 
        store=True) 
    
    rel_tecnologias = fields.Many2many(
    comodel_name='gestion_tareas_sergio.tecnologias_sergio',
    relation='relacion_tareas_tecnologias',
    column1='rel_tareas',
    column2='rel_tecnologias',
    string='Tecnologías')
    
    historia = fields.Many2one(
        'gestion_tareas_sergio.historias_sergio', 
        string='Historia de Usuario',
        ondelete='set null',
        help='Historias de usuario de la tarea')
    
    
    @api.depends('historia', 'historia.proyecto')
    def _compute_sprint(self):
        for tarea in self:
            tarea.sprint = False

            # Verificar que la tarea tiene historia y proyecto
            if tarea.historia and tarea.historia.proyecto:
                # Buscar sprints del proyecto
                sprints = self.env['gestion_tareas_sergio.sprints_sergio'].search([
                    ('proyecto.id', '=', tarea.historia.proyecto.id)
                ])

                # Buscar el sprint activo (fecha_fin > ahora) 
                # de entre todos los sprints asociados al proyecto
                # en teoría solo hay un sprint activo, por eso es el que no ha vencido
                for sprint in sprints:
                    if (isinstance(sprint.fecha_fin, datetime) and 
                            sprint.fecha_ini <= datetime.now() and   
                            sprint.fecha_fin > datetime.now()):
                        tarea.sprint = sprint.id
                        break
    
    @api.depends('sprint', 'sprint.name')
    def _get_codigo(self):
        _logger.info("Iniciando generación de códigos de tareas")

        for tarea in self:
            try:
                if not tarea.sprint:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                    tarea.codigo = "TSK_" + str(tarea.id)

                else:
                    # Si tiene sprint, usamos su nombre
                    tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)

                _logger.debug(f"Código generado: {tarea.codigo}")

            except Exception as e:
                _logger.error(f"Error generando código para tarea {tarea.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")
            
    
#SPINTS*******************************        
class sprints_sergio(models.Model):
    _name = 'gestion_tareas_sergio.sprints_sergio'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")
    fecha_ini = fields.Datetime(string="Fecha Inicio", required=True)
    duracion = fields.Integer(
        string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")
    
    tareas = fields.One2many(
        'gestion_tareas_sergio.tareas_sergio', 
        'sprint', 
        string='Tareas de la Historia')
    
    proyecto = fields.Many2one(
        'gestion_tareas_sergio.proyectos_sergio', 
        string="Proyecto",
        ondelete='set null')

    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
            else:
                sprint.fecha_fin = sprint.fecha_ini
                
                
                
                
#TECNOLOGIAS*******************************              
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