from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdvertisementForm, ResponseForm, MediaFileForm
from .models import Advertisement, Response, MediaFile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



@login_required
def create_advertisement(request):
    if request.method == 'POST':
        advertisement_form = AdvertisementForm(request.POST)
        media_file_form = MediaFileForm(request.POST, request.FILES)
        if advertisement_form.is_valid() and media_file_form.is_valid():
            advertisement = advertisement_form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()

            media_file = media_file_form.save(commit=False)
            media_file.advertisement = advertisement
            media_file.save()

            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        advertisement_form = AdvertisementForm()
        media_file_form = MediaFileForm()

    return render(request, 'board/create_advertisement.html', {'advertisement_form': advertisement_form, 'media_file_form': media_file_form})

@login_required
def respond_to_advertisement(request, advertisement_id):
    advertisement = Advertisement.objects.get(id=advertisement_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()

            # Отправка электронного письма
            send_email_notification(response)

            messages.success(request, 'Отклик успешно отправлен!')
            return redirect('dashboard')  # Перенаправление на страницу пользователя
    else:
        form = ResponseForm()

    return render(request, 'board/respond_to_advertisement.html', {'form': form, 'advertisement': advertisement})

@login_required
def dashboard(request):
    # Получить объявления пользователя и отклики на них
    user_advertisements = Advertisement.objects.filter(user=request.user)
    user_responses = Response.objects.filter(advertisement__user=request.user)

    return render(request, 'board/dashboard.html',
                  {'user_advertisements': user_advertisements, 'user_responses': user_responses})

@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/edit_advertisement.html', {'form': form})

def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    media_files = MediaFile.objects.filter(advertisement=advertisement)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement, 'media_files': media_files})

def account_activation_sent(request):
    return render(request, 'account/activation_sent.html')

def account_activation_invalid(request):
    return render(request, 'account/activation_invalid.html')

def send_email_notification(response):
    subject = 'Новый отклик на ваше объявление'
    message = f'Пользователь {response.user.username} отправил отклик на ваше объявление "{response.advertisement.title}"\n\nТекст отклика: {response.content}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [response.advertisement.user.email]

    send_mail(subject, message, from_email, recipient_list)