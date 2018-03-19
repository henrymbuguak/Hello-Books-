from flask import Flask, render_template, request, flash, url_for, redirect
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from flask_mail import Mail
from models import User, Role, Language, Genre, Book, Author

mail = Mail()
# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'bcrypt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_POST_LOGIN_VIEW'] = '/dashboard'
app.config['SECURITY_POST_REGISTER_VIEW'] = '/dashboard'
mail.init_app(app)

# Setup Flask-Security
use_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, use_datastore)

# Create a user for test with
# @app.before_first_request
# def create_user():
#     init_db()
#     use_datastore.create_user(username='henry', email='henrymbuguak@gmail.com', password='password')
#     db_session.commit()


# views
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# admins route
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    books = Book.query.all()
    return render_template('/admins/index.html', books=books)


@app.route('/admin/dashboard/book/add', methods=['GET', 'POST'])
@login_required
def admin_dashboard_book_add():
    genres = Genre.query.all()
    languages = Language.query.all()
    authors = Author.query.all()
    if request.form:
        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            genre=request.form.get('genre'),
            language=request.form.get('language'),
            summary=request.form.get('summary'),
        )
        db_session.add(book)
        db_session.commit()
        flash('Book successfully added')
        return redirect(url_for('admin_dashboard'))
    return render_template('/admins/book_add.html', genres=genres, languages=languages, authors=authors)


@app.route('/admin/dashboard/language')
@login_required
def admin_dashboard_languages():
    languages = Language.query.all()
    return render_template('/admins/language.html', languages=languages)


@app.route('/admin/dashboard/genre/add', methods=['GET', 'POST'])
@login_required
def admin_dashboard_genre_add():
    if request.form:
        genre = Genre(name=request.form.get('name'))
        db_session.add(genre)
        db_session.commit()
        flash('Genre successfully added')
        return redirect(url_for('admin_dashboard_genre'))
    return render_template('/admins/genre_add.html')


@app.route('/admin/dashboard/genre/edit/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_genre_edit(id):
    genre = Genre.query.filter_by(id=id).first()
    return render_template('/admins/genre_edit.html', genre=genre)


@app.route('/admin/dashboard/genre/update/<int:id>', methods=['POST'])
@login_required
def admin_dashboard_genre_update(id):
    genre_update = request.form.get('name')
    genre = Genre.query.filter_by(id=id).first()
    genre.name = genre_update
    db_session.commit()
    flash('Genre successfully updated')
    return redirect(url_for('admin_dashboard_genre'))


@app.route('/admin/dashboard/genre/delete/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_genre_delete(id):
    genre = Genre.query.filter_by(id=id).first()
    db_session.delete(genre)
    db_session.commit()
    flash('Genre successfully deleted')
    return redirect(url_for('admin_dashboard_genre'))


@app.route('/admin/dashboard/language/add', methods=['GET', 'POST'])
@login_required
def admin_dashboard_language_add():
    if request.form:
        language = Language(name=request.form.get('name'))
        db_session.add(language)
        db_session.commit()
        flash('Language successfully added')
        return redirect(url_for('admin_dashboard_languages'))
    return render_template('/admins/language_add.html')


@app.route('/admin/dashboard/language/edit/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_language_edit(id):
    language = Language.query.filter_by(id=id).first()
    return render_template('/admins/language_edit.html', language=language)


@app.route('/admin/dashboard/language/update/<int:id>', methods=['POST'])
@login_required
def admin_dashboard_language_update(id):
    language_update = request.form.get('name')
    language = Language.query.filter_by(id=id).first()
    language.name = language_update
    db_session.commit()
    flash('Language successfully updated')
    return redirect(url_for('admin_dashboard_languages'))


@app.route('/admin/dashboard/language/delete/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_language_delete(id):
    language = Language.query.filter_by(id=id).first()
    db_session.delete(language)
    db_session.commit()
    flash('Language successfully deleted')
    return redirect(url_for('admin_dashboard_languages'))


@app.route('/admin/dashboard/genre')
@login_required
def admin_dashboard_genre():
    genres = Genre.query.all()
    return render_template('/admins/genre.html', genres=genres)


@app.route('/admin/dashboard/author')
@login_required
def admin_dashboard_author():
    authors = Author.query.all()
    return render_template('/admins/author.html', authors=authors)


@app.route('/admin/dashboard/author/add', methods=['GET', 'POST'])
@login_required
def admin_dashboard_author_add():
    if request.form:
        author = Author(first_name=request.form.get('first_name'), last_name=request.form.get('last_name'))
        db_session.add(author)
        db_session.commit()
        flash('Author successfully added')
        return redirect(url_for('admin_dashboard_author'))
    return render_template('/admins/author_add.html')


@app.route('/admin/dashboard/author/edit/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_author_edit(id):
    author = Author.query.filter_by(id=id).first()
    return render_template('/admins/author_edit.html', author=author)


@app.route('/admin/dashboard/author/update/<int:id>', methods=['POST'])
@login_required
def admin_dashboard_author_update(id):
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    author = Author.query.filter_by(id=id).first()
    author.first_name = first_name
    author.last_name = last_name
    db_session.commit()
    flash('Author successfully updated')
    return redirect(url_for('admin_dashboard_author'))


@app.route('/admin/dashboard/author/delete/<int:id>', methods=['GET'])
@login_required
def admin_dashboard_author_delete(id):
    author = Author.query.filter_by(id=id).first()
    db_session.delete(author)
    db_session.commit()
    flash('Author successfully deleted')
    return redirect(url_for('admin_dashboard_author'))



if __name__ == '__main__':
    app.run()