from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction

class Category(models.Model):
    name = models.CharField(_("Nome"), max_length=100)
    order = models.IntegerField(_("Ordem"), default=0)
    is_active = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Categoria e seus Presentes")
        verbose_name_plural = _("Categorias e seus Presentes")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Gift(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', _("Disponível")
        PARTIALLY = 'partially', _("Parcialmente Reservado")
        RESERVED = 'reserved', _("Totalmente Reservado")
        HIDDEN = 'hidden', _("Oculto")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='gifts', verbose_name=_("Categoria"))
    name = models.CharField(_("Nome"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    image = models.ImageField(_("Imagem"), upload_to='gifts/', blank=True, null=True)
    
    total_quantity = models.PositiveIntegerField(_("Quantidade Total"), default=1)
    reserved_quantity = models.PositiveIntegerField(_("Quantidade Reservada"), default=0)
    
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    order = models.IntegerField(_("Ordem"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Presente")
        verbose_name_plural = _("Presentes")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def available_quantity(self):
        return max(0, self.total_quantity - self.reserved_quantity)

    def clean(self):
        if self.reserved_quantity > self.total_quantity:
            raise ValidationError(_("A quantidade reservada não pode ser maior que a quantidade total."))
        
    def save(self, *args, **kwargs):
        # Update status based on quantities if not hidden
        if self.status != self.Status.HIDDEN:
            if self.reserved_quantity >= self.total_quantity:
                self.status = self.Status.RESERVED
            elif self.reserved_quantity > 0:
                self.status = self.Status.PARTIALLY
            else:
                self.status = self.Status.AVAILABLE
        super().save(*args, **kwargs)

class GiftReservation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _("Ativa")
        CANCELLED = 'cancelled', _("Cancelada")

    gift = models.ForeignKey(Gift, on_delete=models.PROTECT, related_name='reservations', verbose_name=_("Presente"))
    guest_name = models.CharField(_("Nome do Convidado"), max_length=200)
    quantity = models.PositiveIntegerField(_("Quantidade"), default=1)
    message = models.TextField(_("Mensagem"), blank=True)
    is_message_approved = models.BooleanField(_("Mensagem Aprovada"), default=False)
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guest_name} - {self.gift.name} ({self.quantity})"

class SiteSettings(models.Model):
    couple_name = models.CharField(_("Nome do Casal"), max_length=200, default="Pedro & Sabrina")
    wedding_date = models.DateTimeField(_("Data e Hora do Casamento"), null=True, blank=True)
    main_quote = models.TextField(_("Frase Principal"), default="Nossa história continua aqui.")
    our_story = models.TextField(_("Nossa História"), blank=True)
    
    location_name = models.CharField(_("Local do Casamento"), max_length=200, blank=True)
    location_address = models.TextField(_("Endereço"), blank=True)
    location_map_link = models.URLField(_("Link do Mapa"), blank=True)
    
    hero_image = models.ImageField(_("Foto da Capa"), upload_to='site/', blank=True, null=True)
    story_image = models.ImageField(_("Foto da História"), upload_to='site/', blank=True, null=True)
    
    pix_key = models.CharField(_("Chave PIX"), max_length=200, blank=True)
    pix_name = models.CharField(_("Nome do Recebedor PIX"), max_length=200, blank=True)
    pix_city = models.CharField(_("Cidade PIX"), max_length=200, blank=True)
    pix_qrcode = models.ImageField(_("QR Code PIX"), upload_to='site/', blank=True, null=True)
    pix_text = models.TextField(_("Texto do PIX"), default="Se quiser contribuir de outra forma...")
    
    notification_email = models.EmailField(_("E-mail para Notificações"), blank=True)
    
    show_messages = models.BooleanField(_("Exibir Mensagens dos Convidados"), default=True)

    class Meta:
        verbose_name = _("Textos e Galeria do Site")
        verbose_name_plural = _("Textos e Galeria do Site")

    def __str__(self):
        return "Textos e Galeria do Site"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
        
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class GalleryImage(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='gallery_images', null=True, blank=True)
    image = models.ImageField(_("Imagem"), upload_to='gallery/')
    order = models.IntegerField(_("Ordem"), default=0)

    class Meta:
        verbose_name = _("Imagem da Galeria")
        verbose_name_plural = _("Imagens da Galeria")
        ordering = ['order', 'id']

    def __str__(self):
        return f"Imagem {self.id}"

class NotificationLog(models.Model):
    event = models.CharField(_("Evento"), max_length=200)
    recipient = models.CharField(_("Destinatário"), max_length=200)
    status = models.CharField(_("Status"), max_length=50)
    error = models.TextField(_("Erro"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Log de Notificação")
        verbose_name_plural = _("Logs de Notificações")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event} -> {self.recipient} [{self.status}]"
