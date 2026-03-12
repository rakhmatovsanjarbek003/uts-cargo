from django.urls import path
from .views import (
    get_my_arrived_groups, upload_payment_check, set_delivery_method,
    admin_get_pending_payments, admin_verify_payment
)

urlpatterns = [
    path('my-arrived-groups/', get_my_arrived_groups),
    path('groups/<int:group_id>/upload-check/', upload_payment_check),
    path('groups/<int:group_id>/set-delivery/', set_delivery_method),
    path('admin/pending-payments/', admin_get_pending_payments),
    path('admin/verify-payment/<int:group_id>/', admin_verify_payment),
]