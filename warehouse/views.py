from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ArrivedGroup
from .serializers import ArrivedGroupListSerializer, AdminArrivedGroupSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_arrived_groups(request):
    groups = ArrivedGroup.objects.filter(user=request.user).order_by('-created_at')
    serializer = ArrivedGroupListSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_payment_check(request, group_id):
    group = ArrivedGroup.objects.filter(id=group_id, user=request.user).first()
    if not group:
        return Response({"error": "Guruh topilmadi"}, status=404)
    image = request.FILES.get('payment_check')
    if image:
        group.payment_check = image
        group.payment_status = 'Tasdiqlash jarayonida'
        group.save()
        return Response({"message": "Chek yuborildi, admin tasdiqlashini kuting."})
    return Response({"error": "Rasm yuborilmadi"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_delivery_method(request, group_id):
    group = ArrivedGroup.objects.filter(id=group_id, user=request.user).first()
    if not group:
        return Response({"error": "Guruh topilmadi"}, status=404)
    if group.payment_status != 'To\'lov tasdiqlandi':
        return Response({"error": "Avval to'lov admin tomonidan tasdiqlanishi kerak"}, status=400)

    method = request.data.get('delivery_method')
    address = request.data.get('delivery_address', '')
    if method not in ['Punktda', 'Pochta', 'Taksi']:
        return Response({"error": "Noto'g'ri yetkazib berish usuli"}, status=400)

    group.delivery_method = method
    group.delivery_address = address
    group.save()
    return Response({"message": "Qabul qilish turi saqlandi."})


# --- ADMIN VIEWS ---

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_get_pending_payments(request):
    pending_groups = ArrivedGroup.objects.filter(payment_status='Tasdiqlash jarayonida').order_by('-created_at')
    serializer = AdminArrivedGroupSerializer(pending_groups, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_verify_payment(request, group_id):
    try:
        group = ArrivedGroup.objects.get(id=group_id)
    except ArrivedGroup.DoesNotExist:
        return Response({"error": "Guruh topilmadi"}, status=404)

    action = request.data.get('action')
    note = request.data.get('note', '')
    if action == 'confirm':
        group.payment_status = 'To\'lov tasdiqlandi'
        group.admin_note = "To'lov qabul qilindi ✅"
    elif action == 'reject':
        group.payment_status = 'To\'lov rad etildi'
        group.admin_note = note if note else "Chek xato yoki mablag' tushmadi ❌"

    group.save()
    return Response({"message": f"To'lov holati: {group.payment_status}"})