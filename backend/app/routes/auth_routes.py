from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from config.database import db_config
except ImportError:
    db_config = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        logger.info(f"🔍 Login attempt for email: {email}")
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Connect to your flowmind database
        if db_config is not None:
            users_collection = db_config.get_users_collection()
            
            # Fix: Check if collection is None instead of boolean check
            if users_collection is not None:
                logger.info(f"✅ Connected to users collection")
                
                # Find user in database
                user = users_collection.find_one({'email': email})
                logger.info(f"📊 User found in database: {user is not None}")
                
                if user is not None:
                    logger.info(f"🔐 Checking password for user: {email}")
                    
                    # Check password - handle both plain text and hashed
                    password_valid = False
                    stored_password = user.get('password', '')
                    
                    if stored_password:
                        # Check if password is hashed (starts with hash prefixes)
                        if stored_password.startswith(('pbkdf2:', 'scrypt:', '$2b$', '$2a$')):
                            password_valid = check_password_hash(stored_password, password)
                            logger.info(f"🔐 Hashed password check: {password_valid}")
                        else:
                            # Plain text password comparison
                            password_valid = (stored_password == password)
                            logger.info(f"🔐 Plain text password check: {password_valid}")
                            logger.info(f"🔐 Stored password: '{stored_password}', Input password: '{password}'")
                            
                            # Update to hashed password for security
                            if password_valid:
                                hashed_password = generate_password_hash(password)
                                users_collection.update_one(
                                    {'_id': user['_id']},
                                    {'$set': {'password': hashed_password}}
                                )
                                logger.info(f"🔒 Updated password to hashed for user: {email}")
                    
                    if password_valid:
                        # Create JWT token
                        access_token = create_access_token(identity=str(user['_id']))
                        
                        logger.info(f"✅ Login successful for user: {email}")
                        return jsonify({
                            'success': True,
                            'message': 'Login successful',
                            'access_token': access_token,
                            'user': {
                                'id': str(user['_id']),
                                'email': user['email'],
                                'name': user.get('name', user.get('username', email.split('@')[0]))
                            }
                        })
                    else:
                        logger.warning(f"❌ Invalid password for user: {email}")
                        return jsonify({
                            'success': False,
                            'message': 'Invalid email or password'
                        }), 401
                else:
                    logger.warning(f"❌ User not found: {email}")
                    return jsonify({
                        'success': False,
                        'message': 'Invalid email or password'
                    }), 401
            else:
                logger.error("❌ Could not connect to users collection")
                return jsonify({
                    'success': False,
                    'message': 'Database connection error'
                }), 500
        else:
            logger.error("❌ Database config not available")
            return jsonify({
                'success': False,
                'message': 'Database not configured'
            }), 500
            
    except Exception as e:
        logger.error(f"💥 Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Internal server error: {str(e)}'
        }), 500

@auth_routes.route('/test', methods=['GET'])
def test():
    return jsonify({
        'success': True,
        'message': 'Auth routes are working!',
        'database_connected': db_config is not None and db_config.connected if db_config else False
    })

@auth_routes.route('/debug-user', methods=['POST'])
def debug_user():
    """Debug endpoint to check user data"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if db_config is not None:
            users_collection = db_config.get_users_collection()
            if users_collection is not None:
                user = users_collection.find_one({'email': email}, {'password': 0})  # Exclude password
                return jsonify({
                    'success': True,
                    'user_found': user is not None,
                    'user_data': user if user is not None else None
                })
        
        return jsonify({
            'success': False,
            'message': 'Database not connected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@auth_routes.route('/check-db', methods=['GET'])
def check_database():
    """Check database connection"""
    try:
        if db_config is not None:
            db = db_config.get_database()
            if db is not None:
                # Get collection names
                collections = db.list_collection_names()
                
                # Count users
                users_collection = db_config.get_users_collection()
                if users_collection is not None:
                    user_count = users_collection.count_documents({})
                    
                    return jsonify({
                        'success': True,
                        'database_name': db_config.DATABASE_NAME,
                        'collections': collections,
                        'user_count': user_count,
                        'connection_status': 'connected'
                    })
        
        return jsonify({
            'success': False,
            'message': 'Database connection failed',
            'connection_status': 'disconnected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'connection_status': 'error'
        })