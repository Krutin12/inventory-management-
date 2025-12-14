#!/usr/bin/env python3
"""
Quick script to fix manager password in existing database
"""

from app import app, db, User

with app.app_context():
    print("Checking manager user...")
    manager = User.query.filter_by(username='manager').first()
    
    if manager:
        print(f"Found manager user: {manager.username}")
        print(f"Current role: {manager.role}")
        print(f"Current status: {manager.status}")
        
        # Update password to manager123
        manager.set_password('manager123')
        db.session.commit()
        
        # Verify the password was set
        if manager.check_password('manager123'):
            print("\n✅ SUCCESS! Manager password updated to 'manager123'")
            print(f"   Username: {manager.username}")
            print(f"   Password: manager123")
        else:
            print("\n❌ ERROR: Password verification failed!")
    else:
        print("❌ Manager user not found!")
        print("Creating manager user...")
        
        # Check if USR-0002 already exists
        existing = User.query.filter_by(user_id='USR-0002').first()
        if existing:
            print(f"   User ID USR-0002 already exists with username: {existing.username}")
        else:
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
            print("✅ Manager user created successfully!")
            print(f"   Username: manager")
            print(f"   Password: manager123")

