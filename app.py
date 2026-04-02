from flask import Flask, request, jsonify
from config import config
from models import db, User, Task
import os

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
    
    # ========== ROUTES ==========
    
    @app.route('/')
    def home():
        """Home endpoint - API information"""
        return jsonify({
            'message': 'Welcome to Task Manager API',
            'version': '1.0.0',
            'endpoints': {
                'users': '/users',
                'users_detail': '/users/<id>',
                'tasks': '/tasks',
                'tasks_detail': '/tasks/<id>',
                'user_tasks': '/users/<user_id>/tasks',
                'health': '/health'
            }
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint for Railway monitoring"""
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if db.engine else 'disconnected'
        })
    
    # ========== USER ROUTES ==========
    
    @app.route('/users', methods=['GET'])
    def get_users():
        """Get all users"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    
    @app.route('/users', methods=['POST'])
    def create_user():
        """Create a new user"""
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email are required'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """Get a specific user by ID"""
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """Delete a user and all their tasks"""
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'})
    
    # ========== TASK ROUTES ==========
    
    @app.route('/tasks', methods=['GET'])
    def get_all_tasks():
        """Get all tasks (across all users)"""
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    
    @app.route('/users/<int:user_id>/tasks', methods=['GET'])
    def get_user_tasks(user_id):
        """Get all tasks for a specific user"""
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify([task.to_dict() for task in tasks])
    
    @app.route('/users/<int:user_id>/tasks', methods=['POST'])
    def create_task(user_id):
        """Create a new task for a user"""
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Task title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            user_id=user_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    
    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """Get a specific task"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.to_dict())
    
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """Update a task"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        
        return jsonify(task.to_dict())
    
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """Delete a task"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'})
    
    return app

# Create app instance for Railway (uses production config on Railway)
if __name__ == '__main__':
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    # Get port from Railway (or default to 5000)
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port)