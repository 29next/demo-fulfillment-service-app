from allauth.account import forms as allauth_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CustomLoginForm(allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'account_login'
        self.helper.layout = Layout(
            'login',
            'password',
            Submit(
                'submit',
                'Sign In',
                css_class="btn btn-primary w-100",
            )
        )
