from ext import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.password = generate_password_hash("75675757")
        print("Admin password updated.")
    else:
        admin = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("75675757"),
            is_admin=True
        )
        db.session.add(admin)
        print("Admin user created.")

    new_user = User.query.filter_by(username='newuser').first()
    if new_user:
        new_user.password = generate_password_hash("75675757")
        print("User password updated.")
    else:
        new_user = User(
            username="newuser",
            email="newuser@example.com",
            password=generate_password_hash("75675757"),
            is_admin=False
        )
        db.session.add(new_user)
        print("New user created.")

    users = User.query.all()
    for user in users:
        pw = user.password
        if not (pw.startswith("pbkdf2:") or pw.startswith("argon2$") or pw.startswith("bcrypt$")):
            user.password = generate_password_hash(pw)
            print(f"Password for user {user.username} hashed.")

    db.session.commit()
