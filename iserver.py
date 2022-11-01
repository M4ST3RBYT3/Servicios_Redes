from flask import Flask, request, render_template
from gramatica import parser
from Ambito.Ambito import *

app = Flask(__name__)
modulosE = None
modulosI = None

def analizer(input :str) -> str:
    global modulosE
    global modulosI
    ambG = Ambito(None)
    output = parser.parse(input)
    # Primera pasada
    # Reconoce modulos y funciones
    for i in output:
        i.exec(ambG)
    diccionario = ambG.getMods()
    bases = []
    items = []
    for db in diccionario.keys():
        tablas = diccionario.get(db)
        if tablas.mods != None:
            bases.append((db, len(tablas.mods), tablas.line))
            for table in tablas.mods.keys():
                last = tablas.mods.get(table)
                items.append((table, db, last.line))
    modulosE = bases
    modulosI = items
    # Segunda pasada
    # Ejecuta funcion MAIN y llamadas dentro de ella
    tmp = ambG.fun.get('main')
    salida = "Error: se esperaba la funcion main"
    if tmp != None:
        tmp.inst.exec(ambG)
        salida = ambG.console
    return salida

def compiler(input: str) -> str:
    output = parser.parse(input)

@app.route('/MyApp', methods=["POST", "GET"])
def main_view():
    if request.method == "POST":
        buffer = request.form["input"]
        output = analizer(buffer)
        return render_template('analizador.html', buffer = buffer, output = output)
    else:
        return render_template('analizador.html', buffer = "")
    
@app.route('/reportes')
def ejemplo_view():
    return render_template('ejemplo.html', bases=modulosE, tb=len(modulosE), tablas=modulosI, tt=len(modulosI))

@app.route('/autor')
def autor_view():
    return render_template('autor.html')

@app.route('/c3d', methods=["POST", "GET"])
def code_view():
    if request.method == "POST":
        buffer = request.form["input"]
        output = analizer(buffer)
        return render_template('analizador.html', buffer = buffer, output = output)
    else:
        return render_template('code.html')

if __name__ == '__main__':
    app.run(debug=True)