# Task Manager API

A simple Flask-based task management API deployed on Railway.

## API Endpoints

### Users
- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/<id>` - Get user details
- `DELETE /users/<id>` - Delete a user

### Tasks
- `GET /tasks` - List all tasks
- `GET /users/<user_id>/tasks` - Get user's tasks
- `POST /users/<user_id>/tasks` - Create a task
- `GET /tasks/<id>` - Get task details
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

### Health
- `GET /health` - Health check endpoint

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py