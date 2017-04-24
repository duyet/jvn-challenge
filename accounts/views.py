from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.shortcuts import render

from .forms import RegistrationForm
from .models import User

class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User

    def form_valid(self, form):
        obj = form.save(commit=True)
        # obj.set_password(User.objects.make_random_password())
        # obj.save()

        # # This form only requires the "email" field, so will validate.
        # reset_form = PasswordResetForm(self.request.POST)
        # reset_form.is_valid()  # Must trigger validation
        # # Copied from django/contrib/auth/views.py : password_reset
        # opts = {
        #     'use_https': self.request.is_secure(),
        #     'email_template_name': 'registration/verification.html',
        #     'subject_template_name': 'registration/verification_subject.txt',
        #     'request': self.request,
        #     # 'html_email_template_name': provide an HTML content template if you desire.
        # }
        # # This form sends the email on save()
        # reset_form.save(**opts)

        return redirect('accounts:register-done')

def profile(request):
    context = {
        'user': request.user
    }

    return render(request, 'accounts/profile.html', context)

def settings(request, setting = ''):
    setting_pages = [ 'Profile', 'Account', ]

    setting_pages = [ { 'alias': p.lower(), 'name': p} for p in setting_pages ]
    print setting_pages[0]

    if setting not in [p['alias'] for p in setting_pages]:
        setting = setting_pages[0]['alias']

    def get_page_title(page):
        for p in setting_pages:
            if page == p['alias']:
                return p['name']
        return None

    context = {
        'user': request.user,
        'setting_pages': setting_pages,
        'setting': setting,
        'page_title': get_page_title(setting)
    }

    return render(request, 'accounts/settings/%s.html' % setting, context)