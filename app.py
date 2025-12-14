"""
Factory Management System - Flask Backend
Complete backend implementation with SQLAlchemy ORM, JWT authentication, and RESTful APIs
Author: Factory Management Team
Version: 1.0.0
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)

# ===================== CONFIGURATION =====================

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///factory_management.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# ===================== DATABASE MODELS =====================

class User(db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin or manager
    status = db.Column(db.String(20), default='active')
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        if not self.password_hash:
            return False
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            print(f"Password check error: {str(e)}")
            return False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'status': self.status,
            'department': self.department,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Order(db.Model):
    """Order model for managing customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    product = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50), default='yet-to-process')
    priority = db.Column(db.String(20), default='medium')
    deadline = db.Column(db.Date, nullable=False)
    special_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    status_history = db.relationship('OrderStatusHistory', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'product': self.product,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'status': self.status,
            'priority': self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'special_instructions': self.special_instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }


class OrderStatusHistory(db.Model):
    """Track order status changes"""
    __tablename__ = 'order_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'comment': self.comment,
            'changed_by': self.changed_by,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None
        }


class InventoryItem(db.Model):
    """Inventory item model"""
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(20), unique=True, nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    current_stock = db.Column(db.Float, nullable=False, default=0)
    min_level = db.Column(db.Float, nullable=False)
    max_level = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    supplier = db.Column(db.String(120))
    unit_cost = db.Column(db.Float)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_movements = db.relationship('StockMovement', backref='inventory_item', lazy=True, cascade='all, delete-orphan')
    
    def get_status(self):
        """Determine stock status"""
        if self.current_stock == 0:
            return 'out-of-stock'
        elif self.current_stock < self.min_level:
            return 'low-stock'
        else:
            return 'in-stock'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'item_code': self.item_code,
            'item_name': self.item_name,
            'category': self.category,
            'current_stock': self.current_stock,
            'min_level': self.min_level,
            'max_level': self.max_level,
            'unit': self.unit,
            'status': self.get_status(),
            'description': self.description,
            'supplier': self.supplier,
            'unit_cost': self.unit_cost,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class StockMovement(db.Model):
    """Track inventory stock movements"""
    __tablename__ = 'stock_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)  # add, remove, adjust
    quantity = db.Column(db.Float, nullable=False)
    previous_stock = db.Column(db.Float, nullable=False)
    new_stock = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    moved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    moved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'previous_stock': self.previous_stock,
            'new_stock': self.new_stock,
            'reason': self.reason,
            'moved_by': self.moved_by,
            'moved_at': self.moved_at.isoformat() if self.moved_at else None
        }


class RawMaterial(db.Model):
    """Raw materials management"""
    __tablename__ = 'raw_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.String(20), unique=True, nullable=False)
    material_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    current_stock = db.Column(db.Float, nullable=False, default=0)
    min_level = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(120))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_status(self):
        """Determine stock status"""
        if self.current_stock == 0:
            return 'out-of-stock'
        elif self.current_stock < self.min_level:
            return 'low-stock'
        else:
            return 'in-stock'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'material_id': self.material_id,
            'material_name': self.material_name,
            'category': self.category,
            'current_stock': self.current_stock,
            'min_level': self.min_level,
            'unit': self.unit,
            'unit_price': self.unit_price,
            'total_value': round(self.current_stock * self.unit_price, 2),
            'status': self.get_status(),
            'supplier': self.supplier,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PurchaseOrder(db.Model):
    """Purchase orders for raw materials"""
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.String(20), unique=True, nullable=False)
    material_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(120), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    expected_delivery = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='ordered')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'po_id': self.po_id,
            'material_name': self.material_name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'unit_price': self.unit_price,
            'total_cost': self.total_cost,
            'supplier': self.supplier,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'expected_delivery': self.expected_delivery.isoformat() if self.expected_delivery else None,
            'status': self.status,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ActivityLog(db.Model):
    """Activity logging for audit trail"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ===================== DECORATORS & UTILITIES =====================

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


def log_activity(action, details=None):
    """Helper function to log user activity"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        if user:
            activity = ActivityLog(
                user_id=user.id,
                action=action,
                details=details,
                ip_address=request.remote_addr
            )
            db.session.add(activity)
            db.session.commit()
    except:
        pass  # Don't fail if logging fails


# ===================== AUTHENTICATION ROUTES =====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Try to find user by username first, then by user_id
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User.query.filter_by(user_id=username).first()
        
        if not user:
            print(f"Login attempt failed: User '{username}' not found")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if password hash exists
        if not user.password_hash:
            print(f"Login attempt failed: User '{username}' has no password set")
            return jsonify({'error': 'Password not set for this user. Please contact administrator.'}), 401
        
        # Verify password
        password_valid = user.check_password(password)
        print(f"Login attempt for user '{username}' (role: {user.role}): Password check = {password_valid}")
        
        if not password_valid:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if user.status != 'active':
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.user_id)
        
        # Log activity
        activity = ActivityLog(
            user_id=user.id,
            action='Login',
            details='Successful login',
            ip_address=request.remote_addr
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        import traceback
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'An error occurred during login. Please try again.'}), 500


