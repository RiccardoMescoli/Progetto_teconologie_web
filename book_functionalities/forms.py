from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, HTML, Layout, Submit
from django.utils.timezone import now

from book_functionalities.models import Author

class AuthorBaseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'author-edit-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Save'))
    helper.add_input(
        Submit('cancel', 'Cancel', css_class='btn btn-danger ml-md-2')
    )


class AuthorEditForm(AuthorBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'
        self.fields['birth_date'].widget = forms.TextInput(attrs={'type': 'date'})

    class Meta:
        model = Author
        fields = ('portrait', 'full_name', 'birth_date', 'biography')

