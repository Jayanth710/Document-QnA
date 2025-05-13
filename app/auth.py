from flask import Blueprint, jsonify, render_template, request, redirect, session
import logging
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.database_support.database_template import DatabaseTemplate

logger = logging.getLogger(__name__)

from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


def auth_api(db: DatabaseTemplate) -> Blueprint:
    api = Blueprint('auth_api', __name__)

    @api.route('/register', methods=['GET', 'POST'])
    def register():
        try:
            if request.method == 'GET':
                return render_template('register.html')
            
            if request.method == 'POST':
                data = request.get_json()
                logger.info(f'{data}')

                firstname =data.get('firstname')# request.form.get('firstname') #
                lastname = data.get('lastname')#request.form.get('lastname') #
                email = data.get('email')#request.form.get('email') #
                password = data.get('password')#request.form.get('password') #
                

                if not firstname or not email or not password:
                    return jsonify({'message': 'Email and password are required'}), 400
                
                logger.info(f'{email}')

                user_available = db.query("SELECT * FROM users WHERE email = :email", email = email)
                logger.info(f'{user_available.first()}')
                if user_available is None:
                    return jsonify({'message': 'User already exists'}), 400
                
                hashed_password = generate_password_hash(password)

                def insert_user(conn):
                    conn.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO users (firstname, lastname, email, password)
                            VALUES (:firstname, :lastname, :email, :password)
                            """
                        ),
                        {
                            "firstname": firstname,
                            "lastname": lastname,
                            "email": email,
                            "password": hashed_password
                        }
                    )
                
                db.transaction(insert_user)
                logger.info(f'User: {email} created successfully')

                return jsonify({'message': f'User: {email} created successfully'}), 201
            
            else:
                logger.warning('Invalid request method')
                return jsonify({'message': 'Invalid request method'}), 500
            
        except Exception as e:
            logger.error(f'Error: {e}')
            return jsonify({'message': 'Internal server error'}), 500

    @api.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'GET':
                return render_template('login.html')
            
            if request.method == 'POST':
                data = request.get_json()
                logger.info(f"{data}")

                email = data.get('email')#request.form.get('email')#
                password = data.get('password')#request.form.get('password')#
                logger.info(f"User {email} trying to log in")

                response = db.query("SELECT * FROM users WHERE email = :email", email=email)
                
                user = response.first()

                if user and check_password_hash(user.password, password):
                    session["user_id"] = user.id
                    session["email"] = user.email
                    session["name"] = user.firstname

                    logger.info(f"User {user.firstname} logged in successfully.")
                    return jsonify({"status": "success", "message": f"User: {user.firstname} logged in successfully.", "data":{
                        "email": user.email,
                        "name": user.firstname,
                    }}), 200
                
                else:
                    if user is None:
                        logger.error(f"User {email} not found. Please register.")
                        # return render_template('register.html')
                        return jsonify({
                            "message": "User not found",
                            # "status": "redirect",
                            # "redirect": '/register'
                        }), 404
                    
                    logger.error(f"Invalid credentials for user {email}")
                    return jsonify({
                        "message": "Invalid credentials",
                        "status": "error"
                    }), 401
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return jsonify({
                "message": "Internal server error",
                "status": "error"
            }), 500
        
    @api.route('/logout', methods=['POST'])
    def logout():
        try:
            user_email = session.get('email')
            session.clear()
            logger.info(f"User {user_email} logged out successfully.")
            return jsonify({"status": "success", "message": f"User {user_email} logged out successfully."}), 200
        
        except Exception as e:
            logger.error(f"Error: {e}")
            return jsonify({
                "message": "Internal server error",
                "status": "error"
            }), 500
            
                





    return api