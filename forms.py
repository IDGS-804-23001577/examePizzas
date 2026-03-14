from flask_wtf import FlaskForm
from wtforms import StringField, DateField, RadioField, SelectMultipleField, IntegerField, widgets
from wtforms.validators import DataRequired, Length, NumberRange



class PedidoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio")
    ])
    direccion = StringField('Direccion', validators=[
        DataRequired(message="La direccion es obligatoria")
    ])
    telefono = StringField('Telefono', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Length(min=10, max=10, message="El teléfono debe tener 10 dígitos")
    ])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[
        DataRequired(message="Selecciona una fecha valida")
    ])
    


    tamano = RadioField('Tamaño Pizza', choices=[('Chica', 'Chica $40'), ('Mediana', 'Mediana $80'), ('Grande', 'Grande $120')], default='Chica')
    ingredientes = SelectMultipleField('Ingredientes', 
        choices=[('Jamon', 'Jamón $10'), ('Pina', 'Piña $10'), ('Champinones', 'Champiñones $10')],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    


    num_pizzas = IntegerField('Num. de Pizzas', default=1, validators=[
        DataRequired(message="Ingresa una cantidad"),
        NumberRange(min=1, message="Debe ser al menos 1 pizza")
    ])