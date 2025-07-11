from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_wtf.file import FileAllowed



class RegisterForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired()], render_kw={'placeholder': 'Giorgi Sauri'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'mods@gmail.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    interest_area = SelectField('Interest area', choices=[('creating', 'Creating Mods'), ('sell', 'Buying mods'), ('other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Enter product name'})
    price = DecimalField('Price (USD)', validators=[DataRequired(), NumberRange(min=0.01)], places=2, filters=[lambda x: float(x) if x not in (None, '') else None], render_kw={'placeholder': '0.00'})
    mod_type = SelectField('Mod Type', choices=[('Vehicle Mod', 'Vehicle Mod'), ('Map Mod', 'Map Mod'), ('Other Mod', 'Other Mod')], validators=[DataRequired()])
    link = StringField('Mod Link', render_kw={'placeholder': 'https://example.com/my-mod'})
    image = FileField('Mod Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add Product')


class DeleteForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Delete')


