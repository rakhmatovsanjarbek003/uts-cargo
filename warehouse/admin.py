from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from cargo.models import Cargo
from warehouse.models import ArrivedGroup, PaymentRequest, DeliveryQueue


@admin.register(ArrivedGroup)
class ArrivedGroupAdmin(admin.ModelAdmin):
    list_display = ('receipt_code', 'user', 'payment_status', 'created_at')
    filter_horizontal = ('selected_cargos',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "selected_cargos":
            kwargs["queryset"] = Cargo.objects.exclude(status='Punktda')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.selected_cargos.all().update(
            status='Punktda',
            arrived_group=obj,
            arrived_admin=request.user
        )

    class Media:
        js = ('admin/js/vendor/jquery/jquery.js', 'cargo_filter.js',)

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('receipt_code', 'display_user', 'total_price', 'payment_status', 'created_at')
    list_filter = ('payment_status',)
    readonly_fields = ('payment_check_image',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(payment_status='Tasdiqlash jarayonida')

    def display_user(self, obj):
        return f"{obj.user.first_name} ({obj.user.user_id})"

    display_user.short_description = "Foydalanuvchi"

    def payment_check_image(self, obj):
        if obj.payment_check:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="300" /></a>', obj.payment_check.url)
        return "Chek yuklanmagan"

    payment_check_image.short_description = "Chek rasmi"
    actions = ['approve_payments', 'reject_payments']

    @admin.action(description="To'lovni tasdiqlash (✅)")
    def approve_payments(self, request, queryset):
        for group in queryset:
            group.payment_status = 'To\'lov tasdiqlandi'
            group.admin_note = "To'lov qabul qilindi ✅"
            group.save()
        self.message_user(request, f"{queryset.count()} ta to'lov tasdiqlandi.")

    @admin.action(description="To'lovni rad etish (❌)")
    def reject_payments(self, request, queryset):
        queryset.update(payment_status='To\'lov rad etildi', admin_note="To'lov topilmadi yoki chek xato ❌")
        self.message_user(request, f"{queryset.count()} ta to'lov rad etildi.")

@admin.register(DeliveryQueue)
class DeliveryQueueAdmin(admin.ModelAdmin):
    list_display = ('receipt_code', 'get_customer', 'delivery_method', 'delivery_address', 'payment_status')
    list_filter = ('delivery_method', 'payment_status')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            payment_status='To\'lov tasdiqlandi'
        ).exclude(delivery_method__isnull=True).exclude(delivery_method='').exclude(
            cargos__status='Topshirildi').distinct()

    def get_customer(self, obj):
        return format_html("<b>{}</b><br/>{}", obj.user.first_name, obj.user.phone)

    get_customer.short_description = "Mijoz"

    actions = ['ship_out_cargos']

    @admin.action(description="Tanlangan yuklarni topshirish (🚚)")
    def ship_out_cargos(self, request, queryset):
        for group in queryset:
            cargos = group.cargos.all()
            for cargo in cargos:
                cargo.status = 'Topshirildi'
                cargo.delivered_at = timezone.now()
                cargo.delivered_admin = request.user
                cargo.updated_by = request.user
                cargo.save()
        self.message_user(request, "Yuklar muvaffaqiyatli topshirildi va statuslari 'Topshirildi'ga o'zgartirildi.")
    readonly_fields = ('receipt_code', 'user', 'total_price', 'payment_status')