from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)



app.debug = True
app.config['MYSQL_DATABASE_HOST'] = 'b5o9m32q9rds06udvs6v-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER'] = 'upi1ralkoajjg0md'
app.config['MYSQL_DATABASE_PASSWORD'] = '4BlNb1TyEhXjngxWHXOY'
app.config['MYSQL_DATABASE_DB'] = 'b5o9m32q9rds06udvs6v'

mysql = MySQL()
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.get_db().commit()
        cur.close()
        return 'success'
    return render_template('index.html')



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        details = request.form
        Nombre = details['nombre']
        Apellido = details['apellido']
        Usuario = details['usuario']
        Contrasena = details['contrasena']
        cur = mysql.get_db().cursor()
        cur.execute("insert into MyUsers (firstname,lastname,password,usuario) values (%s,%s,%s,%s)", (Nombre,Apellido,Contrasena,Usuario))
        mysql.get_db().commit()
        cur.close()
        return 'ok'
    return render_template('registro.html')





@app.route('/Productos', methods=['GET','POST'])
def entrar():

    return render_template('productos.html')

@app.route('/carrito/', methods=['GET','POST'])
def Carro_compras():
    return render_template('carro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        usuario = details['usr']
        password = details['pssd']
        cur = mysql.get_db().cursor()
        cur.execute("select password from MyUsers where firstname = %s and password ='1234'", (usuario))
        passd = cur.fetchall()
        cur.close()
        return 'ok'
    return render_template('login.html')




@app.route('/usuarios')
def usuarios():
    return render_template()

if __name__ == '__main__':
    app.run()
