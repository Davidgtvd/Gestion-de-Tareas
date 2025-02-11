from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets
import mysql.connector
from sqlalchemy import create_engine
from datetime import datetime
import bcrypt

app = Flask(__name__)

db_user = 'david'
db_password = 'D@v1d2024!'
db_host = 'localhost'
db_name = 'Biblioteca'
db_uri = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)

class Estudiante(db.Model):
    __tablename__ = 'Estudiante'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    inscripciones = db.relationship('Inscripcion', backref='estudiante', lazy=True)
    comentarios = db.relationship('Comentario', backref='estudiante', lazy=True)
    notificaciones = db.relationship('Notificacion', backref='estudiante', lazy=True)

    def __repr__(self):
        return f'<Estudiante {self.nombre} {self.apellido}>'

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('Rol.id_rol'))
    rol = db.relationship('Rol', backref='usuarios', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Rol(db.Model):
    __tablename__ = 'Rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Curso(db.Model):
    __tablename__ = 'Curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    creditos = db.Column(db.Integer)
    semestre = db.Column(db.Integer)
    tareas = db.relationship('Tarea', backref='curso', lazy=True)
    inscripciones = db.relationship('Inscripcion', backref='curso', lazy=True)
    horarios = db.relationship('Horario', backref='curso', lazy=True)
    curso_profesores = db.relationship('CursoProfesor', backref='curso', lazy=True)

    def __repr__(self):
        return f'<Curso {self.nombre_curso}>'

class Profesor(db.Model):
    __tablename__ = 'Profesor'
    id_profesor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    curso_profesores = db.relationship('CursoProfesor', backref='profesor', lazy=True)

    def __repr__(self):
        return f'<Profesor {self.nombre} {self.apellido}>'

class Tarea(db.Model):
    __tablename__ = 'Tarea'
    id_tarea = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    fecha_asignacion = db.Column(db.Date, default=datetime.utcnow)
    fecha_entrega = db.Column(db.Date)
    estado = db.Column(db.String(20), default='Pendiente')
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'), nullable=False)
    comentarios = db.relationship('Comentario', backref='tarea', lazy=True)
    recursos = db.relationship('Recurso', backref='tarea', lazy=True)

    def __repr__(self):
        return f'<Tarea {self.titulo}>'

class Inscripcion(db.Model):
    __tablename__ = 'Inscripcion'
    id_inscripcion = db.Column(db.Integer, primary_key=True)
    fecha_inscripcion = db.Column(db.Date, default=datetime.utcnow)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'), nullable=False)
    calificacion = db.Column(db.Float)

    def __repr__(self):
        return f'<Inscripcion {self.id_inscripcion}>'

class Comentario(db.Model):
    __tablename__ = 'Comentario'
    id_comentario = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    id_tarea = db.Column(db.Integer, db.ForeignKey('Tarea.id_tarea'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'), nullable=False)

    def __repr__(self):
        return f'<Comentario {self.id_comentario}>'

class Recurso(db.Model):
    __tablename__ = 'Recurso'
    id_recurso = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    url = db.Column(db.String(200))
    descripcion = db.Column(db.String(200))
    id_tarea = db.Column(db.Integer, db.ForeignKey('Tarea.id_tarea'), nullable=False)

    def __repr__(self):
        return f'<Recurso {self.id_recurso}>'

class Horario(db.Model):
    __tablename__ = 'Horario'
    id_horario = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    dia = db.Column(db.String(20))
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'), nullable=False)

    def __repr__(self):
        return f'<Horario {self.id_horario}>'

class Notificacion(db.Model):
    __tablename__ = 'Notificacion'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id_estudiante'), nullable=False)

    def __repr__(self):
        return f'<Notificacion {self.id_notificacion}>'

class CursoProfesor(db.Model):
    __tablename__ = 'Curso_Profesor'
    id_curso_profesor = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso'), nullable=False)
    id_profesor = db.Column(db.Integer, db.ForeignKey('Profesor.id_profesor'), nullable=False)

    def __repr__(self):
        return f'<CursoProfesor {self.id_curso_profesor}>'

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

@app.route("/cursos")
def listar_cursos():
    cursos = Curso.query.all()
    return render_template("cursos/lista_cursos.html", cursos=cursos)

@app.route("/profesores")
def listar_profesores():
    profesores = Profesor.query.all()
    return render_template("profesores/lista_profesores.html", profesores=profesores)

@app.route("/tareas")
def listar_tareas():
    tareas = Tarea.query.all()
    return render_template("tareas/lista_tareas.html", tareas=tareas)

@app.route("/inscripciones")
def listar_inscripciones():
    inscripciones = Inscripcion.query.all()
    return render_template("inscripciones/lista_inscripciones.html", inscripciones=inscripciones)

@app.route("/comentarios")
def listar_comentarios():
    comentarios = Comentario.query.all()
    return render_template("comentarios/lista_comentarios.html", comentarios=comentarios)

@app.route("/recursos")
def listar_recursos():
    recursos = Recurso.query.all()
    return render_template("recursos/lista_recursos.html", recursos=recursos)

@app.route("/horarios")
def listar_horarios():
    horarios = Horario.query.all()
    return render_template("horarios/lista_horarios.html", horarios=horarios)

@app.route("/notificaciones")
def listar_notificaciones():
    notificaciones = Notificacion.query.all()
    return render_template("notificaciones/lista_notificaciones.html", notificaciones=notificaciones)

@app.route("/roles")
def listar_roles():
    roles = Rol.query.all()
    return render_template("roles/lista_roles.html", roles=roles)

@app.route("/curso_profesores")
def listar_curso_profesores():
    curso_profesores = CursoProfesor.query.all()
    return render_template("curso_profesores/lista_curso_profesores.html", curso_profesores=curso_profesores)

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios/lista_usuarios.html", usuarios=usuarios)

@app.route("/usuarios/crear", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        nuevo_usuario = Usuario(username=username)
        nuevo_usuario.set_password(password)
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
        password = request.form["password"]
        usuario.set_password(password)
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)