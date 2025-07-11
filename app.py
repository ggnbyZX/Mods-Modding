from ext import app


from routes import home, howitworks, login, register, logout, gallery, profile, marketplace, add_product, edit_product, delete_product, admin_panel, debug_users
app.run(debug=True, host='0.0.0.0')
