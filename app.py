from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'admin',
    'password': 'Test123!',
    'host': 'localhost',
    'database': 'iglesia'
}

grupos_pastorales = [
    "Divino Salvador del Mundo", "Consejo de María", "Unción del Espírituo Santo",
    "Siervo de Siervos", "Ministros Extraordinarios de la Comunión", "El Señor es mi Pastor",
    "Peregrinos del Señor", "Familias para Jesús", "Mensajeros de Jesús", "Pastoral de la Palabra",
    "Lectores", "Grupo Juvenil Exodo", "Grupo Juvenil Corriente de Gracia", "Grupo Juvenil Ascesis",
    "Coros", "Monaguillos", "Pastoral Social", "Pastoral de la Salud", "Pastoral de Catequesis",
    "Primera Comunión", "Confirmación", "Seguimiento", "Bautizos", "Emaús", 
    "Pastoral de Medios de Comunicación", "Asunción de María Juvenil RCC", "Asunción de María RCC",
    "Comité de Construcción", "Misioneros de Jesús RCC", "Misioneros Eucarísticos",
    "Pastoral de Enfermos", "Pastoral de la Primera Infancia", "Grupo Pro-Festejos",
    "Catequesis Pre-Matrimoniales", "Jóvenes al pie de la Cruz", "Desayuno Evangelizador",
    "Adoradoras Eucarísticas", "Asamblea Familiar Santa Clara de Asís", 
    "Comité Católico Santa Clara de Asís", "Asociación comunitaria católica y social SAC"
]

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    search = request.args.get('search')
    if search:
        query = f"""SELECT * FROM miembros WHERE 
                    nombre LIKE %s OR 
                    celular LIKE %s OR 
                    direccion LIKE %s OR 
                    profesion LIKE %s OR 
                    habilidades LIKE %s"""
        like = f"%{search}%"
        cursor.execute(query, (like, like, like, like, like))
    else:
        cursor.execute("SELECT * FROM miembros")
    miembros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", miembros=miembros, search=search)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        datos = request.form
        grupos = ', '.join(request.form.getlist('grupo'))
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO miembros (nombre, fecha_nacimiento, celular, direccion, profesion, habilidades, sector, grupo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datos['nombre'], datos['fecha'], datos['celular'], datos['direccion'], datos['profesion'],
            datos['habilidades'], datos['sector'], grupos
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("form.html", grupos=grupos_pastorales)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM miembros WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# (pendiente: ruta para editar si lo deseas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
