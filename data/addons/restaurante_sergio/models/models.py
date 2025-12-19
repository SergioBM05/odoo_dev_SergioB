from odoo import models, fields, api


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



    def _get_codigo(self):
        for plato in self:
            if plato.categoria:
                plato.codigo = f"{plato.categoria[:3].upper()}_{plato.id}"
            else:
                plato.codigo = f"PLT_{plato.id}"

    def _compute_precio_con_iva(self):
        for plato in self:
            plato.precio_con_iva = plato.precio * 1.10 if plato.precio else 0.0

    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if plato.precio:
                descuento = plato.descuento or 0.0
                plato.precio_final = plato.precio * (1 - descuento / 100)
            else:
                plato.precio_final = 0.0




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
