from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, DetailView, UpdateView

from book_functionalities.forms import AuthorEditForm
from book_functionalities.models import Author

from user_profile.decorators import moderators_only


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'book_functionalities/author/detail.html'


@method_decorator(moderators_only, name='dispatch')
class AuthorEditView(UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'book_functionalities/author/edit.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('book_functionalities:author-detail', args=(self.kwargs.get('pk'),))

        if 'cancel' in self.request.POST:
            return redirect(self.success_url)

        return super(AuthorEditView, self).form_valid(form)


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'book_functionalities/author/delete.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect(reverse_lazy('book_functionalities:author-detail', args=(self.kwargs.get('pk'),)))

        return super(AuthorEditView, self).form_valid(form)