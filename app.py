from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configuración de la conexión a MySQL
def conectar():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='', # Tu contraseña
        db='usuarios',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# RUTA: Listar registros (Equivalente a index.php)
@app.route('/')
def index():
    db = conectar()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
    finally:
        db.close()
    return render_template('index.html', usuarios=usuarios)

# RUTA: Crear registro (Equivalente a create.php)
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        
        db = conectar()
        try:
            with db.cursor() as cursor:
                cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
            db.commit()
        finally:
            db.close()
        return redirect(url_for('index'))
    
    return render_template('formulario.html', titulo="Agregar Usuario", usuario=None)

# RUTA: Editar (Equivalente a update.php)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = conectar()
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        try:
            with db.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET nombre=%s, email=%s WHERE id=%s", (nombre, email, id))
            db.commit()
        finally:
            db.close()
        return redirect(url_for('index'))
    
    # Si es GET, buscamos los datos del usuario para el formulario
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cursor.fetchone()
    db.close()
    return render_template('formulario.html', titulo="Editar Usuario", usuario=usuario)

# RUTA: Eliminar (Equivalente a delete.php)
@app.route('/delete/<int:id>')
def delete(id):
    db = conectar()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        db.commit()
    finally:
        db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)