from flask_migrate import Migrate
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, os
from ext import app, db, login_manager
from forms import RegisterForm, LoginForm, ProductForm
from models import User, Product, get_user_by_email, get_user_by_username
from ext import Flask

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash("Wrong password or email", "danger")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if get_user_by_email(form.email.data) or get_user_by_username(form.full_name.data):
            flash("User is already registered.")
            return redirect(url_for('register'))

        is_admin = form.email.data == "admin@example.com"
        hashed_password = generate_password_hash("75675757")

        new_user = User(
    username=form.full_name.data,
    email=form.email.data,
    password=hashed_password,
    is_admin=is_admin
)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', current_user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/marketplace')
def marketplace():
    mods = [
        {
            "title": "Bmw M4 G82",
            "type": "Vehicle Mod",
            "price": "3.00$",
            "sold": 35,
            "daily": 2,
            "image": "1.jpg",
            "link": "https://www.modland.net/beamng.drive-mods/cars/2020-2025-bmw-m4-g82g83-comp-cs-csl-kith-adro-and-more.html"
        },
        {
            "title": "Los Santos",
            "type": "Map Mod",
            "price": "11.50$",
            "sold": 27,
            "daily": 1,
            "image": "2.jpg",
            "link": "https://www.modland.net/beamng.drive-mods/maps/gta-v-los-santos-map-for-beamng-2.html"
        },
        {
            "title": "Bmw X5M F95",
            "type": "Vehicle Mod",
            "price": "5.99$",
            "sold": 18,
            "daily": 1,
            "image": "3.jpg",
            "link": "https://www.modland.net/beamng.drive-mods/cars/bmw-x5-f95-3.html"
        }
    ]
    all_products = Product.query.all()
    form = ProductForm()
    return render_template("marketplace.html", mods=mods, products=all_products, current_user=current_user, form=form)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'uploads/{filename}'
        else:
            image_url = 'images.png'

        price = float(form.price.data)
        new_product = Product(
            title=form.name.data,
            price=price,
            type=form.mod_type.data,
            link=form.link.data,
            image=image_url,
            author=current_user.username
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('marketplace'))

    return render_template('add_product.html', form=form, product=None, current_user=current_user)

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if current_user.username != product.author and not current_user.is_admin:
        return "Access Denied", 403

    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.title = form.name.data
        product.price = float(form.price.data)
        product.type = form.mod_type.data
        product.link = form.link.data

        image = form.image.data
        if image:
            filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            product.image = f'uploads/{filename}'

        db.session.commit()
        return redirect(url_for('marketplace'))

    return render_template('add_product.html', form=form, product=product, current_user=current_user)

@app.route('/delete_product/<id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return "Product not found", 404

    if current_user.username != product.author and not current_user.is_admin:
        return "Access Denied", 403

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('marketplace'))

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return "Access Denied", 403
    return render_template('admin.html', current_user=current_user)

@app.route('/debug_users')
def debug_users():
    users = User.query.all()
    output = []
    for u in users:
        output.append(f"User: {u.username}, Password stored: {u.password}")
    return "<br>".join(output)