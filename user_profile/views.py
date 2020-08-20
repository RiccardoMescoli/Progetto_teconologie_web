from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView

from user_profile.decorators import profile_required
from user_profile.forms import ExtendedUserCreationForm, UserProfileCreateForm, UserProfileEditForm
from user_profile.models import ExtendedUser, UserProfile


class UserCreateView(CreateView):
    form_class = ExtendedUserCreationForm
    template_name = 'registration/user_crispy_create.html'
    success_url = reverse_lazy('homepage')


@method_decorator(login_required, name='dispatch')
class UserProfileCreateView(CreateView):
    form_class = UserProfileCreateForm
    model = UserProfile
    template_name = 'user_profile/create.html'

    def form_valid(self, form):
        user = self.request.user
        instance, _ = UserProfile.objects.get_or_create(user=user)
        instance.profile_picture = form.cleaned_data.get('profile_picture', None)
        instance.first_name = form.cleaned_data.get('first_name', '').capitalize()
        instance.last_name = form.cleaned_data.get('last_name', '').capitalize()
        instance.save()
        return redirect(reverse('user_profile:user-profile-detail', args=(self.request.user.profile.id,)))


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'user_profile/detail.html'


@profile_required
def own_user_profile_detail_view(request):
    return redirect('user_profile:user-profile-detail', pk=request.user.profile.id)


@method_decorator(profile_required, name='dispatch')
class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'user_profile/edit.html'
    success_url = reverse_lazy('user_profile:own-user-profile-detail')

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect(self.get_success_url())
        return super(UserProfileEditView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.id == kwargs['pk']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return reverse('user_profile:own-user-profile-detail')




