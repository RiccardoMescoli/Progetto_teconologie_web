from operator import attrgetter

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView

from user_profile.decorators import no_profile, profile_required
from user_profile.forms import ExtendedUserCreationForm, UserProfileCreateForm, UserProfileEditForm
from user_profile.models import ChatMessage, UserProfile, UserProfileFollow

from user_profile.search import get_user_profile_queryset

from django.contrib.humanize.templatetags.humanize import naturaltime


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


# ---------- Search pages ----------

def user_profile_search_view(request):
    context = {}

    if request.GET:
        query = request.GET.get('query')
        context['query'] = query

        results_list = sorted(get_user_profile_queryset(query), key=attrgetter('user.username'), reverse=False)
        context['results_list'] = results_list

    return render(request, 'user_profile/search_pages/user_profile/search.html', context)

@profile_required
def user_profile_followed_list_view(request):
    context = {}

    followed_ids = UserProfileFollow.objects.filter(follower=request.user.profile).values('followed')
    followed_profiles = UserProfile.objects.filter(id__in=followed_ids)

    results_list = sorted(followed_profiles, key=attrgetter('user.username'), reverse=False)
    context['results_list'] = results_list

    return render(request, 'user_profile/search_pages/user_profile/followed_list.html', context)


# ---------------  ChatMessage -----------------

@profile_required
def chat_list(request):
    context = {}

    chatting_with_ids = ChatMessage.objects.filter(sender=request.user.profile).values('receiver').union(
        ChatMessage.objects.filter(receiver=request.user.profile).values('sender')
    ).distinct()
    chatting_with = UserProfile.objects.filter(
        id__in=chatting_with_ids
    ).distinct()

    context['chatting_with'] = list(set([profile for profile in chatting_with]))

    return render(request, 'user_profile/search_pages/user_chat/chat_list.html', context)


@profile_required
def chat_main(request, **kwargs):
    if request.POST:
        try:
            receiver = UserProfile.objects.get(id=kwargs.get('pk', None))
        except UserProfile.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        message = ChatMessage(
            text=request.POST['message'],
            sender=request.user.profile,
            receiver=receiver,
        )
        message.save()
        return redirect(reverse_lazy('user_profile:chat', args=(kwargs.get('pk', None),)))

    else:
        try:
            receiver = UserProfile.objects.get(id=kwargs.get('pk', None))
        except UserProfile.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        delete_button = kwargs.get('delete_button', False)

        if ChatMessage.objects.filter(sender=request.user.profile, receiver=receiver).union(
                ChatMessage.objects.filter(sender=receiver, receiver=request.user.profile)
        ).distinct().exists():
            delete_button = True

        context = {'receiver': receiver, 'delete_button': delete_button}
        return render(request, 'user_chat/chat.html', context)


@profile_required
def delete_chat(request, **kwargs):
    if request.POST:
        try:
            receiver = UserProfile.objects.get(id=kwargs.get('pk', None))
        except UserProfile.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        ChatMessage.objects.filter(sender=request.user.profile, receiver=receiver).delete()
        ChatMessage.objects.filter(sender=receiver, receiver=request.user.profile).delete()

        return redirect(reverse("user_profile:chat-list"))

    else:
        try:
            receiver = UserProfile.objects.get(id=kwargs.get('pk', None))
        except UserProfile.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        context = {'receiver': receiver}
        return render(request, 'user_chat/delete.html', context)


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


@profile_required
def ajax_get_chat_messages(request):
    receiver = UserProfile.objects.get(id=request.GET.get('receiver', False))
    messages = ChatMessage.objects.filter(
        sender=request.user.profile,
        receiver=receiver
    ).union(ChatMessage.objects.filter(
        sender=receiver,
        receiver=request.user.profile
    )
    ).order_by('creation_datetime')

    results = [[
        message.sender.user.username if len(message.sender.user.username) < 20
        else message.sender.user.username[:20] + "...",
        message.text,
        naturaltime(message.creation_datetime),
        message.sender.user == request.user] for message in messages]

    return JsonResponse(results, safe=False)
