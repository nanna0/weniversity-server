from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Mission
from .serializers import MissionSerializer, MissionResultSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_mission(request):
    """
    미션 제출 API
    """
    user = request.user
    data = request.data.copy()
    data['email'] = user.email  # 이메일 자동 설정
    
    serializer = MissionSerializer(data=data)
    if serializer.is_valid():
        # 기존 제출이 있다면 업데이트, 없으면 생성
        mission, created = Mission.objects.update_or_create(
            email=user.email,
            problem_id=data['problem_id'],
            defaults={
                'title': data['title'],
                'user_code': data.get('user_code', ''),
                'is_correct': data.get('is_correct', False),
                'message': data.get('message', ''),
            }
        )
        return Response(MissionSerializer(mission).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mission_results(request):
    """
    사용자의 모든 미션 제출 결과 조회
    """
    user = request.user
    missions = Mission.objects.filter(email=user.email)
    serializer = MissionResultSerializer(missions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mission_statistics(request):
    """
    사용자의 미션 통계 조회
    """
    user = request.user
    missions = Mission.objects.filter(email=user.email)
    
    total_submitted = missions.count()
    solved_count = missions.filter(is_correct=True).count()
    skipped_count = missions.filter(user_code='').count()
    
    accuracy = 0
    if total_submitted > 0:
        accuracy = round((solved_count / total_submitted) * 100)
    
    return Response({
        'total_submitted': total_submitted,
        'solved_count': solved_count,
        'skipped_count': skipped_count,
        'accuracy': accuracy
    })