from flask import Flask
from flask import render_template, request, redirect, url_for
import redis

#export FLASK DEBUG=1
#FLASK run

app = Flask(__name__)

listicket = ['01','02','03','04','05','06','07','08','09','10']

def connect_db():
    """Crear conexion a base de datos."""
    conexion = redis.StrictRedis(host='127.0.0.1', port= 6379, decode_responses=True, charset='utf-8')
    if (conexion.ping()):
        print ("conectado al servidor de redis")
    else:
        print("error...")
    return conexion

@app.route('/')
def index():
    """Retorna la pagina index(Principal)."""
    return render_template('index.html')
    
@app.route('/about')
def about():        
    """Retorna la pagina about."""
    return 'about Python Flask'

@app.route('/imagenes')
def imagenes():
    """Cargar carpeta imagenes"""
    return render_template('imagenes.html',img_path = url_for('static'))


@app.route('/comprar', methods=['GET','POST'])
def compraticket():
    key = request.args.get('c')
    #print("LA CLAVE DEL TICKET ES --> "+key)
    bd = connect_db()
    bd.lpop(key)
    bd.lpush(key,"reservado")
    bd.expire(key,240)
    print(bd.ttl(key))
    return redirect(url_for('tickets'))

@app.route('/confircompra', methods=['GET','POST'])
def terminarcompraticket():
    key = request.args.get('com')
    precio = 250
    bd = connect_db()
    bd.lpop(key)
    bd.lpush(key,'vendido')
    #print("LA CLAVE DEL TICKET ES --> "+key)
    return render_template('confirmar.html',key = key, precio = precio)

@app.route('/tickets')
def tickets():
    dic = {}
    bd = connect_db()
    key = bd.keys('*')
    for t in listicket:
        if t in key:
            for aux in key:
                v = bd.lrange(aux,0,-1)
                value = ''.join(v)
                value.encode('utf-8')
                dic[aux] = value
        else:
            bd.lpush(t,'disponible') 
    return render_template('tickets.html', dic = dic)    

if __name__ == '__main__':
    app.run(host ='localhost', port='5000', debug=True)    