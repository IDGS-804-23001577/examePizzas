from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from models import db, Cliente, Pizza, Pedido, DetallePedido, PizzaTemp
import forms
from config import DevelopmentConfig
import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
db.init_app(app)

with app.app_context():
    db.create_all()

PRECIOS_TAMANO = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
PRECIO_INGREDIENTE = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.PedidoForm(request.form)
    
    
    carrito_temp = PizzaTemp.query.all()
    
    if request.method == 'POST':
        
        

        if 'agregar' in request.form:
            
            if form.validate(): 
                tamano = form.tamano.data
                ingredientes = form.ingredientes.data
                cantidad = form.num_pizzas.data
                
                precio_base = PRECIOS_TAMANO.get(tamano, 40)
                precio_extras = len(ingredientes) * PRECIO_INGREDIENTE
                precio_unitario = precio_base + precio_extras
                subtotal = precio_unitario * cantidad
                
                nueva_pizza_temp = PizzaTemp(
                    tamano=tamano,
                    ingredientes=', '.join(ingredientes) if ingredientes else 'Queso',
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                db.session.add(nueva_pizza_temp)
                db.session.commit()
            
            
        
        elif 'quitar' in request.form:
            id_borrar = request.form.get('quitar')
            pizza_a_borrar = PizzaTemp.query.get(id_borrar)
            if pizza_a_borrar:
                db.session.delete(pizza_a_borrar)
                db.session.commit()
            

        
        elif 'terminar' in request.form:
            
            carrito_temp = PizzaTemp.query.all()
            
            if not carrito_temp:
                flash("No hay pizzas agregadas al pedido.", "danger")
                
            
            elif form.validate(): 
                total_pedido = sum(p.subtotal for p in carrito_temp)
                
                
                nuevo_cliente = Cliente(
                    nombre=form.nombre.data,
                    direccion=form.direccion.data,
                    telefono=form.telefono.data
                )
                db.session.add(nuevo_cliente)
                db.session.commit()
                
                
                nuevo_pedido = Pedido(
                    id_cliente=nuevo_cliente.id_cliente,
                    fecha=form.fecha.data,
                    total=total_pedido
                )
                db.session.add(nuevo_pedido)
                db.session.commit()
                
                
                for p_temp in carrito_temp:
                    nueva_pizza = Pizza(
                        tamano=p_temp.tamano,
                        ingredientes=p_temp.ingredientes,
                        precio=p_temp.precio_unitario
                    )
                    db.session.add(nueva_pizza)
                    db.session.commit() 
                    
                    nuevo_detalle = DetallePedido(
                        id_pedido=nuevo_pedido.id_pedido,
                        id_pizza=nueva_pizza.id_pizza,
                        cantidad=p_temp.cantidad,
                        subtotal=p_temp.subtotal
                    )
                    db.session.add(nuevo_detalle)
                    
                    
                    db.session.delete(p_temp)
                
                db.session.commit()
                flash(f"Pedido guardado, importe total a pagar: ${total_pedido}", "success")
                return redirect(url_for('index'))

    
    carrito_temp = PizzaTemp.query.all()
    hoy = datetime.date.today()
    ventas_hoy = Pedido.query.filter_by(fecha=hoy).all()
    total_hoy = sum(v.total for v in ventas_hoy)
    total_actual = sum(p.subtotal for p in carrito_temp)
    
    return render_template('index.html', form=form, carrito=carrito_temp, total_actual=total_actual, ventas_hoy=ventas_hoy, total_hoy=total_hoy)




@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    pedidos_filtrados = []
    total_acumulado = 0
    tipo_busqueda = None
    
    if request.method == 'POST':
        tipo_busqueda = request.form.get('tipo_busqueda') 
        
        
        if tipo_busqueda == 'dia':
            termino_numero = int(request.form.get('termino_dia'))
        else:
            termino_numero = int(request.form.get('termino_mes'))
            
        todos_pedidos = Pedido.query.all()
        
        
        for p in todos_pedidos:
            if not p.fecha: continue
            
            if tipo_busqueda == 'dia':
                
                if p.fecha.weekday() == termino_numero:
                    pedidos_filtrados.append(p)
                    total_acumulado += p.total
                    
            elif tipo_busqueda == 'mes':
                
                if p.fecha.month == termino_numero:
                    pedidos_filtrados.append(p)
                    total_acumulado += p.total

    return render_template('ventas.html', pedidos=pedidos_filtrados, total=total_acumulado, tipo=tipo_busqueda)

@app.route('/detalle/<int:id_pedido>')
def detalle(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)
    return render_template('detalle.html', pedido=pedido)

if __name__ == '__main__':
    app.run(port=5000)