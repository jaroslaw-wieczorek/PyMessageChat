from flask import session, render_template, request, Flask
from . import main
from app.pycode.forms import LoginForm

app = Flask(__name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['login'] = form.login.data
        session['password'] = form.password.data
        return #TO_DO przekierowanie
    elif request.method == 'GET':
        form.login.data = session.get('login', '')
        form.password.data = session.get('password', '')
    return render_template('login.html', form=form)
