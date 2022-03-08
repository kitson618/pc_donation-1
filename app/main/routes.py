from datetime import datetime, date, timedelta
from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import azure_blob, db
from app.main.forms import EditProfileForm
from app.main.decorator import check_confirmed
from app.models import User, Teacher, Region, EquipmentType, EquipmentApplication
from app.main import bp
from app.main import index_data
from webconfig import ai_chatbot


@bp.before_request
def before_request():
    if User.is_authenticated:
        User.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # recent_applications = db.session.query(EquipmentApplication).filter(
    #     db.and_(EquipmentApplication.student == current_user),
    #     db.func.date(EquipmentApplication.created_at) < (date.today() - timedelta(days=180))
    # )
    # if recent_applications.count():
    #     # TODO: Check the original Logic
    #     print(recent_applications)
    categorys = index_data.categories
    # isTeacher = None
    if User.is_authenticated:
        if not User.activated:
            return redirect(url_for('auth.unconfirmed'))
        # elif current_user.role == "teacher" and current_user.admin_confirm == False:
        #     return redirect(url_for('admin.admin_unconfirm'))
        # elif current_user.role == "student" and current_user.admin_confirm == False and isTeacher == None:
        #     return redirect(url_for('student.student_be_confirm_view'))
        # elif current_user.role == "student" and current_user.admin_confirm == False and isTeacher != None:
        #     return redirect(url_for('teacher.teacher_unconfirm'))
        # elif current_user.role == "teacher":
        #     return redirect(url_for('support.teacher_view'))
        # elif current_user.role == "volunteer":
        #     return redirect(url_for('support.volunteer_view'))
        # elif current_user.role == "student":
        return redirect(url_for('student.student_view'))
        # elif current_user.role == "donate":
        #     return redirect(url_for('donate.donate_view'))
        # elif current_user.role == "admin":
        #     return redirect(url_for('admin.admin_view'))
        # else:
        #     return render_template('index.html', title=_('Home'), categorys=categorys, withoutcontainer=True,
        #                            key=ai_chatbot.index_chatbot_key)
    else:
        return render_template('index.html', title=_('Home'), categorys=categorys, withoutcontainer=True,
                               key=ai_chatbot.index_chatbot_key)


@bp.route('/support', methods=['GET', 'POST'])
def supporter():
    return render_template('support/index.html', title=_('Home'), supportors=index_data.supporters)


# @bp.route('/explore')
# @login_required
# def explore():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.timestamp.desc()).paginate(
#         page, current_app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main.explore', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('main.explore', page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('index.html', title=_('Explore'),
#                            posts=posts.items, next_url=next_url,
#                            prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
@check_confirmed
def user(username):
    login_user = User.query.filter_by(username=username).first_or_404()

    # information = db.session.query(User.full_name, User.email, User.id, User.email, ).filter().all()

    # page = request.args.get('page', 1, type=int)
    # posts = user.posts.order_by(Post.timestamp.desc()).paginate(
    #     page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('main.user', username=user.username, page=posts.next_num) \
    #     if posts.has_next else None
    # prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
    #     if posts.has_prev else None
    return render_template('user.html', user=login_user,
                           image=azure_blob.get_img_url_with_blob_sas_token)  # ,posts=posts.items,
    # next_url=next_url, prev_url=prev_url

    # return render_template('user.html', user=user, posts=posts.items,
    #                        next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit_profile():
    form = EditProfileForm(current_user.username)
    form.region.choices = [(s.id, s.region) for s in db.session.query(Region).all()]
    print(current_user.region)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.region_id = form.region.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
        form.region.data = current_user.region_id
        form.phone_number.data = current_user.phone_number

    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(request.referrer)


@bp.route('/terms')
def terms():
    return render_template('terms.html', title=_('Terms'))


@bp.route('/about-us')
def about_us():
    return render_template('about_us.html', title=_('About US'))
