from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .ai_service import get_recipe_ai_service
from .models import SearchHistory


def home(request):
    """Render the home page"""
    return render(request, 'home.html')


@api_view(['POST'])
def search_recipe(request):
    """
    API endpoint to search for recipes
    Accepts: { "query": "recipe name or ingredients", "type": "recipe" or "ingredients" }
    """
    try:
        data = request.data
        query = data.get('query', '').strip()
        query_type = data.get('type', 'recipe')  # 'recipe' or 'ingredients'
        
        if not query:
            return Response(
                {'error': 'Query is required', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get AI service
        try:
            ai_service = get_recipe_ai_service()
        except Exception as init_error:
            print(f"AI Service initialization error: {init_error}")
            import traceback
            traceback.print_exc()
            return Response(
                {
                    'error': f'Failed to initialize AI service: {str(init_error)}',
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Perform search based on type
        if query_type == 'recipe':
            result = ai_service.search_by_recipe_name(query)
        elif query_type == 'ingredients':
            result = ai_service.search_by_ingredients(query)
        else:
            result = ai_service.general_query(query)
        
        # Save to history
        if result.get('success'):
            try:
                SearchHistory.objects.create(
                    query_type=query_type,
                    query_text=query,
                    result=result.get('result', '')
                )
            except Exception as db_error:
                print(f"Database error (non-critical): {db_error}")
        
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Unexpected error in search_recipe: {e}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': str(e), 'success': False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def search_history(request):
    """
    Get search history
    """
    try:
        history = SearchHistory.objects.all()[:20]  # Last 20 searches
        data = [
            {
                'id': item.id,
                'query_type': item.query_type,
                'query_text': item.query_text,
                'created_at': item.created_at.isoformat()
            }
            for item in history
        ]
        return Response({'history': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    """
    try:
        ai_service = get_recipe_ai_service()
        return Response({
            'status': 'healthy',
            'ai_service': 'initialized'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
