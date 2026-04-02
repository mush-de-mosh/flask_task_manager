#!/usr/bin/env python
"""Script to populate the database with sample data"""

import os
from app import create_app
from models import db, User, Task

def seed_database():
    """Add sample users and tasks to the database"""
    
    # Use production config if DATABASE_URL exists, otherwise development
    env = 'production' if os.environ.get('DATABASE_URL') else 'development'
    app = create_app(env)
    
    with app.app_context():
        # Check if database is already seeded
        if User.query.count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample users
        users = [
            User(username="alice_wonder", email="alice@example.com"),
            User(username="bob_builder", email="bob@example.com"),
            User(username="carol_danvers", email="carol@example.com"),
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f"Added {len(users)} users")
        
        # Create sample tasks for each user
        tasks_data = [
            (users[0], "Complete project report", "Write the final report for the PaaS assignment", False),
            (users[0], "Review pull requests", "Check team members' code contributions", True),
            (users[0], "Deploy to Railway", "Get the app up and running on Railway", False),
            
            (users[1], "Buy groceries", "Milk, eggs, bread, and coffee", False),
            (users[1], "Schedule dentist appointment", "Call Dr. Smith's office", True),
            
            (users[2], "Study for exam", "Review chapters 5-8 for Wednesday", False),
            (users[2], "Update resume", "Add recent project experience", False),
            (users[2], "Pay electricity bill", "Due by the 15th", True),
        ]
        
        tasks = []
        for user, title, description, completed in tasks_data:
            task = Task(
                title=title,
                description=description,
                completed=completed,
                user_id=user.id
            )
            tasks.append(task)
        
        db.session.add_all(tasks)
        db.session.commit()
        print(f"Added {len(tasks)} tasks")
        
        print("\n=== Database Seeded Successfully ===")
        print(f"Users: {User.query.count()}")
        print(f"Tasks: {Task.query.count()}")
        
        # Print summary
        print("\n--- Sample Data Summary ---")
        for user in User.query.all():
            print(f"\nUser: {user.username} ({user.email})")
            for task in user.tasks:
                status = "✓" if task.completed else "○"
                print(f"  {status} {task.title}")

if __name__ == "__main__":
    seed_database()