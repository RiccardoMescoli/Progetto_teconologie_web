from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_profile.models import ExtendedUser, UserProfile


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'repeat your password'
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Register', css_class='btn btn-success')
        )

    class Meta:
        model = ExtendedUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'terms_of_service_acceptance',
        )


class UserProfileCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'user-profile-creation-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Save'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.inputs[0].value = 'Create'
        self.helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'first_name', 'last_name')


class UserProfileEditForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'user-profile-edit-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Save'))
    helper.add_input(
        Submit('cancel', 'Cancel', css_class='btn btn-danger ml-md-2')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'first_name', 'last_name')
