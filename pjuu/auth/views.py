# 3rd party imports
from flask import (abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug import check_password_hash, generate_password_hash

# Pjuu imports
from pjuu import app, db
from pjuu.lib.mail import send_mail
from pjuu.users.models import User

# Package imports
from .backend import (authenticate, current_user, is_safe_url, login,
                      logout, create_account, activate_signer, forgot_signer,
                      email_signer, generate_token, check_token)
from .decorators import anonymous_required, login_required
from .forms import (ForgotForm, LoginForm, ResetForm, SignupForm,
                    PasswordChangeForm, EmailChangeForm)


@app.context_processor
def inject_user():
    """
    Injects `current_user` into the Jinja environment
    """
    return dict(current_user=current_user)


@app.route('/signin', methods=['GET', 'POST'])
@anonymous_required
def signin():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # Handles the passing of the next argument to the login view
        redirect_url = request.values.get('next', None)
        if not redirect_url or not is_safe_url(redirect_url):
            redirect_url=url_for('feed')
        if form.validate():
            username = form.username.data
            password = form.password.data
            # Calls authenticate from backend.py
            user = authenticate(username, password)
            if user is not None:
                if not user.active:
                    flash('Please activate your account. Check your e-mails',
                          'warning')
                elif user.banned:
                    flash('Your account has been banned. Naughty boy',
                          'warning')
                else:
                    login(user)
                    return redirect(redirect_url)
            else:
                flash('Invalid user name or password', 'error')
        else:
            flash('Invalid user name or password', 'error')
    return render_template('auth/signin.html', form=form)


@app.route('/signout')
def signout():
    if current_user:
        logout()
        flash('Successfully logged out!', 'success')
    return redirect(url_for('signin'))


@app.route('/signup', methods=['GET', 'POST'])
@anonymous_required
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # User successfully signed up, create an account
            new_user = create_account(form.username.data, form.email.data,
                                      form.password.data)
            if new_user:
                token = generate_token(activate_signer,
                                       {'username': new_user.username})
                send_mail('Activation', [new_user.email],
                          text_body=render_template('auth/activate.email.txt',
                                                    token=token),
                          html_body=render_template('auth/activate.email.html',
                                                    token=token))
                flash('Yay! You\'ve signed up. Please check your e-mails to activate your account.', 'success')
                return redirect(url_for('signin'))
        # This will fire if the form is invalid
        flash('Oh no! There are errors in your signup form', 'error')
    return render_template('auth/signup.html', form=form)


@app.route('/activate/<token>')
@anonymous_required
def activate(token):
    # Attempt to get the data from the token
    data = check_token(activate_signer, token)
    if data is not None:
        try:
            # Attempt to activate the users account
            user = User.query.filter_by(username=data['username']).first()
            user.active = True
            db.session.add(user)
            db.session.commit()
            # If we have got to this point. Send a welcome e-mail :)
            send_mail('Welcome', user.email,
                      text_body=render_template('auth/welcome.email.txt'),
                      html_body=render_template('auth/welcome.email.html'))
            flash('Youre account has now been activated.', 'success')
        except:
            # Something went wrong. Show them the broken Otter.
            db.session.rollback()
            abort(500)
    else:
        # The token is either out of date or has been tampered with
        flash('Invalid token.', 'error')
        return redirect(url_for('signup'))
    # Go to signin if successful
    return redirect(url_for('signin'))


@app.route('/forgot', methods=['GET', 'POST'])
@anonymous_required
def forgot():
    form = ForgotForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        #TODO: Make this a function. It checks for users
        if '@' in username:
            user = User.query.filter(User.email.ilike(username)).first()
        else:
            user = User.query.filter(User.username.ilike(username)).first()
        if user:
            token = generate_token(forgot_signer,
                                   {'username': user.username})
            send_mail('Password reset', [user.email],
                      text_body=render_template('auth/forgot.email.txt',
                                                token=token),
                      html_body=render_template('auth/forgot.email.html',
                                                token=token))
        flash('If we have you user record we have e-mailed a reset link too you',
              'information')
        return redirect(url_for('signin'))
    return render_template('auth/forgot.html', form=form)


@app.route('/reset/<token>', methods=['GET', 'POST'])
@anonymous_required
def password_reset(token):
    form = ResetForm(request.form)
    data = check_token(forgot_signer, token.encode)
    if data is not None:
        try:
            user = User.query.filter_by(username=data['username']).first()
        except:
            # Something went wrong
            db.session.rollback()
            abort(500)
    else:
        flash('Invalid token.', 'error')
        return redirect(url_for('forgot'))
    return render_template('auth/reset.html', form=form)


@app.route('/change_password', method['POST'])
@login_required
def password_change():
    pass


@app.route('/change_email', methods=['POST'])
@login_required
def email_change():
    pass
