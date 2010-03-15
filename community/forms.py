from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.template import loader,Context

class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
        help_text = _("Thirty alphanumeric characters or less."),
        error_message = _("This value must contain only letters, numbers and underscores."))
    email = forms.EmailField(label=_("E-mail"),help_text="We hate spam as much as you do.", max_length=75)
    password = forms.CharField(label=_("Password"), max_length=50, widget=forms.PasswordInput(render_value=False),
                    help_text = _("Don't use a sensitive password, as it will be mailed back to you in cleartext."))

    class Meta:
        model = User
        fields = ("username","email","password")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        
        #if User.objects.filter(email__iexact=self.cleaned_data['email']).count():
        #    raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def save(self, commit=True, domain_override=None, email_template_name='registration/registration_email.txt',
             use_https=False):
        user = super(RegistrationForm, self).save(commit=False)
        #user.set_unusable_password()
        if not commit:
            return user
        user.save()

        from django.core.mail import send_mail
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'user': user,
            'protocol': use_https and 'https' or 'http',
        }
        send_mail(_("Your registration for %s") % site_name,
            t.render(Context(c)), None, [user.email], fail_silently=False)
        return user

