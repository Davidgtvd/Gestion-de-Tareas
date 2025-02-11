from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    password = db.Column(db.String(100), nullable=False)  # Considera usar hashing
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