@app.route('/api/auth/register', methods=['POST'])
@admin_required
def register():
    """Register new user (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Generate user_id
        user_count = User.query.count()
        user_id = f"USR-{str(user_count + 1).zfill(3)}"
        
        # Create new user
        user = User(
            user_id=user_id,
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            role=data['role'],
            department=data.get('department'),
            phone=data.get('phone'),
            status=data.get('status', 'active')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        log_activity('User Created', f'Created user: {user.username}')
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== USER MANAGEMENT ROUTES =====================

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'department' in data:
            user.department = data['department']
        if 'phone' in data:
            user.phone = data['phone']
        if 'status' in data:
            user.status = data['status']
        if 'password' in data:
            # Ensure password is not empty and properly hashed
            password = data['password'].strip()
            if password:
                user.set_password(password)
            else:
                return jsonify({'error': 'Password cannot be empty'}), 400
        
        db.session.commit()
        
        log_activity('User Updated', f'Updated user: {user.username}')
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """Reset user password (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'password' not in data:
            return jsonify({'error': 'New password is required'}), 400
        
        new_password = data['password'].strip()
        
        if not new_password:
            return jsonify({'error': 'Password cannot be empty'}), 400
        
        # Reset password
        user.set_password(new_password)
        db.session.commit()
        
        log_activity('Password Reset', f'Password reset for user: {user.username}')
        
        return jsonify({
            'message': 'Password reset successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'user_id': user.user_id
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.role == 'admin':
            # Count admin users
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count <= 1:
                return jsonify({'error': 'Cannot delete the last admin user'}), 403
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        log_activity('User Deleted', f'Deleted user: {username}')
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== ORDER MANAGEMENT ROUTES =====================

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders with optional filters"""
    try:
        status = request.args.get('status')
        customer = request.args.get('customer')
        priority = request.args.get('priority')
        
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        if customer:
            query = query.filter(Order.customer_name.ilike(f'%{customer}%'))
        if priority:
            query = query.filter_by(priority=priority)
        
        orders = query.order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get specific order"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_dict = order.to_dict()
        order_dict['status_history'] = [history.to_dict() for history in order.status_history]
        
        return jsonify(order_dict), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders', methods=['POST'])
@admin_required
def create_order():
    """Create new order (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'product', 'quantity', 'deadline']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate unique order_id robustly
        def generate_unique_order_id():
            # Start with count-based, then increment until free to avoid collisions after deletes/seed data
            next_num = Order.query.count() + 1
            attempt_limit = 1000
            while attempt_limit > 0:
                candidate = f"ORD-{str(next_num).zfill(4)}"
                if not Order.query.filter_by(order_id=candidate).first():
                    return candidate
                next_num += 1
                attempt_limit -= 1
            # Fallback to timestamp-based if somehow exhausted
            return f"ORD-{int(datetime.utcnow().timestamp())}"

        order_id = generate_unique_order_id()
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        # Calculate total amount if unit price is provided
        unit_price = data.get('unit_price', 0)
        quantity = data['quantity']
        total_amount = unit_price * quantity if unit_price else None
        
        # Create order
        order = Order(
            order_id=order_id,
            customer_name=data['customer_name'],
            product=data['product'],
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date(),
            priority=data.get('priority', 'medium'),
            special_instructions=data.get('special_instructions'),
            created_by=user.id
        )
        
        db.session.add(order)
        try:
            db.session.commit()
        except IntegrityError:
            # Retry once with a fresh id in case of race or collision
            db.session.rollback()
            order.order_id = generate_unique_order_id()
            db.session.add(order)
            db.session.commit()
        
        log_activity('Order Created', f'Created order: {order.order_id}')
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """Update order"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        data = request.get_json()
        
        # Admins can update all fields, managers can only update status
        if user.role == 'admin':
            if 'customer_name' in data:
                order.customer_name = data['customer_name']
            if 'product' in data:
                order.product = data['product']
            if 'quantity' in data:
                order.quantity = data['quantity']
            if 'unit_price' in data:
                order.unit_price = data['unit_price']
            if 'total_amount' in data:
                order.total_amount = data['total_amount']
            elif 'unit_price' in data or 'quantity' in data:
                # Recalculate total amount
                order.total_amount = order.unit_price * order.quantity if order.unit_price else None
            if 'deadline' in data:
                order.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            if 'priority' in data:
                order.priority = data['priority']
            if 'special_instructions' in data:
                order.special_instructions = data['special_instructions']
        
        # Both admin and manager can update status
        if 'status' in data:
            old_status = order.status
            order.status = data['status']
            
            # Create status history
            status_history = OrderStatusHistory(
                order_id=order.id,
                old_status=old_status,
                new_status=data['status'],
                comment=data.get('comment'),
                changed_by=user.id
            )
            db.session.add(status_history)
        
        db.session.commit()
        
        log_activity('Order Updated', f'Updated order: {order.order_id}')
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order(order_id):
    """Delete order (admin only)"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_ref = order.order_id
        db.session.delete(order)
        db.session.commit()
        
        log_activity('Order Deleted', f'Deleted order: {order_ref}')
        
        return jsonify({'message': 'Order deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== INVENTORY MANAGEMENT ROUTES =====================

@app.route('/api/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    """Get all inventory items"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = InventoryItem.query
        
        if category:
            query = query.filter_by(category=category)
        
        items = query.all()
        
        if status:
            items = [item for item in items if item.get_status() == status]
        
        return jsonify([item.to_dict() for item in items]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>', methods=['GET'])
@jwt_required()
def get_inventory_item(item_id):
    """Get specific inventory item"""
    try:
        item = InventoryItem.query.get(item_id)
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        item_dict = item.to_dict()
        item_dict['stock_movements'] = [movement.to_dict() for movement in item.stock_movements]
        
        return jsonify(item_dict), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory', methods=['POST'])
@admin_required
def create_inventory_item():
    """Create new inventory item (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['item_name', 'category', 'current_stock', 'min_level', 'max_level', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate item_code
        item_count = InventoryItem.query.count()
        item_code = f"ITM-{str(item_count + 1).zfill(4)}"
        
        # Create item
        item = InventoryItem(
            item_code=item_code,
            item_name=data['item_name'],
            category=data['category'],
            current_stock=data['current_stock'],
            min_level=data['min_level'],
            max_level=data['max_level'],
            unit=data['unit'],
            description=data.get('description'),
            supplier=data.get('supplier'),
            unit_cost=data.get('unit_cost'),
            location=data.get('location')
        )
        
        db.session.add(item)
        db.session.commit()
        
        log_activity('Inventory Item Created', f'Created item: {item.item_code}')
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>/adjust', methods=['POST'])
@admin_required
def adjust_inventory(item_id):
    """Adjust inventory stock (admin only)"""
    try:
        item = InventoryItem.query.get(item_id)
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if 'movement_type' not in data or 'quantity' not in data or 'reason' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        movement_type = data['movement_type']
        quantity = float(data['quantity'])
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        # Calculate new stock
        previous_stock = item.current_stock
        
        if movement_type == 'add':
            new_stock = previous_stock + quantity
        elif movement_type == 'remove':
            if quantity > previous_stock:
                return jsonify({'error': 'Insufficient stock'}), 400
            new_stock = previous_stock - quantity
        elif movement_type == 'adjust':
            new_stock = quantity
        else:
            return jsonify({'error': 'Invalid movement type. Use: add, remove, or adjust'}), 400
        
        # Update stock
        item.current_stock = new_stock
        
        # Create movement record
        movement = StockMovement(
            item_id=item.id,
            movement_type=movement_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reason=data['reason'],
            moved_by=user.id
        )
        
        db.session.add(movement)
        db.session.commit()
        
        log_activity('Inventory Adjusted', f'Adjusted stock for {item.item_code}: {movement_type} {quantity}')
        
        return jsonify({
            'message': 'Stock adjusted successfully',
            'item': item.to_dict(),
            'movement': movement.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
@admin_required
def update_inventory_item(item_id):
    """Update inventory item (admin only)"""
    try:
        item = InventoryItem.query.get(item_id)
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'item_name' in data:
            item.item_name = data['item_name']
        if 'category' in data:
            item.category = data['category']
        # Support updating current stock directly via this endpoint and record movement
        if 'current_stock' in data:
            try:
                new_stock_value = float(data['current_stock'])
            except (TypeError, ValueError):
                return jsonify({'error': 'current_stock must be a number'}), 400
            previous_stock_value = item.current_stock
            if new_stock_value != previous_stock_value:
                # Get current user for movement tracking
                current_user_id = get_jwt_identity()
                user = User.query.filter_by(user_id=current_user_id).first()
                # Update stock
                item.current_stock = new_stock_value
                # Create a stock movement record to preserve audit trail
                movement = StockMovement(
                    item_id=item.id,
                    movement_type='adjust',
                    quantity=new_stock_value,  # quantity represents the target when using 'adjust'
                    previous_stock=previous_stock_value,
                    new_stock=new_stock_value,
                    reason=data.get('reason', 'Stock adjusted via item update'),
                    moved_by=user.id if user else None
                )
                db.session.add(movement)
        if 'min_level' in data:
            item.min_level = data['min_level']
        if 'max_level' in data:
            item.max_level = data['max_level']
        if 'unit' in data:
            item.unit = data['unit']
        if 'description' in data:
            item.description = data['description']
        if 'supplier' in data:
            item.supplier = data['supplier']
        if 'unit_cost' in data:
            item.unit_cost = data['unit_cost']
        if 'location' in data:
            item.location = data['location']
        
        db.session.commit()
        
        log_activity('Inventory Item Updated', f'Updated item: {item.item_code}')
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_inventory_item(item_id):
    """Delete inventory item (admin only)"""
    try:
        item = InventoryItem.query.get(item_id)
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        item_code = item.item_code
        db.session.delete(item)
        db.session.commit()
        
        log_activity('Inventory Item Deleted', f'Deleted item: {item_code}')
        
        return jsonify({'message': 'Item deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== RAW MATERIALS MANAGEMENT ROUTES =====================

@app.route('/api/raw-materials', methods=['GET'])
@jwt_required()
def get_raw_materials():
    """Get all raw materials"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = RawMaterial.query
        
        if category:
            query = query.filter_by(category=category)
        
        materials = query.all()
        
        if status:
            materials = [material for material in materials if material.get_status() == status]
        
        return jsonify([material.to_dict() for material in materials]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/raw-materials/<int:material_id>', methods=['GET'])
@jwt_required()
def get_raw_material(material_id):
    """Get specific raw material"""
    try:
        material = RawMaterial.query.get(material_id)
        
        if not material:
            return jsonify({'error': 'Material not found'}), 404
        
        return jsonify(material.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/raw-materials', methods=['POST'])
@admin_required
def create_raw_material():
    """Create new raw material (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['material_name', 'category', 'current_stock', 'min_level', 'unit', 'unit_price']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate material_id
        material_count = RawMaterial.query.count()
        material_id = f"MAT-{str(material_count + 1).zfill(4)}"
        
        # Create material
        material = RawMaterial(
            material_id=material_id,
            material_name=data['material_name'],
            category=data['category'],
            current_stock=data['current_stock'],
            min_level=data['min_level'],
            unit=data['unit'],
            unit_price=data['unit_price'],
            supplier=data.get('supplier'),
            description=data.get('description')
        )
        
        db.session.add(material)
        db.session.commit()
        
        log_activity('Raw Material Created', f'Created material: {material.material_id}')
        
        return jsonify({
            'message': 'Material created successfully',
            'material': material.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/raw-materials/<int:material_id>', methods=['PUT'])
@admin_required
def update_raw_material(material_id):
    """Update raw material (admin only)"""
    try:
        material = RawMaterial.query.get(material_id)
        
        if not material:
            return jsonify({'error': 'Material not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'material_name' in data:
            material.material_name = data['material_name']
        if 'category' in data:
            material.category = data['category']
        if 'current_stock' in data:
            material.current_stock = data['current_stock']
        if 'min_level' in data:
            material.min_level = data['min_level']
        if 'unit' in data:
            material.unit = data['unit']
        if 'unit_price' in data:
            material.unit_price = data['unit_price']
        if 'supplier' in data:
            material.supplier = data['supplier']
        if 'description' in data:
            material.description = data['description']
        
        db.session.commit()
        
        log_activity('Raw Material Updated', f'Updated material: {material.material_id}')
        
        return jsonify({
            'message': 'Material updated successfully',
            'material': material.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/raw-materials/<int:material_id>', methods=['DELETE'])
@admin_required
def delete_raw_material(material_id):
    """Delete raw material (admin only)"""
    try:
        material = RawMaterial.query.get(material_id)
        
        if not material:
            return jsonify({'error': 'Material not found'}), 404
        
        material_ref = material.material_id
        db.session.delete(material)
        db.session.commit()
        
        log_activity('Raw Material Deleted', f'Deleted material: {material_ref}')
        
        return jsonify({'message': 'Material deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== PURCHASE ORDER ROUTES =====================

@app.route('/api/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():
    """Get all purchase orders"""
    try:
        status = request.args.get('status')
        supplier = request.args.get('supplier')
        
        query = PurchaseOrder.query
        
        if status:
            query = query.filter_by(status=status)
        if supplier:
            query = query.filter(PurchaseOrder.supplier.ilike(f'%{supplier}%'))
        
        purchase_orders = query.order_by(PurchaseOrder.created_at.desc()).all()
        return jsonify([po.to_dict() for po in purchase_orders]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders/<int:po_id>', methods=['GET'])
@jwt_required()
def get_purchase_order(po_id):
    """Get specific purchase order"""
    try:
        po = PurchaseOrder.query.get(po_id)
        
        if not po:
            return jsonify({'error': 'Purchase order not found'}), 404
        
        return jsonify(po.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders', methods=['POST'])
@admin_required
def create_purchase_order():
    """Create new purchase order (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['material_name', 'category', 'quantity', 'unit', 'unit_price', 'supplier', 'order_date', 'expected_delivery']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate po_id
        po_count = PurchaseOrder.query.count()
        po_id = f"PO-{str(po_count + 1).zfill(4)}"
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()
        
        # Calculate total cost
        total_cost = float(data['quantity']) * float(data['unit_price'])
        
        # Create purchase order
        po = PurchaseOrder(
            po_id=po_id,
            material_name=data['material_name'],
            category=data['category'],
            quantity=data['quantity'],
            unit=data['unit'],
            unit_price=data['unit_price'],
            total_cost=total_cost,
            supplier=data['supplier'],
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            expected_delivery=datetime.strptime(data['expected_delivery'], '%Y-%m-%d').date(),
            notes=data.get('notes'),
            created_by=user.id
        )
        
        db.session.add(po)
        db.session.commit()
        
        log_activity('Purchase Order Created', f'Created PO: {po.po_id}')
        
        return jsonify({
            'message': 'Purchase order created successfully',
            'purchase_order': po.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders/<int:po_id>', methods=['PUT'])
@admin_required
def update_purchase_order(po_id):
    """Update purchase order (admin only)"""
    try:
        po = PurchaseOrder.query.get(po_id)
        
        if not po:
            return jsonify({'error': 'Purchase order not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'material_name' in data:
            po.material_name = data['material_name']
        if 'category' in data:
            po.category = data['category']
        if 'quantity' in data:
            po.quantity = data['quantity']
        if 'unit' in data:
            po.unit = data['unit']
        if 'unit_price' in data:
            po.unit_price = data['unit_price']
        if 'supplier' in data:
            po.supplier = data['supplier']
        if 'order_date' in data:
            po.order_date = datetime.strptime(data['order_date'], '%Y-%m-%d').date()
        if 'expected_delivery' in data:
            po.expected_delivery = datetime.strptime(data['expected_delivery'], '%Y-%m-%d').date()
        if 'status' in data:
            po.status = data['status']
        if 'notes' in data:
            po.notes = data['notes']
        
        # Recalculate total cost
        po.total_cost = po.quantity * po.unit_price
        
        db.session.commit()
        
        log_activity('Purchase Order Updated', f'Updated PO: {po.po_id}')
        
        return jsonify({
            'message': 'Purchase order updated successfully',
            'purchase_order': po.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders/<int:po_id>', methods=['DELETE'])
@admin_required
def delete_purchase_order(po_id):
    """Delete purchase order (admin only)"""
    try:
        po = PurchaseOrder.query.get(po_id)
        
        if not po:
            return jsonify({'error': 'Purchase order not found'}), 404
        
        po_ref = po.po_id
        db.session.delete(po)
        db.session.commit()
        
        log_activity('Purchase Order Deleted', f'Deleted PO: {po_ref}')
        
        return jsonify({'message': 'Purchase order deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders/<int:po_id>/receive', methods=['POST'])
@admin_required
def receive_purchase_order(po_id):
    """Mark purchase order as received and update raw material stock"""
    try:
        po = PurchaseOrder.query.get(po_id)
        
        if not po:
            return jsonify({'error': 'Purchase order not found'}), 404
        
        if po.status == 'received':
            return jsonify({'error': 'Purchase order already received'}), 400
        
        # Update PO status
        po.status = 'received'
        
        # Find and update raw material stock
        material = RawMaterial.query.filter_by(material_name=po.material_name).first()
        
        if material:
            material.current_stock += po.quantity
        else:
            # Create new material if it doesn't exist
            material_count = RawMaterial.query.count()
            material_id = f"MAT-{str(material_count + 1).zfill(4)}"
            
            material = RawMaterial(
                material_id=material_id,
                material_name=po.material_name,
                category=po.category,
                current_stock=po.quantity,
                min_level=0,  # Set default, should be updated later
                unit=po.unit,
                unit_price=po.unit_price,
                supplier=po.supplier
            )
            db.session.add(material)
        
        db.session.commit()
        
        log_activity('Purchase Order Received', f'Received PO: {po.po_id}')
        
        return jsonify({
            'message': 'Purchase order received successfully',
            'purchase_order': po.to_dict(),
            'material': material.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== ACTIVITY LOG ROUTES =====================

@app.route('/api/activity-logs', methods=['GET'])
@admin_required
def get_activity_logs():
    """Get activity logs (admin only)"""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        user_id = request.args.get('user_id', type=int)
        action = request.args.get('action')
        
        query = ActivityLog.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if action:
            query = query.filter(ActivityLog.action.ilike(f'%{action}%'))
        
        # Order by most recent first
        query = query.order_by(ActivityLog.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get user details for each log
        logs_with_users = []
        for log in pagination.items:
            log_dict = log.to_dict()
            if log.user_id:
                user = User.query.get(log.user_id)
                if user:
                    log_dict['user'] = {
                        'username': user.username,
                        'full_name': user.full_name,
                        'role': user.role
                    }
            logs_with_users.append(log_dict)
        
        return jsonify({
            'logs': logs_with_users,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== DASHBOARD & STATISTICS ROUTES =====================

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Order statistics
        total_orders = Order.query.count()
        pending_orders = Order.query.filter_by(status='yet-to-process').count()
        processing_orders = Order.query.filter_by(status='processing').count()
        completed_orders = Order.query.filter_by(status='completed').count()
        
        # Inventory statistics
        total_inventory = InventoryItem.query.count()
        low_stock_items = len([item for item in InventoryItem.query.all() if item.get_status() == 'low-stock'])
        out_of_stock_items = len([item for item in InventoryItem.query.all() if item.get_status() == 'out-of-stock'])
        
        # Raw materials statistics
        total_materials = RawMaterial.query.count()
        low_stock_materials = len([mat for mat in RawMaterial.query.all() if mat.get_status() == 'low-stock'])
        total_material_value = sum([mat.current_stock * mat.unit_price for mat in RawMaterial.query.all()])
        
        # Purchase order statistics
        total_purchase_orders = PurchaseOrder.query.count()
        pending_pos = PurchaseOrder.query.filter_by(status='ordered').count()
        total_po_value = sum([po.total_cost for po in PurchaseOrder.query.all()])
        
        # Recent activities
        recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
        activities_list = []
        for activity in recent_activities:
            activity_dict = activity.to_dict()
            if activity.user_id:
                user = User.query.get(activity.user_id)
                if user:
                    activity_dict['user'] = {
                        'username': user.username,
                        'full_name': user.full_name
                    }
            activities_list.append(activity_dict)
        
        # Order status distribution
        order_statuses = db.session.query(
            Order.status,
            db.func.count(Order.id)
        ).group_by(Order.status).all()
        
        status_distribution = {status: count for status, count in order_statuses}
        
        # Upcoming deadlines (next 7 days)
        today = datetime.utcnow().date()
        seven_days_later = today + timedelta(days=7)
        upcoming_deadlines = Order.query.filter(
            Order.deadline.between(today, seven_days_later),
            Order.status != 'completed'
        ).order_by(Order.deadline).all()
        
        return jsonify({
            'orders': {
                'total': total_orders,
                'pending': pending_orders,
                'processing': processing_orders,
                'completed': completed_orders,
                'status_distribution': status_distribution
            },
            'inventory': {
                'total': total_inventory,
                'low_stock': low_stock_items,
                'out_of_stock': out_of_stock_items
            },
            'raw_materials': {
                'total': total_materials,
                'low_stock': low_stock_materials,
                'total_value': round(total_material_value, 2)
            },
            'purchase_orders': {
                'total': total_purchase_orders,
                'pending': pending_pos,
                'total_value': round(total_po_value, 2)
            },
            'recent_activities': activities_list,
            'upcoming_deadlines': [order.to_dict() for order in upcoming_deadlines]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/charts/orders-by-status', methods=['GET'])
@jwt_required()
def get_orders_by_status_chart():
    """Get order distribution by status for charts"""
    try:
        order_statuses = db.session.query(
            Order.status,
            db.func.count(Order.id)
        ).group_by(Order.status).all()
        
        return jsonify({
            'labels': [status for status, _ in order_statuses],
            'data': [count for _, count in order_statuses]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/charts/inventory-status', methods=['GET'])
@jwt_required()
def get_inventory_status_chart():
    """Get inventory status distribution"""
    try:
        items = InventoryItem.query.all()
        
        status_count = {
            'in-stock': 0,
            'low-stock': 0,
            'out-of-stock': 0
        }
        
        for item in items:
            status = item.get_status()
            status_count[status] = status_count.get(status, 0) + 1
        
        return jsonify({
            'labels': list(status_count.keys()),
            'data': list(status_count.values())
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/charts/monthly-orders', methods=['GET'])
@jwt_required()
def get_monthly_orders_chart():
    """Get monthly order statistics"""
    try:
        # Get orders from last 12 months
        today = datetime.utcnow()
        twelve_months_ago = today - timedelta(days=365)
        
        orders = Order.query.filter(Order.created_at >= twelve_months_ago).all()
        
        # Group by month
        monthly_data = {}
        for order in orders:
            month_key = order.created_at.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = 0
            monthly_data[month_key] += 1
        
        # Sort by date
        sorted_months = sorted(monthly_data.keys())
        
        return jsonify({
            'labels': sorted_months,
            'data': [monthly_data[month] for month in sorted_months]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== REPORT ROUTES =====================

@app.route('/api/reports/orders', methods=['GET'])
@jwt_required()
def get_order_report():
    """Generate order report with filters"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        
        query = Order.query
        
        if start_date:
            query = query.filter(Order.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            query = query.filter(Order.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
        if status:
            query = query.filter_by(status=status)
        
        orders = query.all()
        
        # Calculate totals
        total_orders = len(orders)
        total_quantity = sum([order.quantity for order in orders])
        total_amount = sum([order.total_amount for order in orders if order.total_amount])
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'summary': {
                'total_orders': total_orders,
                'total_quantity': total_quantity,
                'total_amount': round(total_amount, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/inventory', methods=['GET'])
@jwt_required()
def get_inventory_report():
    """Generate inventory report"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = InventoryItem.query
        
        if category:
            query = query.filter_by(category=category)
        
        items = query.all()
        
        if status:
            items = [item for item in items if item.get_status() == status]
        
        # Calculate totals
        total_items = len(items)
        total_value = sum([item.current_stock * item.unit_cost for item in items if item.unit_cost])
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'summary': {
                'total_items': total_items,
                'total_value': round(total_value, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_order_report():
    """Generate purchase order report"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        supplier = request.args.get('supplier')
        
        query = PurchaseOrder.query
        
        if start_date:
            query = query.filter(PurchaseOrder.order_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(PurchaseOrder.order_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        if status:
            query = query.filter_by(status=status)
        if supplier:
            query = query.filter(PurchaseOrder.supplier.ilike(f'%{supplier}%'))
        
        purchase_orders = query.all()
        
        # Calculate totals
        total_pos = len(purchase_orders)
        total_cost = sum([po.total_cost for po in purchase_orders])
        
        return jsonify({
            'purchase_orders': [po.to_dict() for po in purchase_orders],
            'summary': {
                'total_purchase_orders': total_pos,
                'total_cost': round(total_cost, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== UTILITY ROUTES =====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all unique categories"""
    try:
        inventory_categories = db.session.query(InventoryItem.category).distinct().all()
        material_categories = db.session.query(RawMaterial.category).distinct().all()
        
        all_categories = list(set(
            [cat[0] for cat in inventory_categories] + 
            [cat[0] for cat in material_categories]
        ))
        
        return jsonify({
            'categories': sorted(all_categories)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all unique suppliers"""
    try:
        inventory_suppliers = db.session.query(InventoryItem.supplier).distinct().all()
        material_suppliers = db.session.query(RawMaterial.supplier).distinct().all()
        po_suppliers = db.session.query(PurchaseOrder.supplier).distinct().all()
        
        all_suppliers = list(set(
            [sup[0] for sup in inventory_suppliers if sup[0]] + 
            [sup[0] for sup in material_suppliers if sup[0]] +
            [sup[0] for sup in po_suppliers if sup[0]]
        ))
        
        return jsonify({
            'suppliers': sorted(all_suppliers)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'error': 'Bad request'}), 400


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    """Handle unauthorized access"""
    return jsonify({'error': 'Missing or invalid token'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    """Handle invalid token"""
    return jsonify({'error': 'Invalid token'}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token"""
    return jsonify({'error': 'Token has expired'}), 401


# ===================== DATABASE INITIALIZATION =====================

def init_db():
    """Initialize database with tables and default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Create default admin user
            admin = User(
                user_id='USR-0001',
                username='admin',
                email='admin@factory.com',
                full_name='System Administrator',
                role='admin',
                department='Management',
                status='active'
            )
            admin.set_password('password')
            
            # Create default manager user
            manager = User(
                user_id='USR-0002',
                username='manager',
                email='manager@factory.com',
                full_name='Factory Manager',
                role='manager',
                department='Operations',
                status='active'
            )
            manager.set_password('manager123')
            
            db.session.add(admin)
            db.session.add(manager)
            db.session.commit()
            
            print("\n" + "="*60)
            print("✓ Database initialized with default users")
            print("="*60)
            print("  Admin User:")
            print("    Username: admin")
            print("    Password: password")
            print("  Manager User:")
            print("    Username: manager")
            print("    Password: manager123")
            print("="*60 + "\n")
        else:
            # Database exists - check and update manager password if needed
            manager = User.query.filter_by(username='manager').first()
            if manager:
                # Update manager password to manager123 if it's not already set
                # Test with the old password first to see if we need to update
                if manager.check_password('password') or not manager.check_password('manager123'):
                    manager.set_password('manager123')
                    db.session.commit()
                    print("✓ Manager password updated to 'manager123'")
            else:
                # Manager doesn't exist, create it
                manager = User(
                    user_id='USR-0002',
                    username='manager',
                    email='manager@factory.com',
                    full_name='Factory Manager',
                    role='manager',
                    department='Operations',
                    status='active'
                )
                manager.set_password('manager123')
                db.session.add(manager)
                db.session.commit()
                print("✓ Manager user created with password 'manager123'")
            
            print("✓ Database already initialized")


@app.route('/api/init-db', methods=['POST'])
def initialize_database():
    """Endpoint to initialize database (use only once)"""
    try:
        init_db()
        return jsonify({'message': 'Database initialized successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/seed-data', methods=['POST'])
@admin_required
def seed_sample_data():
    """Seed database with sample data for testing (admin only)"""
    try:
        # Sample inventory items
        if InventoryItem.query.count() == 0:
            sample_items = [
                InventoryItem(
                    item_code='ITM-0001',
                    item_name='Finished Product A',
                    category='Finished Goods',
                    current_stock=150,
                    min_level=50,
                    max_level=500,
                    unit='pieces',
                    unit_cost=25.50,
                    supplier='ABC Manufacturing',
                    location='Warehouse A',
                    description='High-quality finished product A'
                ),
                InventoryItem(
                    item_code='ITM-0002',
                    item_name='Finished Product B',
                    category='Finished Goods',
                    current_stock=30,
                    min_level=50,
                    max_level=300,
                    unit='pieces',
                    unit_cost=35.75,
                    supplier='XYZ Corp',
                    location='Warehouse B',
                    description='Premium finished product B'
                ),
                InventoryItem(
                    item_code='ITM-0003',
                    item_name='Component X',
                    category='Components',
                    current_stock=200,
                    min_level=100,
                    max_level=1000,
                    unit='pieces',
                    unit_cost=5.25,
                    supplier='Component Supplies Ltd',
                    location='Warehouse C',
                    description='Standard component X'
                )
            ]
            db.session.bulk_save_objects(sample_items)
        
        # Sample raw materials
        if RawMaterial.query.count() == 0:
            sample_materials = [
                RawMaterial(
                    material_id='MAT-0001',
                    material_name='Steel Sheets',
                    category='Metals',
                    current_stock=500,
                    min_level=100,
                    unit='kg',
                    unit_price=15.00,
                    supplier='Steel Supplies Inc',
                    description='High-grade steel sheets'
                ),
                RawMaterial(
                    material_id='MAT-0002',
                    material_name='Plastic Pellets',
                    category='Plastics',
                    current_stock=200,
                    min_level=150,
                    unit='kg',
                    unit_price=8.50,
                    supplier='Polymer Solutions',
                    description='Industrial plastic pellets'
                ),
                RawMaterial(
                    material_id='MAT-0003',
                    material_name='Aluminum Bars',
                    category='Metals',
                    current_stock=300,
                    min_level=100,
                    unit='kg',
                    unit_price=22.00,
                    supplier='Metal Works Co',
                    description='Extruded aluminum bars'
                )
            ]
            db.session.bulk_save_objects(sample_materials)
        
        # Sample orders
        if Order.query.count() == 0:
            admin = User.query.filter_by(username='admin').first()
            sample_orders = [
                Order(
                    order_id='ORD-0001',
                    customer_name='Acme Corporation',
                    product='Finished Product A',
                    quantity=100,
                    unit_price=30.00,
                    total_amount=3000.00,
                    status='processing',
                    priority='high',
                    deadline=(datetime.utcnow() + timedelta(days=7)).date(),
                    special_instructions='Rush order - handle with care',
                    created_by=admin.id
                ),
                Order(
                    order_id='ORD-0002',
                    customer_name='Global Industries',
                    product='Finished Product B',
                    quantity=50,
                    unit_price=40.00,
                    total_amount=2000.00,
                    status='yet-to-process',
                    priority='medium',
                    deadline=(datetime.utcnow() + timedelta(days=14)).date(),
                    created_by=admin.id
                )
            ]
            db.session.bulk_save_objects(sample_orders)
        
        # Sample purchase orders
        if PurchaseOrder.query.count() == 0:
            admin = User.query.filter_by(username='admin').first()
            sample_pos = [
                PurchaseOrder(
                    po_id='PO-0001',
                    material_name='Steel Sheets',
                    category='Metals',
                    quantity=1000,
                    unit='kg',
                    unit_price=15.00,
                    total_cost=15000.00,
                    supplier='Steel Supplies Inc',
                    order_date=datetime.utcnow().date(),
                    expected_delivery=(datetime.utcnow() + timedelta(days=10)).date(),
                    status='ordered',
                    notes='Quarterly steel order',
                    created_by=admin.id
                )
            ]
            db.session.bulk_save_objects(sample_pos)
        
        db.session.commit()
        
        return jsonify({'message': 'Sample data seeded successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===================== FRONTEND ROUTES =====================

@app.route('/')
def serve_frontend():
    """Serve the HTML frontend"""
    return send_from_directory('.', '1.html')

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'application': 'Factory Management System API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'auth': '/api/auth/login',
            'users': '/api/users',
            'orders': '/api/orders',
            'inventory': '/api/inventory',
            'raw_materials': '/api/raw-materials',
            'purchase_orders': '/api/purchase-orders',
            'dashboard': '/api/dashboard/stats',
            'health': '/api/health'
        },
        'documentation': 'See README.md for full API documentation'
    }), 200


# ===================== MAIN ENTRY POINT =====================

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    print("\n" + "="*60)
    print("🏭 Factory Management System - Backend Server")
    print("="*60)
    print(f"🚀 Server starting on http://localhost:{port}")
    print(f"📊 Environment: {'Development' if debug else 'Production'}")
    print(f"🗄️  Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )