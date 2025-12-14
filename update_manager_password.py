#!/usr/bin/env python3
"""
Script to update manager password in existing database
Run this if your database already exists and you need to update the manager password
"""

from app import app, db, User

def update_manager_password():
    """Update manager user password to manager123"""
    with app.app_context():
        manager = User.query.filter_by(username='manager').first()
        
        if manager:
            manager.set_password('manager123')
            db.session.commit()
            print("✓ Manager password updated successfully!")
            print(f"  Username: {manager.username}")
            print(f"  New Password: manager123")
        else:
            print("✗ Manager user not found in database!")
            print("  Run init_db() to create default users first.")

if __name__ == "__main__":
    update_manager_password()

