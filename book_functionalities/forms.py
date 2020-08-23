from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit

from book_functionalities.models import Author, Book, BookGenre, BookReview


class BaseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Save'))
    helper.add_input(Button('back', 'Cancel',
                            css_class='btn-secondary ml-3',
                            onClick="javascript:history.go(-1);"))


class AuthorEditForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'author-edit-form'
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'
        self.fields['birth_date'].widget = forms.TextInput(attrs={'type': 'date'})

    class Meta:
        model = Author
        fields = ('portrait', 'full_name', 'birth_date', 'biography')


class AuthorCreateForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'author-create-form'
        self.helper.inputs[0].value = 'Create'
        self.helper.inputs[0].field_classes = 'btn btn-success'
        self.fields['birth_date'].widget = forms.TextInput(attrs={'type': 'date'})

    class Meta:
        model = Author
        fields = ('portrait', 'full_name', 'birth_date', 'biography')


class BookEditForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'book-edit-form'
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'
        self.fields['release_date'].widget = forms.TextInput(attrs={'type': 'date'})

    class Meta:
        model = Book
        fields = ('cover', 'title', 'author', 'release_date', 'synopsis', 'genres')


class BookCreateForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'author-create-form'
        self.helper.inputs[0].value = 'Create'
        self.helper.inputs[0].field_classes = 'btn btn-success'
        self.fields['author'].label = ''
        self.fields['release_date'].widget = forms.TextInput(attrs={'type': 'date'})


    class Meta:
        model = Book
        fields = ('author', 'cover', 'title', 'release_date', 'synopsis', 'genres')


class BookGenreEditForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'book-genre-edit-form'
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'

    class Meta:
        model = BookGenre
        fields = ('name',)


class BookGenreCreateForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'book-genre-create-form'
        self.helper.inputs[0].value = 'Create'
        self.helper.inputs[0].field_classes = 'btn btn-warning'

    class Meta:
        model = BookGenre
        fields = ('name',)


class BookReviewCreateForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'book-review-create-form'
        self.helper.inputs[0].value = 'Create'
        self.helper.inputs[0].field_classes = 'btn btn-success'
        self.fields['book'].label = ''
        self.fields['content'].label = 'Content (MaxChars: 500)'
        self.fields['content'].widget = forms.Textarea(attrs={'maxlenght': 500, 'rows': 5, 'cols': 100})
        self.fields['rating'].label = 'rating'

    '''
    def clean(self):
        cleaned_data = super(BookReviewCreateForm, self).clean()
    '''

    class Meta:
        model = BookReview
        fields = ('book', 'rating', 'spoiler', 'content',)


class BookReviewEditForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_id = 'book-review-edit-form'
        self.helper.inputs[0].value = 'Update'
        self.helper.inputs[0].field_classes = 'btn btn-warning'
        self.fields['book'].label = ''
        self.fields['content'].label = 'Content (MaxChars: 500)'
        self.fields['content'].widget = forms.Textarea(attrs={'maxlenght': 500, 'rows': 5, 'cols': 100})
        self.fields['rating'].label = 'rating'

    class Meta:
        model = BookReview
        fields = ('book', 'rating', 'spoiler', 'content',)







