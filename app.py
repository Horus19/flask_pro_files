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
        try:
            cur = mysql.get_db().cursor()
            details = request.form
            Nombre = details['nombre']
            Apellido = details['apellido']
            Contrasena = details['contrasena']
            if len(Nombre) == 0 or len(Apellido) == 0 or len(Contrasena)==0:
                return "Asegurese de que ha ingresado los datos correctamente"
            else:
                cur.execute(" call Registro_Cliente(%s,%s,%s);",(Nombre,Apellido,Contrasena))
                variable  = cur.fetchall();
                mysql.get_db().commit()
                cur.close()
                return 'el id de registro fue' + str(variable)
        except:
            return 'El usuario no se ha podido registrar'
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
        try:
            details = request.form
            id = details['usr']
            password = details['pssd']
            cur = mysql.get_db().cursor()
            cur.execute("call Validar_Usuario(%s,%s);", (id,password))
            acc = cur.fetchall()
            cur.close()
            return str(acc)
        except:
            return 'no se pudo validar el usuario'
    return render_template('login.html')




@app.route('/usuarios')
def usuarios():
    return render_template()

if __name__ == '__main__':
    app.run()
