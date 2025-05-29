from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def yoco_webhook(request):
    """Handle Yoco payment webhooks"""
    try:
        payload = json.loads(request.body)
        # Process payment confirmation
        # This will be implemented when we integrate Yoco
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})