from django import forms
from django.forms.utils import ErrorList

from accounts.models import User
from .models import CompetitionSubmit


class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()
	def as_divs(self):
		if not self: return ''
		return '<div class="alert alert-danger">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])

class CompetitionSubmitForm(forms.ModelForm):
    def __init__(self, user, competition, *args, **kwargs):
        self.user = user
        self.competition = competition

        super(CompetitionSubmitForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CompetitionSubmit
        error_class=DivErrorList
        fields = ('file', )

    def save(self, commit=True, *args, **kwargs):
        submit = super(CompetitionSubmitForm, self).save(commit=False, *args, **kwargs)
        submit.author = User.objects.get(username=self.user)
        submit.competition = self.competition

        if commit:
            submit.save()
        return submit
