from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

# MODELO PLATOS SERGIO ****************

class PlatosSergio(models.Model):
    _name = 'restaurante_sergio.platos_sergio'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre del plato",
        required=True
    )

    description = fields.Text(
        string="Descripción"
    )

    precio = fields.Float(
        string="Precio",
        help="Precio del plato en euros"
    )

    codigo = fields.Char(
        string="Código del plato",
        compute="_get_codigo"
    )

    precio_con_iva = fields.Float(
        string="Precio con IVA",
        compute="_compute_precio_con_iva"
    )

    descuento = fields.Float(
        string="Descuento (%)"
    )

    precio_final = fields.Float(
        string="Precio final",
        compute="_compute_precio_final",
        store=True
    )

    tiempo_preparacion = fields.Integer(
        string="Tiempo de preparación (minutos)",
        required=True
    )

    disponible = fields.Boolean(
        string="Disponible",
        default=True
    )

    categoria = fields.Selection(
        [('entrante', 'Entrante'),
         ('principal', 'Principal'),
         ('postre', 'Postre'),
         ('bebida', 'Bebida')],
        string="Categoría"
    )

    menu_id = fields.Many2one(
        'restaurante_sergio.menu_sergio',
        string='Menú relacionado',
        ondelete='set null'
    )

    rel_ingredientes = fields.Many2many(
        'restaurante_sergio.ingredientes_sergio',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes'
    )


    #METODOS ****************
    def _get_codigo(self):
        for plato in self:
            try:
                if not plato.categoria:
                    _logger.warning(f"El plato {plato.name} no tiene categoría asignada.")
                    plato.codigo = f"PLT_{plato.id}"
                else:
                    plato.codigo = f"{plato.categoria[:3].upper()}_{plato.id}"
                    _logger.debug(f"Código asignado: {plato.codigo}")
            except Exception as e:
                raise ValidationError(f"Error al generar el código del plato: {str(e)}")


    def _compute_precio_con_iva(self):
        for plato in self:
            plato.precio_con_iva = plato.precio * 1.10 if plato.precio else 0.0
            
    
    
    #CONSTRAINTS ****************
    @api.constrains('tiempo_preparacion')
    def _check_tiempo_preparacion(self):
        for plato in self:
            if plato.tiempo_preparacion:
                if plato.tiempo_preparacion < 1 or plato.tiempo_preparacion > 240:
                 raise ValidationError("El tiempo de preparación no puede ser mayor a 4 Horas.")
             
    @api.constrains('precio')
    def _check_precio_positivo(self):
        for plato in self:
            if plato.precio <= 0:
                raise ValidationError("El precio del plato no puede ser negativo.")
            else:
                _logger.debug(f"Precio del plato {plato.name} es correcto: {plato.precio} euros.")

    #DEPENDS ****************
    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if plato.precio:
                descuento = plato.descuento or 0.0
                plato.precio_final = plato.precio * (1 - descuento / 100)
            else:
                plato.precio_final = 0.0



#MODELO MENÚS SERGIO ****************
class Menu(models.Model):
    _name = 'restaurante_sergio.menu_sergio'
    _description = 'Modelo de Menús para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    fecha_ini = fields.Datetime(
        string="Fecha Inicio",
        required=True
    )

    fecha_fin = fields.Datetime(
        string="Fecha Final"
    )

    activo = fields.Boolean(
        string="Activo",
        default=True
    )

    platos = fields.One2many(
        'restaurante_sergio.platos_sergio',
        'menu_id',
        string='Platos del Menú'
    )

    precio_total = fields.Float(
        string="Precio total",
        compute="_compute_precio_total",
        store=True
    )

#CONSTRAINS ****************
    @api.constrains('fecha_ini', 'fecha_fin')
    def _check_fechas_menu(self):
        for menu in self:
            if menu.fecha_fin:
                if menu.fecha_fin < menu.fecha_ini:
                    raise ValidationError("La fecha final no puede ser anterior a la fecha de inicio.")
                
    @api.constrains('platos', 'activo')
    def _check_platos_activo(self):
        for menu in self:
            if menu.activo and not menu.platos:
                raise ValidationError("Un menú activo debe tener al menos un plato asociado.")



#DEPENDS ****************
    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            menu.precio_total = sum(menu.platos.mapped('precio_final'))




class IngredientesSergio(models.Model):
    _name = 'restaurante_sergio.ingredientes_sergio'
    _description = 'Modelo de Ingredientes para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre",
        required=True
    )

    es_alergeno = fields.Boolean(
        string="Es alérgeno",
        default=False
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    rel_platos = fields.Many2many(
        'restaurante_sergio.platos_sergio',
        relation='relacion_platos_ingredientes',
        column1='rel_ingredientes',
        column2='rel_platos',
        string='Platos'
    )
