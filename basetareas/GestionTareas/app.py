from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import mysql.connector

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://DavidToledo:Nathanael@localhost/Biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'tu_clave_secreta' 

db = SQLAlchemy(app)  

class Estudiante(db.Model):
    __tablename__ = 'Estudiante'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)

    def __repr__(self):
        return f'<Estudiante {self.nombre} {self.apellido}>'

class Usuario(db.Model):
    __tablename__ = 'Usuario' 
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False) 
    id_rol = db.Column(db.Integer, db.ForeignKey('Rol.id_rol'))
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))  # Relación con la tabla Rol

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Rol(db.Model):
    __tablename__ = 'Rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))

    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Curso(db.Model):
    __tablename__ = 'Curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    creditos = db.Column(db.Integer)
    semestre = db.Column(db.Integer)

    def __repr__(self):
        return f'<Curso {self.nombre_curso}>'

class Profesor(db.Model):
    __tablename__ = 'Profesor'
    id_profesor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

    def __repr__(self):
        return f'<Profesor {self.nombre} {self.apellido}>'

class Tarea(db.Model):
    __tablename__ = 'Tarea'
    id_tarea = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    fecha_asignacion = db.Column(db.Date)
    fecha_entrega = db.Column(db.Date)
    estado = db.Column(db.String(20))
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'))
    curso = db.relationship('Curso', backref=db.backref('tareas', lazy=True))

    def __repr__(self):
        return f'<Tarea {self.titulo}>'

class Inscripcion(db.Model):
    __tablename__ = 'Inscripcion'
    id_inscripcion = db.Column(db.Integer, primary_key=True)
    fecha_inscripcion = db.Column(db.Date)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'))
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'))
    estudiante = db.relationship('Estudiante', backref=db.backref('inscripciones', lazy=True))
    curso = db.relationship('Curso', backref=db.backref('inscripciones', lazy=True))
    calificacion = db.Column(db.Float)

    def __repr__(self):
        return f'<Inscripcion {self.id_inscripcion}>'

class Comentario(db.Model):
    __tablename__ = 'Comentario'
    id_comentario = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime)
    id_tarea = db.Column(db.Integer, db.ForeignKey('Tarea.id_tarea'))
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'))
    tarea = db.relationship('Tarea', backref=db.backref('comentarios', lazy=True))
    estudiante = db.relationship('Estudiante', backref=db.backref('comentarios', lazy=True))

    def __repr__(self):
        return f'<Comentario {self.id_comentario}>'

class Recurso(db.Model):
    __tablename__ = 'Recurso'
    id_recurso = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    url = db.Column(db.String(200))
    descripcion = db.Column(db.String(200))
    id_tarea = db.Column(db.Integer, db.ForeignKey('Tarea.id_tarea'))
    tarea = db.relationship('Tarea', backref=db.backref('recursos', lazy=True))

    def __repr__(self):
        return f'<Recurso {self.id_recurso}>'

class Horario(db.Model):
    __tablename__ = 'Horario'
    id_horario = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    dia = db.Column(db.String(20))
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'))
    curso = db.relationship('Curso', backref=db.backref('horarios', lazy=True))

    def __repr__(self):
        return f'<Horario {self.id_horario}>'

class Notificacion(db.Model):
    __tablename__ = 'Notificacion'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_envio = db.Column(db.DateTime)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'))
    estudiante = db.relationship('Estudiante', backref=db.backref('notificaciones', lazy=True))

    def __repr__(self):
        return f'<Notificacion {self.id_notificacion}>'

class CursoProfesor(db.Model):
    __tablename__ = 'Curso_Profesor'
    id_curso_profesor = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'))
    id_profesor = db.Column(db.Integer, db.ForeignKey('Profesor.id_profesor'))
    curso = db.relationship('Curso', backref=db.backref('curso_profesores', lazy=True))
    profesor = db.relationship('Profesor', backref=db.backref('curso_profesores', lazy=True))

    def __repr__(self):
        return f'<CursoProfesor {self.id_curso_profesor}>'

# Rutas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estudiantes")
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template("estudiantes/lista_estudiantes.html", estudiantes=estudiantes)

@app.route("/estudiantes/crear", methods=["GET", "POST"])
def crear_estudiante():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        nuevo_estudiante = Estudiante(nombre=nombre, apellido=apellido, correo=correo, telefono=telefono, fecha_nacimiento=fecha_nacimiento)
        db.session.add(nuevo_estudiante)
        db.session.commit()
        return redirect(url_for("listar_estudiantes"))
    return render_template("estudiantes/crear_estudiante.html")

# Rutas para Usuarios, Cursos, etc. (adaptadas a los modelos SQLAlchemy)

# Ejemplo de consulta con SQLAlchemy
@app.route("/cursos")
def listar_cursos():
    cursos = Curso.query.all()
    return render_template("cursos/lista_cursos.html", cursos=cursos)

# Resto de las rutas (adaptadas a los modelos SQLAlchemy)
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)

@app.route("/usuarios/crear", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Considera usar hashing
        id_rol = request.form["id_rol"]

        nuevo_usuario = Usuario(username=username, password=password, id_rol=id_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    roles = Rol.query.all()
    return render_template("usuarios/crear_usuario.html", roles=roles)

@app.route("/usuarios/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        usuario.username = request.form["username"]
        usuario.password = request.form["password"]  # Considera usar hashing
        usuario.id_rol = request.form["id_rol"]
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    roles = Rol.query.all()
    return render_template("usuarios/editar_usuario.html", usuario=usuario, roles=roles)

@app.route("/usuarios/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("listar_usuarios"))

# Inicio de la aplicación
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)