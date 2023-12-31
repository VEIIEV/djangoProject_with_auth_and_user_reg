from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from account.forms import LoginFrom, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile
from actions.models import Action
from actions.utils import create_action
from images.models import Contact


# Create your views here.


# путь закомментирован
def user_login(request):
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # auth возвращает объект User если учетные данные правильные
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # login задает пользователя в текущем сеансе
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginFrom()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(request.user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    # всё норм, мы добавляем поле following динамически в account.models
    # values_list возвращается список кортежей с данными, flat=True преобразует кортежи в единичные значения
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # user_id in (following_ids)
        actions = actions.filter(user_id__in=following_ids)
    # методы оптимизации
    # select_related() join'ит все foreignkey или только указанные
    # prefetch_related()
    actions = actions.select_related('user', 'user__profile').prefetch_related('target').order_by('-created')[:10]
    profiles = Profile.objects.all()
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'profiles': profiles,
                   'actions': actions})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # contrib.messages исп для добавления инф в контекст,
            # можно просто передать в рендер, как ещё 1 пункт словаря,
            # но так круче и универсальнее
            messages.success(request, 'profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
