from odoo import models, fields, api

class PlatosSergio(models.Model):
    _name = 'restaurante_sergio.platos_sergio'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre del plato",
        required=True,
        help="Introduzca el nombre del plato"
        )
    
    description = fields.Text(
        string="Descripción",
        help="Descripción del plato"
        )
    
    precio = fields.Float(
        string="Precio",
        required=True,
        help="Precio del plato en euros"
        )
    
    
    tiempo_preparacion = fields.Integer(
        string="Tiempo de preparación (minutos)", 
        required=True,
        help="Tiempo estimado de preparación del plato en minutos"
        )
    
    disponible = fields.Boolean(
        string="Disponible",
        default=True,
        help="Indica si el plato está disponible en el menú"
        )
    
    categoria = fields.Selection(
        [('entrante', 'Entrante'),
         ('principal', 'Principal'),
         ('postre', 'Postre'),
         ('bebida', 'Bebida')],
        string="Categoría",
        required=True
    )
    
    menu_id = fields.Many2one(
    'restaurante_sergio.menu_sergio', 
    string='Menú relacionado', 
    ondelete='set null', 
    help='Menú al que pertenece este plato')
    
    rel_ingredientes = fields.Many2many(
    comodel_name='restaurante_sergio.ingredientes_sergio',
    relation='relacion_platos_ingredientes',
    column1='rel_platos',
    column2='rel_ingredientes',
    string='Ingredientes')
    
class Menu(models.Model):
    _name = 'restaurante_sergio.menu_sergio'
    _description = 'Modelo de Menús para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del menú")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del menú")
    
    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del menú")
    
    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización del sprint")
    
    activo = fields.Boolean(
        string="Activo",
        default=True,
        help="Indica si el menú está activo"
    )
    
    platos = fields.One2many(
    'restaurante_sergio.platos_sergio', 
    'menu_id', 
    string='Platos del Menú')
    
    
class IngredientesSergio(models.Model):
    
    _name = 'restaurante_sergio.ingredientes_sergio'
    _description = 'Modelo de Ingredientes para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del ingrediente")
    
    es_alergeno = fields.Boolean(
        string="Es alérgeno",
        default=False,
        help="Indica si el ingrediente es un alérgeno"
    )
    
    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del ingrediente")
    
    rel_platos = fields.Many2many(
    comodel_name='restaurante_sergio.platos_sergio',
    relation='relacion_platos_ingredientes',
    column1='rel_ingredientes',
    column2='rel_platos',
    string='Platos')
    
    
