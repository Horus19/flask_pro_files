from flask import Flask, render_template, request, redirect, url_for,flash,session, g,jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'some_secret'


app.debug = True
app.config['MYSQL_DATABASE_HOST'] = 'b5o9m32q9rds06udvs6v-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER'] = 'upi1ralkoajjg0md'
app.config['MYSQL_DATABASE_PASSWORD'] = '4BlNb1TyEhXjngxWHXOY'
app.config['MYSQL_DATABASE_DB'] = 'b5o9m32q9rds06udvs6v'

mysql = MySQL()
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('user_id'):
        return render_template('index.html')
    else:
        return redirect('/Perfil')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        try:
            cur = mysql.get_db().cursor()
            details = request.form
            Nombre = details['nombre']
            Apellido = details['apellido']
            Contrasena = details['contrasena']
            if len(Nombre) == 0 or len(Apellido) == 0 or len(Contrasena)==0:
                return "rectificar datos"
            else:
                cur.execute(" call Registro_Cliente(%s,%s,%s);",(Nombre,Apellido,Contrasena))
                variable  = cur.fetchall();
                mysql.get_db().commit()
                cur.execute("call get_nombre(%s)", (variable))
                usuario = cur.fetchall()
                cur.close()
                return render_template('registro_Correcto.html',id = variable, usuario = usuario )

        except:
            return 'El usuario no se ha podido registrar'
    return render_template('registro.html')






@app.route('/carrito/<idProducto>/<idPedido>', methods=['GET','POST'])
def Carro_compras(idProducto,idPedido):
    if not session.get('user_id'):
        return redirect('/login')
    else:
        cur = mysql.get_db().cursor()
        cur.execute('insert into Pedido_has_Producto values (%s,%s);',(idPedido,idProducto))
        mysql.get_db().commit();
        cur.close();
        session['PedidoID']=idPedido
        return redirect('/Carro')



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if not session.get('user_id'):
        if request.method == "POST":
            try:
                session.pop('user_id', None)
                details = request.form
                id = details['usr']
                password = details['pssd']
                cur = mysql.get_db().cursor()
                cur.execute("call Validar_Usuario(%s,%s);", (id,password))
                acc = cur.fetchall()
                if str(acc) == "(('Contraseña correcta',),)":
                    session['user_id'] = id
                    cur.execute("call Crear_pedido()")
                    mysql.get_db().commit();
                    session['pedido_id'] = cur.fetchall()
                    cur.close()
                    return redirect('/Perfil')
                else :
                    return "contraseña incorrecta"
                    cur.close()
            except:
                return 'no se pudo validar el usuario'
    else:
        return redirect('/Productos')
    return render_template('login.html')


@app.route('/Productos', methods=['GET','POST'])
def Productos():
    cur = mysql.get_db().cursor()
    cur.execute('call listar_productos();')
    Productos = cur.fetchall()
    cur.execute('call listar_tipoProducto();')
    Tipo_productos = cur.fetchall()
    cur.execute('call listar_proveedores();')
    Proveedores = cur.fetchall()
    if not session.get('user_id'):
        idPedido = '0'
    else:
        idPedido = session['pedido_id']
    return render_template('productos.html', productos = Productos,Tipo_producto = Tipo_productos,proveedores = Proveedores,idPedido = idPedido)

@app.route('/Proveedors/<Proveedor>')
def Productos_proveedor(Proveedor):
    if not session.get('user_id'):
        idPedido = '0'
    else:
        idPedido = session['pedido_id']
    cur = mysql.get_db().cursor()
    cur.execute('call listar_ProveedorID(%s);',(Proveedor))
    idProveedor = cur.fetchall()
    cur.execute('call listar_productos_proveedor(%s)',(idProveedor))
    Productos = cur.fetchall()
    cur.execute('call listar_tipoProducto();')
    Tipo_productos = cur.fetchall()
    cur.execute('call listar_proveedores();')
    Proveedores = cur.fetchall()
    return render_template('productos.html', productos = Productos,Tipo_producto = Tipo_productos,proveedores = Proveedores,idPedido = idPedido)

@app.route('/TipoProducto/<Tipo_Producto>')
def Productos_tipo(Tipo_Producto):
    if not session.get('user_id'):
        idPedido = '0'
    else:
        idPedido = session['pedido_id']
    cur = mysql.get_db().cursor()
    cur.execute('call listar_TipoProductoID(%s);',(Tipo_Producto))
    idTipo = cur.fetchall()
    cur.execute('call listar_productos_tipo(%s);',(idTipo))
    Productos = cur.fetchall()
    cur.execute('call listar_tipoProducto();')
    Tipo_productos = cur.fetchall()
    cur.execute('call listar_proveedores();')
    Proveedores = cur.fetchall()
    return render_template('productos.html', productos=Productos, Tipo_producto=Tipo_productos, proveedores=Proveedores,idPedido = idPedido)

@app.route('/Carro')
def Productos_en_carro():
    if not session.get('user_id'):
        return redirect('/login')
    else:

        cur = mysql.get_db().cursor()
        cur.execute('call Productos_en_carrito(%s)',(session['PedidoID']))
        Productos = cur.fetchall();
        cur.execute('call valor_total(%s)',(session['PedidoID']))
        valor = cur.fetchall();
        cur.close()
        return render_template('shopping-cart.html',productos=Productos, valor = valor )




@app.route('/Perfil')
def perfil():
    if not session.get('user_id'):
        return redirect('/login/')
    else:
        cur = mysql.get_db().cursor()
        cur.execute('call get_nombre(%s)',(session['user_id']))
        nombre = cur.fetchall()
        cur.close()
        return render_template('Profile.html',usuario = nombre, idPedido = session['pedido_id'] )


@app.route('/Cambiar_Contrasena', methods=['GET','POST'])
def cambiar_contrasena():
    if session.get('user_id'):
        if request.method == "POST":
            details = request.form
            nueva_contrasena = details['pssd']
            cur = mysql.get_db().cursor()
            id = session['user_id']
            cur.execute('call cambiar_contrasena(%s,%s);',(id,nueva_contrasena))
            mysql.get_db().commit()
            cur.close()
            session.pop('user_id',None)
            return redirect('/login/')
        return render_template('cambiar_contrasena.html')
    else:
        return redirect('/')

@app.route('/Exit')
def salida():
    session.pop('user_id')
    session.pop('PedidoID')
    session.pop('pedido_id')
    return redirect('/')




if __name__ == '__main__':
    app.run()
