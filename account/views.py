from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginFrom(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             # auth возвращает объект User если учетные данные правильные
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     # login задает пользователя в текущем сеансе
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginFrom()
#     return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(requset):
    return render(requset,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
