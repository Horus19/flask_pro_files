from flask import Flask, render_template, request, redirect, url_for,flash,session, g
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
    return render_template('index.html')


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
                cur.close()
                return redirect('/Productos')

        except:
            return 'El usuario no se ha podido registrar'
    return render_template('registro.html')






@app.route('/carrito/', methods=['GET','POST'])
def Carro_compras():
    return render_template('carro.html')



@app.route('/login/', methods=['GET', 'POST'])
def login():
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
                cur.execute("call get_nombre(%s)", (id))
                usuario = cur.fetchall()
                cur.close()
                return render_template('Profile.html',usuario = usuario)
            else :
                return "contraseña incorrecta"
                cur.close()
        except:
            return 'no se pudo validar el usuario'
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
    return render_template('productos.html', productos = Productos,Tipo_producto = Tipo_productos,proveedores = Proveedores)

@app.route('/Proveedors/<Proveedor>')
def Productos_proveedor(Proveedor):
    cur = mysql.get_db().cursor()
    cur.execute('call listar_ProveedorID(%s);',(Proveedor))
    idProveedor = cur.fetchall()
    cur.execute('call listar_productos_proveedor(%s)',(idProveedor))
    Productos = cur.fetchall()
    cur.execute('call listar_tipoProducto();')
    Tipo_productos = cur.fetchall()
    cur.execute('call listar_proveedores();')
    Proveedores = cur.fetchall()
    return render_template('productos.html', productos = Productos,Tipo_producto = Tipo_productos,proveedores = Proveedores)
@app.route('/TipoProducto/<Tipo_Producto>')
def Productos_tipo(Tipo_Producto):
    cur = mysql.get_db().cursor()
    cur.execute('call listar_TipoProductoID(%s);',(Tipo_Producto))
    idTipo = cur.fetchall()
    cur.execute('call listar_productos_tipo(%s);',(idTipo))
    Productos = cur.fetchall()
    cur.execute('call listar_tipoProducto();')
    Tipo_productos = cur.fetchall()
    cur.execute('call listar_proveedores();')
    Proveedores = cur.fetchall()
    return render_template('productos.html', productos=Productos, Tipo_producto=Tipo_productos, proveedores=Proveedores)



@app.route('/Perfil')
def perfil():
    return render_template('Profile.html')



@app.errorhandler(404)
def Pagina_no_encontrada():
    return render_template('404.html'),404


if __name__ == '__main__':
    app.run()
