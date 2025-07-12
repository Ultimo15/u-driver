import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Conexión a base de datos (CAMBIA ESTO)
DATABASE_URL = "postgresql://neondb_owner:npg_QydCDism46Xq@ep-falling-wave-aelaluc1-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    """Obtener conexión a la base de datos"""
    try:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except Exception as e:
        logger.error(f"Error conectando a DB: {e}")
        return None

def init_db():
    """Inicializar tablas de la base de datos"""
    conn = get_connection()
    if not conn:
        logger.error("No se pudo conectar a la base de datos")
        return
        
    try:
        with conn.cursor() as cur:
            # Tabla de usuarios
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    user_type VARCHAR(20) DEFAULT 'client',
                    subscription_status VARCHAR(20) DEFAULT 'inactive',
                    subscription_end DATE,
                    rating DECIMAL(3,2) DEFAULT 5.00,
                    trips_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de viajes
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trips (
                    id SERIAL PRIMARY KEY,
                    client_id BIGINT REFERENCES users(telegram_id),
                    driver_id BIGINT REFERENCES users(telegram_id),
                    pickup_location TEXT,
                    dropoff_location TEXT,
                    pickup_lat DECIMAL(10,8),
                    pickup_lng DECIMAL(11,8),
                    dropoff_lat DECIMAL(10,8),
                    dropoff_lng DECIMAL(11,8),
                    initial_offer INTEGER,
                    final_price INTEGER,
                    status VARCHAR(20) DEFAULT 'pending',
                    military_code VARCHAR(10),
                    client_rating INTEGER,
                    driver_rating INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)
            
            # Tabla de ofertas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS offers (
                    id SERIAL PRIMARY KEY,
                    trip_id INTEGER REFERENCES trips(id),
                    driver_id BIGINT REFERENCES users(telegram_id),
                    offer_amount INTEGER,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de suscripciones
            cur.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    driver_id BIGINT REFERENCES users(telegram_id),
                    amount INTEGER DEFAULT 20000,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payment_method VARCHAR(20),
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            
            conn.commit()
            logger.info("Base de datos inicializada correctamente")
            
    except Exception as e:
        logger.error(f"Error inicializando DB: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_user(telegram_id, username, first_name, user_type='client'):
    """Agregar o actualizar usuario"""
    conn = get_connection()
    if not conn:
        logger.warning("No hay conexión a DB, usuario no guardado")
        return {"telegram_id": telegram_id, "username": username, "first_name": first_name}
        
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (telegram_id, username, first_name, user_type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (telegram_id) 
                DO UPDATE SET 
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING *
            """, (telegram_id, username, first_name, user_type))
            
            user = cur.fetchone()
            conn.commit()
            return user
            
    except Exception as e:
        logger.error(f"Error agregando usuario: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_user(telegram_id):
    """Obtener información de usuario"""
    conn = get_connection()
    if not conn:
        return None
        
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
            return cur.fetchone()
            
    except Exception as e:
        logger.error(f"Error obteniendo usuario: {e}")
        return None
    finally:
        conn.close()

def create_trip(client_id, pickup_location, dropoff_location, pickup_coords, dropoff_coords, initial_offer):
    """Crear nuevo viaje"""
    conn = get_connection()
    if not conn:
        return None
        
    try:
        with conn.cursor() as cur:
            # Generar código militar aleatorio
            import random
            military_code = f"{random.choice(['ALFA', 'BRAVO', 'CHARLIE', 'DELTA', 'ECHO'])}-{random.randint(100, 999)}"
            
            cur.execute("""
                INSERT INTO trips (
                    client_id, pickup_location, dropoff_location,
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng,
                    initial_offer, military_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (
                client_id, pickup_location, dropoff_location,
                pickup_coords[0], pickup_coords[1],
                dropoff_coords[0], dropoff_coords[1],
                initial_offer, military_code
            ))
            
            trip = cur.fetchone()
            conn.commit()
            return trip
            
    except Exception as e:
        logger.error(f"Error creando viaje: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_active_drivers():
    """Obtener conductores con suscripción activa"""
    conn = get_connection()
    if not conn:
        return []
        
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM users 
                WHERE user_type = 'driver' 
                AND subscription_status = 'active'
                AND subscription_end >= CURRENT_DATE
            """)
            return cur.fetchall()
            
    except Exception as e:
        logger.error(f"Error obteniendo conductores: {e}")
        return []
    finally:
        conn.close()