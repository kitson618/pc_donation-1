from flask_babel import _

categories = [
    {
        'link_name': 'auth/register_donate',
        'name': _('Donator'),
        'body': _("index_page_donate_info")
    },
    {
        'link_name': 'auth/register_student',
        'name': _('Student'),
        'body': _("index_page_student_info")
    },
    {
        'link_name': 'support',
        'name': _('Volunteer'),
        'body': _("index_page_volunteer_info")
    }
]

supporters = [
    {
        'link_name': 'auth/register_teacher',
        'name': _('School teacher'),
        'body': _("volunteer_page_teacher_info")
    },
    {
        'link_name': 'auth/register_volunteer',
        'name': _('Support Volunteer'),
        'body': _("volunteer_page_volunteer_info")
    }

]

