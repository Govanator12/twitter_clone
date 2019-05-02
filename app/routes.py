from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, LoginForm, RegisterForm, ContactForm, PostForm
from app.models import Title, Contact, Post, User
from flask_login import current_user

@app.route('/')
@app.route('/index')
def index():
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

    header = Title.query.get(1).title

    return render_template('index.html', title='Home', products=products, header=header)


@app.route('/title', methods=['GET', 'POST'])
def title():
    form = TitleForm()

    if form.validate_on_submit():
        header = form.title.data

        data = Title.query.get(1)
        data.title = header

        # add to session and commit
        db.session.add(data)
        db.session.commit()

        flash(f'You have changed the title to {header}')
        return redirect(url_for('index'))

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

    # check to see if the user is already logged in, if so send to index
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = form.age.data,
            bio = form.bio.data
        )

        # call set_password to create hash
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'Thanks for registering, an e-mail confirmation has been sent to {form.email.data}')
        return redirect(url_for('login'))

    return render_template('form.html', title='Register', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact = Contact(
                name = form.name.data,
                email = form.email.data,
                message = form.message.data
            )

            db.session.add(contact)
            db.session.commit()

            flash(f'Thanks for your submission, we will contact you shortly. A copy of your message has been sent to {form.email.data}')
            return redirect(url_for('index'))
        except:
            flash('Sorry, your submission did not go through')
            return redirect(url_for('contact'))

    return render_template('form.html', form=form, title='Contact Us')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = PostForm()

    posts = Post.query.all()

    if form.validate_on_submit():
        post=Post(tweet=form.tweet.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('profile.html', title='Profile', form=form, posts=posts)
