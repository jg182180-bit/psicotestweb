from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --------------------------------
# BASE DE DATOS
# --------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menteyfe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------------
# MODELO
# --------------------------------
class Evaluacion(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.String(100))

    nombre = db.Column(db.String(100))
    edad = db.Column(db.String(20))
    telefono = db.Column(db.String(30))

    ciudad = db.Column(db.String(100))
    barrio = db.Column(db.String(100))
    direccion = db.Column(db.String(200))

    ocupacion = db.Column(db.String(100))

    p1 = db.Column(db.Integer)
    p2 = db.Column(db.Integer)
    p3 = db.Column(db.Integer)
    p4 = db.Column(db.Integer)
    p5 = db.Column(db.Integer)
    p6 = db.Column(db.Integer)
    p7 = db.Column(db.Integer)
    p8 = db.Column(db.Integer)
    p9 = db.Column(db.Integer)
    p10 = db.Column(db.Integer)
    p11 = db.Column(db.Integer)
    p12 = db.Column(db.Integer)

    observacion = db.Column(db.Text)

    estres = db.Column(db.Integer)
    ansiedad = db.Column(db.Integer)
    autoestima = db.Column(db.Integer)
    bienestar = db.Column(db.Integer)

    puntaje = db.Column(db.Integer)

    resultado = db.Column(db.String(300))

    mensaje = db.Column(db.Text)

    recomendacion = db.Column(db.Text)

# --------------------------------
# CREAR BD
# --------------------------------
with app.app_context():
    db.create_all()

# --------------------------------
# FUNCIÓN NIVELES
# --------------------------------
def obtener_nivel(valor):

    if valor <= 2:
        return "🟢 Bajo"

    elif valor <= 5:
        return "🟡 Moderado"

    else:
        return "🔴 Alto"

# --------------------------------
# INICIO
# --------------------------------
@app.route('/')
def inicio():

    return render_template('inicio.html')

# --------------------------------
# DATOS PERSONALES
# --------------------------------
@app.route('/datos')
def datos():

    return render_template('datos.html')

# --------------------------------
# TEST
# --------------------------------
@app.route('/test', methods=['POST'])
def test():

    return render_template(

        'test.html',

        nombre=request.form['nombre'],
        edad=request.form['edad'],
        telefono=request.form['telefono'],

        ciudad=request.form['ciudad'],
        barrio=request.form['barrio'],
        direccion=request.form['direccion'],

        ocupacion=request.form['ocupacion']

    )

