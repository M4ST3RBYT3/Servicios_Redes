from flask import Flask, request, render_template

app = Flask(__name__)
ventas = []
x = 0

@app.route('/MyApp', methods=["POST", "GET"])
def main_view():
    if request.method == "POST":
        description = request.form["description"]
        amount = request.form["amount"]
        count = request.form["count"]
        ventas.append((description,amount,count))
        return render_template('analizador.html', d = '', a = '', c = '')
    else:
        return render_template('analizador.html', d = '', a = '', c = '')
    
@app.route('/Ventas')
def autor_view():
    return render_template('autor.html', v = ventas)

if __name__ == '__main__':
    app.run(debug=True)