from django.db import models
from accounts.models import User
from core import settings

class Cargo(models.Model):
    STATUS_CHOICES = [
        ('Omborda', 'Omborda'),
        ('Yo\'lda', 'Yo\'lda'),
        ('Punktda', 'Punktda'),
        ('Topshirildi', 'Topshirildi'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cargos', verbose_name="Foydalanuvchi")
    track_code = models.CharField(max_length=50, unique=True, verbose_name="Trek kod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Omborda', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Oxirgi o'zgarish")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Topshirilgan vaqt")
    warehouse_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='warehouse_actions', verbose_name="Ombor admini")
    onway_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='onway_actions', verbose_name="Yo'lga chiqargan")
    arrived_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='arrived_actions', verbose_name="Punktga qabul qilgan")
    delivered_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='delivery_actions', verbose_name="Topshirgan admin")
    arrived_group = models.ForeignKey(
        'warehouse.ArrivedGroup',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cargos',
        verbose_name="Kelganlar guruhi"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_cargos', verbose_name="Qo'shgan admin")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='updated_cargos', verbose_name="Mas'ul admin")

    def __str__(self):
        return f"{self.track_code} - {self.status}"

    class Meta:
        verbose_name = "Yuk"
        verbose_name_plural = "Yuklar"

class WarehouseCargo(Cargo):
    class Meta:
        proxy = True
        verbose_name = "Ombordagi yuk"
        verbose_name_plural = "Ombordagi yuklar"

class OnWayCargo(Cargo):
    class Meta:
        proxy = True
        verbose_name = "Yo'ldagi yuk"
        verbose_name_plural = "Yo'ldagi yuklar"

class ArrivedCargo(Cargo):
    class Meta:
        proxy = True
        verbose_name = "Punkda (Topshirish)"
        verbose_name_plural = "Punktda (Topshirish)"

class DeliveredCargo(Cargo):
    class Meta:
        proxy = True
        verbose_name = "Topshirilgan yuk"
        verbose_name_plural = "Topshirilgan yuklar"