# --------------------------------
# RESULTADO
# --------------------------------
@app.route('/resultado', methods=['POST'])
def resultado():

    # DATOS PERSONALES
    nombre = request.form['nombre']
    edad = request.form['edad']
    telefono = request.form['telefono']

    ciudad = request.form['ciudad']
    barrio = request.form['barrio']
    direccion = request.form['direccion']

    ocupacion = request.form['ocupacion']

    # RESPUESTAS
    p1 = int(request.form['p1'])
    p2 = int(request.form['p2'])
    p3 = int(request.form['p3'])
    p4 = int(request.form['p4'])
    p5 = int(request.form['p5'])
    p6 = int(request.form['p6'])
    p7 = int(request.form['p7'])
    p8 = int(request.form['p8'])
    p9 = int(request.form['p9'])
    p10 = int(request.form['p10'])
    p11 = int(request.form['p11'])
    p12 = int(request.form['p12'])

    observacion = request.form['observacion']

    # --------------------------------
    # ÁREAS
    # --------------------------------
    estres = p1 + p2 + p3
    ansiedad = p4 + p5 + p6
    autoestima = p7 + p8 + p9
    bienestar = p10 + p11 + p12

    puntaje = (
        p1+p2+p3+p4+p5+p6+
        p7+p8+p9+p10+p11+p12
    )

    # --------------------------------
    # NIVELES
    # --------------------------------
    nivel_estres = obtener_nivel(estres)
    nivel_ansiedad = obtener_nivel(ansiedad)
    nivel_autoestima = obtener_nivel(autoestima)
    nivel_bienestar = obtener_nivel(bienestar)

    # --------------------------------
    # MOTOR IA
    # --------------------------------
    mensaje = ""
    recomendacion = ""

    resultado_final = "Perfil emocional analizado"

    # PERFIL POSITIVO
    if (

        ansiedad <= 2 and
        estres <= 2 and
        autoestima >= 6 and
        bienestar >= 6

    ):

        resultado_final = "Perfil emocional saludable"

        mensaje += """
        La evaluación refleja adecuados niveles
        de bienestar emocional,
        estabilidad psicológica
        y percepción positiva personal.
        """

        recomendacion += """
        Continúe fortaleciendo hábitos saludables,
        equilibrio emocional
        y autocuidado personal.
        """

    # ANSIEDAD
    if ansiedad >= 6:

        mensaje += """
        Se identifican indicadores elevados
        de ansiedad emocional,
        preocupación persistente
        y tensión psicológica.
        """

    elif ansiedad >= 3:

        mensaje += """
        Se observan indicadores moderados
        de tensión emocional
        y preocupación ocasional.
        """

    else:

        mensaje += """
        La evaluación refleja adecuados niveles
        de regulación emocional.
        """

    # ESTRÉS
    if estres >= 6:

        mensaje += """
        También se evidencian signos
        de sobrecarga emocional
        y agotamiento psicológico.
        """

    elif estres >= 3:

        mensaje += """
        Se observan niveles moderados
        de estrés cotidiano.
        """

    else:

        mensaje += """
        Se identifican adecuados recursos
        para afrontar situaciones de presión.
        """

    # AUTOESTIMA
    if autoestima <= 3:

        mensaje += """
        La evaluación refleja posibles dificultades
        relacionadas con autoestima
        y seguridad personal.
        """

    elif autoestima <= 5:

        mensaje += """
        Se observan algunas variaciones
        relacionadas con confianza emocional.
        """

    else:

        mensaje += """
        La evaluación refleja adecuados niveles
        de autoestima y autoconfianza.
        """

    # BIENESTAR
    if bienestar <= 3:

        mensaje += """
        Se identifican indicadores asociados
        a disminución del bienestar emocional.
        """

    elif bienestar <= 5:

        mensaje += """
        Se observan algunas variaciones
        en bienestar psicológico.
        """

    else:

        mensaje += """
        La evaluación refleja adecuados niveles
        de bienestar emocional.
        """

    # CRUCES
    if ansiedad >= 6 and autoestima <= 3:

        mensaje += """
        El perfil emocional observado
        sugiere tensión psicológica
        acompañada de vulnerabilidad emocional.
        """

    # OBSERVACIÓN
    if observacion != "":

        mensaje += f"""

        Información adicional proporcionada:
        "{observacion}"
        """

    # RECOMENDACIÓN GENERAL
    recomendacion += """
    Se recomienda continuar fortaleciendo
    hábitos saludables,
    bienestar emocional
    y apoyo social.
    """

    # FECHA
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # GUARDAR
    evaluacion = Evaluacion(

        fecha=fecha_actual,

        nombre=nombre,
        edad=edad,
        telefono=telefono,

        ciudad=ciudad,
        barrio=barrio,
        direccion=direccion,

        ocupacion=ocupacion,

        p1=p1,
        p2=p2,
        p3=p3,
        p4=p4,
        p5=p5,
        p6=p6,
        p7=p7,
        p8=p8,
        p9=p9,
        p10=p10,
        p11=p11,
        p12=p12,

        observacion=observacion,

        estres=estres,
        ansiedad=ansiedad,
        autoestima=autoestima,
        bienestar=bienestar,

        puntaje=puntaje,

        resultado=resultado_final,

        mensaje=mensaje,

        recomendacion=recomendacion

    )

    db.session.add(evaluacion)
    db.session.commit()

    return render_template(

        'resultado.html',

        nombre=nombre,

        resultado=resultado_final,

        puntaje=puntaje,

        mensaje=mensaje,

        recomendacion=recomendacion,

        nivel_estres=nivel_estres,
        nivel_ansiedad=nivel_ansiedad,
        nivel_autoestima=nivel_autoestima,
        nivel_bienestar=nivel_bienestar

    )

# --------------------------------
# ADMIN
# --------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        clave = request.form['clave']

        if clave == "sena2026":

            datos = Evaluacion.query.order_by(
                Evaluacion.id.desc()
            ).all()

            return render_template(

                'historial.html',

                datos=datos,

                obtener_nivel=obtener_nivel

            )

        else:

            return """
            <h2>❌ Contraseña incorrecta</h2>
            <a href="/admin">Volver</a>
            """

    return """
    <h2 style='text-align:center;margin-top:50px;'>
        🔐 Acceso Profesional
    </h2>

    <form method="POST"
          style='max-width:400px;margin:auto;'>

        <input type="password"
               name="clave"
               class="form-control mb-3"
               placeholder="Ingrese contraseña">

        <button type="submit"
                class="btn btn-dark w-100">

            Ingresar

        </button>

    </form>
    """

# --------------------------------
# EJECUTAR
# --------------------------------
if __name__ == '__main__':

    app.run(debug=True)