from django.http import JsonResponse
from django.shortcuts import redirect

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView

from user_profile.decorators import no_profile, profile_required
from user_profile.forms import ExtendedUserCreationForm, UserProfileCreateForm, UserProfileEditForm
from user_profile.models import UserProfile, UserProfileFollow

# --------- User and Profile ---------


class UserCreateView(CreateView):
    form_class = ExtendedUserCreationForm
    template_name = 'registration/user_crispy_create.html'
    success_url = reverse_lazy('homepage')


@method_decorator(no_profile, name='dispatch')
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

    def form_valid(self, form):
        self.success_url = reverse_lazy('user_profile:user-profile-detail', args=(self.kwargs['pk'],))
        return super(UserProfileEditView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.profile.id == kwargs['pk'] or request.user.is_superuser or request.user.is_moderator \
                    and not UserProfile.objects.get(pk=kwargs['pk']).user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass

        return redirect(reverse('user_profile:own-user-profile-detail'))


# -------------- Ajax -------------

@profile_required
def ajax_follow_create(request):
    try:
        follower = UserProfile.objects.get(pk=int(request.GET.get('follower', False)))
        followed = UserProfile.objects.get(pk=int(request.GET.get('followed', False)))
    except UserProfile.DoesNotExist:
        return JsonResponse(
            {
                'is_success': False
            }
        )

    if request.user.id != follower.user.id:
        return JsonResponse(
            {
                'is_success': False
            }
        )

    instance, _ = UserProfileFollow.objects.get_or_create(follower=follower, followed=followed)
    instance.save()

    return JsonResponse(
        {
            'is_success': True
        }
    )


@profile_required
def ajax_follow_delete(request):
    try:
        follower = UserProfile.objects.get(pk=int(request.GET.get('follower', False)))
        followed = UserProfile.objects.get(pk=int(request.GET.get('followed', False)))
    except UserProfile.DoesNotExist:
        return JsonResponse(
            {
                'is_success': False
            }
        )

    if request.user.id != follower.user.id:
        return JsonResponse(
            {
                'is_success': False
            }
        )

    try:
        instance = UserProfileFollow.objects.get(follower=follower, followed=followed)
        instance.delete()
    except UserProfileFollow.DoesNotExist:
        return JsonResponse(
            {
                'is_success': False
            }
        )

    return JsonResponse(
        {
            'is_success': True
        }
    )


