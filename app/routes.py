from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, LoginForm, RegisterForm, ContactForm

@app.route('/')
@app.route('/index')
@app.route('/index/<header>', methods=['GET'])
def index(header=''):
    products = [
        {
            'id': 1001,
            'title': 'Soap',
            'price': 3.98,
            'desc': 'Very clean soapy soap, descriptive text'
        },
        {
            'id': 1002,
            'title': 'Grapes',
            'price': 4.56,
            'desc': 'A bundle of grapey grapes, yummy'
        },
        {
            'id': 1003,
            'title': 'Pickles',
            'price': 5.67,
            'desc': 'IM PICKLE RIIIIIIIICK'
        },
        {
            'id': 1004,
            'title': 'Juice',
            'price': 2.68,
            'desc': 'Yummy orange juice'
        }
    ]

    return render_template('index.html', title='Home', products=products, header=header)


@app.route('/title', methods=['GET', 'POST'])
def title():
    form = TitleForm()

    if form.validate_on_submit():
        header = form.title.data

        flash(f'You have changed the title to {header}')
        return redirect(url_for('index', header=header))

    return render_template('form.html', title='Change Title', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Successfully Logged In')
        return redirect(url_for('index'))
    return render_template('form.html', title='Login', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        flash(f'Thanks for registering, an e-mail confirmation has been sent to {form.email.data}')
        return redirect(url_for('login'))

    return render_template('form.html', title='Register', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash(f'Thanks for your submission, we will contaact you shortly. A copy of your message has been sent to {form.email.data}')
        return redirect(url_for('index'))

    return render_template('form.html', form=form, title='Contact Us')
