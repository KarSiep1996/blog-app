from flask import render_template, request, session, flash, redirect, url_for
from blog import app, mail
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools
from flask_mail import Mail, Message

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

def create_edit_entry(entry_id=0):
    errors = None
    if entry_id == 0:
        form = EntryForm()
    else:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    if request.method == 'POST':
            if form.validate_on_submit():
                if entry_id == 0:
                    entry = Entry(
                        title=form.title.data,
                        body=form.body.data,
                        is_published=form.is_published.data
                    )
                    db.session.add(entry)
                else:
                    form.populate_obj(entry)
                db.session.commit()
            else:
                errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/about-me")
def about_me():
    return render_template("about_me.html")

@app.route("/contact-me", methods=['GET', 'POST'])
def contact_me():
    return render_template("contact_me.html")

@app.route('/send-email/', methods=['POST', 'GET'])
def send_email():
    data=request.args
    message_title = "Message from " + data['name']+ ' ' + data['surname'] + ", " + data['email']
    msg = Message(message_title, sender = 'ancymonka1996@gmail.com', recipients = ['ancymonka1996@gmail.com'])
    msg.body = data['message']
    mail.send(msg)
    return render_template("about_me.html")

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return create_edit_entry()


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return create_edit_entry(entry_id)

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route('/search/')
def search():
    results = []
    search_query = request.args.get("q", "")
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    for post in all_posts:
        if search_query in post.title:
            results = results + [post] 
    return render_template("search.html", results = results)

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


@app.route("/delete-post/<int:entry_id>", methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Post deleted', 'success')
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)
    
    




