from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menteyfe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO
class Evaluacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    celular = db.Column(db.String(20))
    situacion = db.Column(db.Text)
    puntaje = db.Column(db.Integer)
    resultado = db.Column(db.String(100))

# Crear BD
with app.app_context():
    db.create_all()

# -------------------------------
# TEST PSICOLÓGICO
# -------------------------------
@app.route('/', methods=['GET', 'POST'])
def test():

    if request.method == 'POST':
        nombre = request.form['nombre']
        celular = request.form['celular']
        situacion = request.form['situacion']

        # Simulación (luego lo hacemos real)
        puntaje = 47

        if puntaje < 50:
            resultado = "Alerta leve"
        elif puntaje < 70:
            resultado = "Moderado"
        else:
            resultado = "Alto"

        # Guardar en BD
        evaluacion = Evaluacion(
            nombre=nombre,
            celular=celular,
            situacion=situacion,
            puntaje=puntaje,
            resultado=resultado
        )

        db.session.add(evaluacion)
        db.session.commit()

        return f"""
        <h2>Resultado: {resultado}</h2>
        <p><strong>Puntaje:</strong> {puntaje}</p>

        <p><strong>Nombre:</strong> {nombre}</p>
        <p><strong>Celular:</strong> {celular}</p>
        <p><strong>Situación:</strong> {situacion}</p>

        <p>Se recomienda fortalecer el autocuidado.</p>
        <p><em>Evaluación realizada por el psicólogo José Manuel González Romero</em></p>

        <br><br>

        <button onclick="window.location.href='/'">🔄 Hacer otro test</button>
        <br><br>
        <button onclick="window.location.href='/ver'">📊 Ver historial</button>
        """

    return '''
    <h2>Test Psicológico MenteYFe</h2>
    <form method="POST">
        Nombre:<br>
        <input type="text" name="nombre" required><br><br>

        Celular:<br>
        <input type="text" name="celular" required><br><br>

        Cuéntanos tu situación:<br>
        <textarea name="situacion" rows="4" cols="40"></textarea><br><br>

        <button type="submit">Evaluar</button>
    </form>
    '''

# -------------------------------
# HISTORIAL
# -------------------------------
@app.route('/ver')
def ver():
    datos = Evaluacion.query.all()

    html = "<h2>Historial de Evaluaciones</h2>"

    if not datos:
        html += "<p>No hay evaluaciones registradas.</p>"
    else:
        for d in datos:
            html += f"""
            <p>
            <strong>{d.nombre}</strong><br>
            Celular: {d.celular}<br>
            Resultado: {d.resultado} (Puntaje: {d.puntaje})<br>
            Situación: {d.situacion}
            </p>
            <hr>
            """

    html += '<br><button onclick="window.location.href=\'/\'">⬅ Volver al test</button>'

    return html

# -------------------------------
# EJECUTAR
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)