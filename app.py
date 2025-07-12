from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from database import get_user, create_trip, get_active_drivers
import logging

app = Flask(__name__)
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta principal
@app.route('/')
def index():
    return jsonify({"status": "U-Driver API activa", "version": "1.0"})

# Ruta para Mini App Cliente
@app.route('/cliente')
def cliente_app():
    return render_template('cliente.html')

# Ruta para Mini App Conductor
@app.route('/conductor')
def conductor_app():
    return render_template('conductor.html')

# API: Obtener datos de usuario
@app.route('/api/user/<int:telegram_id>')
def get_user_data(telegram_id):
    user = get_user(telegram_id)
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "Usuario no encontrado"}), 404

# API: Crear viaje
@app.route('/api/trip', methods=['POST'])
def create_new_trip():
    try:
        data = request.json
        trip = create_trip(
            client_id=data['client_id'],
            pickup_location=data['pickup_location'],
            dropoff_location=data['dropoff_location'],
            pickup_coords=(data['pickup_lat'], data['pickup_lng']),
            dropoff_coords=(data['dropoff_lat'], data['dropoff_lng']),
            initial_offer=data['initial_offer']
        )
        
        if trip:
            # Notificar a conductores activos
            drivers = get_active_drivers()
            # Aquí agregaremos notificaciones después
            
            return jsonify(dict(trip))
        return jsonify({"error": "Error creando viaje"}), 500
        
    except Exception as e:
        logger.error(f"Error en create_trip: {e}")
        return jsonify({"error": str(e)}), 500

# API: Obtener conductores activos
@app.route('/api/drivers/active')
def active_drivers():
    drivers = get_active_drivers()
    return jsonify([dict(d) for d in drivers])

# Archivos estáticos
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Ejecutar servidor
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)