# main.py
from flask import flash, render_template, request, redirect,url_for
from flask_bootstrap import Bootstrap

from quartzapp import app
from quartzdb_setup import init_db, db_session
from quartzmodels import MicronPart
from quartzmodels import QuartzSerialNumber
from quartzmodels import User
from quartznewforms import QuartzForm
from quartznewforms import QuartzSearchForm
from quartznewforms import LoginForm
from quartznewforms import RegisterForm
from quartztable import Results
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('quartzindex'))

        return '<h1> Invalid username or password</h1>'


    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return '<h1> New User has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/quartzindex', methods=['GET', 'POST'])
def quartzindex():
    search = QuartzSearchForm(request.form)
    if request.method == 'POST':
        return searchresults(search)

    return render_template('quartzindex.html', form=search)

@app.route('/results/')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(MicronPart)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', table=table)


@app.route('/new_quartz', methods=['GET', 'POST'])
def new_quartz():
    """
    Add a new album
    """
    form = QuartzForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the album
        micronpart = MicronPart()
        save_changes(micronpart, form, new=True)
        flash('MicronPart created successfully!')
        return redirect('/')

    return render_template('new_quartz.html', form=form)


def save_changes(micronpart, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    quartzserialnumber = QuartzSerialNumber()
    quartzserialnumber.name = form.quartzserialnumber.data
    micronpart.title = form.title.data
    micronpart.quartzserialnumber = quartzserialnumber
    micronpart.quartz_type = form.quartz_type.data
    micronpart.installation_date = form.installation_date.data
    micronpart.toolname = form.toolname.data
    micronpart.quartz_condition_type = form.quartz_condition_type.data

    if new:
        # Add the new quartz to the database
        db_session.add(micronpart)

    # commit the data to the database
    db_session.commit()




@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(MicronPart).filter(
        MicronPart.id == id)
    micronpart = qry.first()

    if micronpart:
        form = QuartzForm(formdata=request.form, obj=micronpart)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(micronpart, form)
            flash('Quartz updated successfully!')
            return redirect('/')
        return render_template('edit_quartz.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/results')
def searchresults(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'QuartzSerialNumber':
            qry = db_session.query(MicronPart, QuartzSerialNumber).filter(
                QuartzSerialNumber.id == MicronPart.quartzserialnumber_id).filter(
                QuartzSerialNumber.name.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'QuartzType':
            qry = db_session.query(MicronPart).filter(
                MicronPart.quartz_type.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'ToolName':
            qry = db_session.query(MicronPart).filter(
                MicronPart.toolname.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(MicronPart)
            results = qry.all()
    else:
        qry = db_session.query(MicronPart)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id, micronpart=None):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(MicronPart).filter(
        MicronPart.id==id)
    micronpart = qry.first()

    if micronpart:
        form = QuartzForm(formdata=request.form, obj=micronpart)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(micronpart)
            db_session.commit()

            flash('MicronPart deleted successfully!')
            return redirect('/')
        return render_template('delete_quartz.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


if __name__ == '__main__':
    app.run(debug=True)