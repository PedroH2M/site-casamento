from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import SiteSettings, Category, Gift, GiftReservation, GalleryImage, NotificationLog

def home(request):
    settings = SiteSettings.get_settings()
    categories = Category.objects.filter(is_active=True).prefetch_related('gifts')
    gallery = GalleryImage.objects.all()
    approved_messages = GiftReservation.objects.filter(is_message_approved=True).exclude(message__exact='')
    
    # Filter active gifts that aren't hidden
    active_categories = []
    for cat in categories:
        gifts = cat.gifts.exclude(status=Gift.Status.HIDDEN)
        if gifts.exists():
            active_categories.append({
                'category': cat,
                'gifts': gifts
            })

    context = {
        'settings': settings,
        'categories': active_categories,
        'gallery': gallery,
        'guest_messages': approved_messages,
    }
    return render(request, 'registry/home.html', context)

def reserve_gift(request, gift_id):
    gift = get_object_or_404(Gift, id=gift_id)
    
    if gift.status in [Gift.Status.RESERVED, Gift.Status.HIDDEN]:
        messages.error(request, "Este presente não está mais disponível.")
        return redirect('home')

    if request.method == 'POST':
        guest_name = request.POST.get('guest_name', '').strip()
        quantity_str = request.POST.get('quantity', '1')
        message_text = request.POST.get('message', '').strip()
        
        if not guest_name:
            messages.error(request, "Por favor, informe seu nome.")
            return redirect('reserve_gift', gift_id=gift.id)
            
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                raise ValueError
        except ValueError:
            messages.error(request, "Quantidade inválida.")
            return redirect('reserve_gift', gift_id=gift.id)

        try:
            with transaction.atomic():
                # Lock the row for update
                locked_gift = Gift.objects.select_for_update().get(id=gift.id)
                
                if locked_gift.available_quantity < quantity:
                    messages.error(request, f"Desculpe, apenas {locked_gift.available_quantity} unidades disponíveis.")
                    return redirect('reserve_gift', gift_id=gift.id)
                
                # Create reservation
                reservation = GiftReservation.objects.create(
                    gift=locked_gift,
                    guest_name=guest_name,
                    quantity=quantity,
                    message=message_text,
                )
                
                # Update gift quantity
                locked_gift.reserved_quantity += quantity
                locked_gift.save() # This will also update the status
                
                # Log notification (we simulate email sending for now)
                NotificationLog.objects.create(
                    event="Nova Reserva",
                    recipient="Noivos",
                    status="Pendente",
                )
                
                messages.success(request, "Presente reservado com carinho! ❤️")
                return redirect('home')
        except Exception as e:
            messages.error(request, "Não conseguimos concluir sua reserva. Tente novamente.")
            return redirect('reserve_gift', gift_id=gift.id)

    context = {
        'gift': gift,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'registry/reserve.html', context)

from django.contrib.auth.decorators import login_required
from .forms import GiftForm

@login_required
def panel_dashboard(request):
    gifts = Gift.objects.select_related('category').all()
    reservations = GiftReservation.objects.select_related('gift').all()
    return render(request, 'registry/panel_dashboard.html', {
        'gifts': gifts,
        'reservations': reservations,
        'settings': SiteSettings.get_settings()
    })

@login_required
def panel_gift_create(request):
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Presente adicionado com sucesso!")
            return redirect('panel_dashboard')
    else:
        form = GiftForm()
    return render(request, 'registry/panel_gift_form.html', {'form': form, 'title': 'Adicionar Presente', 'settings': SiteSettings.get_settings()})

@login_required
def panel_gift_edit(request, pk):
    gift = get_object_or_404(Gift, pk=pk)
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES, instance=gift)
        if form.is_valid():
            form.save()
            messages.success(request, "Presente salvo!")
            return redirect('panel_dashboard')
    else:
        form = GiftForm(instance=gift)
    return render(request, 'registry/panel_gift_form.html', {'form': form, 'title': 'Editar Presente', 'gift': gift, 'settings': SiteSettings.get_settings()})

@login_required
def panel_gift_delete(request, pk):
    gift = get_object_or_404(Gift, pk=pk)
    if request.method == 'POST':
        gift.delete()
        messages.success(request, "Presente excluído!")
        return redirect('panel_dashboard')
    return HttpResponseBadRequest()

