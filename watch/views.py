from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import FrontTest,WatchProgress,UserLastWatched
from django.utils import timezone
import traceback
from django.db.models import Count, Q

#테스트완
@csrf_exempt
def watch_progress_upsert(request):
    print(f"🔍 [DEBUG] 요청 시작 - Method: {request.method}")
    
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        body = json.loads(request.body)
        print(f"🔍 [DEBUG] 받은 데이터: {body}")
        
        # 필수 필드 검증
        user_id = body.get('userId')
        course_id = body.get('courseId')
        chapter_id = body.get('chapterId')
        video_id = body.get('videoId', chapter_id)
        
        print(f"🔍 [DEBUG] 필드 확인 - userId: {user_id}, courseId: {course_id}, chapterId: {chapter_id}")
        
        if not all([user_id, course_id, chapter_id]):
            print("❌ [DEBUG] 필수 필드 누락")
            return JsonResponse({
                'error': 'userId, courseId, chapterId are required'
            }, status=400)
        
        print(f"🔍 [DEBUG] get_or_create 시작")
        
        wp, created = WatchProgress.objects.get_or_create(
            userId=user_id,
            courseId=course_id,
            chapterId=chapter_id,
            videoId=video_id,
            defaults={
                'currentTime': body.get('currentTime', 0),
                'totalDuration': body.get('totalDuration', 0),
                'watchedPercentage': body.get('watchedPercentage', 0),
                'isCompleted': body.get('isCompleted', False),
                'chapterOrder': body.get('chapterOrder', 1),
                'videoOrder': body.get('videoOrder', 1),
                'chapterIndex': body.get('chapterIndex', 0),
                'videoIndex': body.get('videoIndex', 0),
                'totalWatchTime': body.get('totalWatchTime', 0),
                'sessionCount': body.get('sessionCount', 1),
                'watchSpeed': body.get('watchSpeed', 1.0),
                'firstWatchedAt': timezone.now(),
                'lastWatchedAt': timezone.now(),
            }
        )
        
        print(f"✅ [DEBUG] get_or_create 성공 - created: {created}, id: {wp.id}")
        
        if not created:
            print(f"🔄 [DEBUG] 기존 데이터 업데이트 시작")
            wp.currentTime = body.get('currentTime', wp.currentTime)
            wp.totalDuration = body.get('totalDuration', wp.totalDuration)
            wp.watchedPercentage = body.get('watchedPercentage', wp.watchedPercentage)
            wp.isCompleted = body.get('isCompleted', wp.isCompleted)
            wp.save()
            print(f"✅ [DEBUG] 업데이트 완료")
        
        # 🔥 마지막 시청 위치 업데이트 추가
        print(f"🔄 [DEBUG] 마지막 시청 위치 업데이트 시작")
        try:
            update_last_watched(
                user_id=user_id,
                course_id=course_id,
                chapter_id=chapter_id,
                video_id=video_id,
                chapter_order=body.get('chapterOrder', wp.chapterOrder),
                video_order=body.get('videoOrder', wp.videoOrder),
                chapter_index=body.get('chapterIndex', wp.chapterIndex),
                video_index=body.get('videoIndex', wp.videoIndex),
                current_time=body.get('currentTime', wp.currentTime)
            )
            print(f"✅ [DEBUG] 마지막 시청 위치 업데이트 완료")
        except Exception as last_watched_error:
            print(f"⚠️ [DEBUG] 마지막 시청 위치 업데이트 실패: {str(last_watched_error)}")
            # 마지막 시청 위치 업데이트 실패해도 메인 로직은 계속 진행
        
        # 간단한 응답
        response_data = {
            'success': True,
            'created': created,
            'userId': wp.userId,
            'courseId': wp.courseId,
            'chapterId': wp.chapterId,
            'videoId': wp.videoId,
            'currentTime': wp.currentTime,
        }
        
        print(f"✅ [DEBUG] 응답 데이터: {response_data}")
        
        status_code = 201 if created else 200
        return JsonResponse(response_data, status=status_code)
    
    except json.JSONDecodeError as e:
        print(f"❌ [DEBUG] JSON 파싱 에러: {str(e)}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"❌ [DEBUG] 예외 발생: {str(e)}")
        print(f"❌ [DEBUG] 타입: {type(e)}")
        print(f"❌ [DEBUG] Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

def update_last_watched(
    user_id,
    course_id,
    chapter_id,
    video_id,
    chapter_order,
    video_order,
    chapter_index,
    video_index,
    current_time
):
    print(f"🔧 [UPDATE_LAST_WATCHED] 시작: user={user_id}, course={course_id}")
    print(f"🔧 [UPDATE_LAST_WATCHED] 시작: current_time={current_time}")
    try:
        obj, created = UserLastWatched.objects.update_or_create(
            userId=user_id,
            courseId=course_id,
            defaults={
                'chapterId': chapter_id,
                'videoId': video_id,
                'lastChapterId': chapter_id,
                'lastVideoId': video_id,
                'lastChapterOrder': chapter_order,
                'lastVideoOrder': video_order,
                'lastChapterIndex': chapter_index,
                'lastVideoIndex': video_index,
                'lastCurrentTime': current_time,
                'lastWatchedAt': timezone.now(),
            }
        )
        print(f"✅ [UPDATE_LAST_WATCHED] 성공: created={created}, obj={obj.__dict__}")
        print(f"✅ [UPDATE_LAST_WATCHED] DB 저장 완료: lastCurrentTime = {current_time}")
        return obj
    except Exception as e:
        print(f"❌ [UPDATE_LAST_WATCHED] 실패: {e}")
        import traceback
        print(traceback.format_exc())
        raise


#관련챕터만
@csrf_exempt
def watch_progress_by_course(request, user_id, video_id):
    print(f"Called watch_progress_by_video with user_id={user_id}, video_id={video_id}") 
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        # 진행률 목록 - 순서대로 정렬
        progress_list = WatchProgress.objects.filter(
            userId=user_id,
            videoId=video_id
        ).order_by('chapterOrder', 'videoOrder').values(
            'userId', 'courseId', 'chapterId', 'videoId',
            'chapterOrder', 'videoOrder', 'chapterIndex', 'videoIndex',
            'currentTime', 'totalDuration', 'watchedPercentage', 'isCompleted',
            'totalWatchTime', 'sessionCount', 'watchSpeed',
            'firstWatchedAt', 'lastWatchedAt', 'completedAt'
        )

        print(f"서버 응답할 progress_list 개수: {progress_list.count()}")

        # 마지막 시청 위치 가져오기
        try:
            last_watched = UserLastWatched.objects.get(
                userId=user_id,
                videoId=video_id
            )
            last_watched_data = {
                'lastChapterId': last_watched.lastChapterId,
                'lastVideoId': last_watched.lastVideoId,
                'lastChapterOrder': last_watched.lastChapterOrder,
                'lastVideoOrder': last_watched.lastVideoOrder,
                'lastChapterIndex': last_watched.lastChapterIndex,
                'lastVideoIndex': last_watched.lastVideoIndex,
                'lastWatchedAt': last_watched.lastWatchedAt.isoformat(),
                'currentTime': last_watched.lastCurrentTime,
            }
        except UserLastWatched.DoesNotExist:
            last_watched_data = None

        # 통계 정보 계산
        total_videos = progress_list.count()
        completed_videos = progress_list.filter(isCompleted=True).count()
        
        # 챕터별 통계
        chapters_stats = progress_list.values('chapterId').annotate(
            total_videos=Count('videoId'),
            completed_videos=Count('videoId', filter=Q(isCompleted=True))
        )
        
        total_chapters = chapters_stats.count()
        completed_chapters = sum(1 for ch in chapters_stats if ch['completed_videos'] == ch['total_videos'] and ch['total_videos'] > 0)

        # 전체 진행률 계산
        overall_progress = (completed_videos / total_videos * 100) if total_videos > 0 else 0

        return JsonResponse({
            'userId': user_id,
            'videoId': video_id,
            'chapters': list(progress_list),
            'lastWatched': last_watched_data,
            'statistics': {
                'totalChapters': total_chapters,
                'completedChapters': completed_chapters,
                'totalVideos': total_videos,
                'completedVideos': completed_videos,
                'overallProgress': round(overall_progress, 2),
                'isCompleted': completed_videos == total_videos and total_videos > 0
            }
        })

    except Exception as e:
        print(f"Error in watch_progress_by_course: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)

#특정 사용자 전체 진행률
@csrf_exempt
def watch_progress_by_course_all(request, user_id, course_id):
    course_id = course_id 

    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        progress_list = WatchProgress.objects.filter(
            userId=user_id,
            courseId=course_id
        ).order_by('chapterOrder', 'videoOrder').values(
            'id', 'userId', 'courseId', 'chapterId', 'videoId',
            'chapterOrder', 'videoOrder', 'chapterIndex', 'videoIndex',
            'currentTime', 'totalDuration', 'watchedPercentage', 'isCompleted',
            'totalWatchTime', 'sessionCount', 'watchSpeed',
            'firstWatchedAt', 'lastWatchedAt', 'completedAt'
        )

        last_watched = UserLastWatched.objects.filter(
            userId=user_id,
            courseId=course_id
        ).order_by('-lastWatchedAt').first()

        if last_watched:
            last_watched_data = {
                'lastChapterId': last_watched.lastChapterId,
                'lastVideoId': last_watched.lastVideoId,
                'lastChapterOrder': last_watched.lastChapterOrder,
                'lastVideoOrder': last_watched.lastVideoOrder,
                'lastChapterIndex': last_watched.lastChapterIndex,
                'lastVideoIndex': last_watched.lastVideoIndex,
                'currentTime': last_watched.lastCurrentTime,
                'lastWatchedAt': last_watched.lastWatchedAt.isoformat(),
            }
        else:
            last_watched_data = None

        total_videos = progress_list.count()
        completed_videos = progress_list.filter(isCompleted=True).count()

        chapters_stats = progress_list.values('chapterId').annotate(
            total_videos=Count('videoId'),
            completed_videos=Count('videoId', filter=Q(isCompleted=True))
        )

        total_chapters = chapters_stats.count()
        completed_chapters = sum(
            1 for ch in chapters_stats if ch['completed_videos'] == ch['total_videos'] and ch['total_videos'] > 0
        )

        return JsonResponse({
            'userId': user_id,
            'video_id': video_id,  # 매개변수 이름 유지
            'chapters': list(progress_list),
            'lastWatched': last_watched_data,
            'statistics': {
                'totalChapters': total_chapters,
                'completedChapters': completed_chapters,
                'totalVideos': total_videos,
                'completedVideos': completed_videos,
                'overallProgress': (completed_videos / total_videos * 100) if total_videos > 0 else 0,
                'isCompleted': completed_videos == total_videos and total_videos > 0,
            }
        })

    except Exception as e:
        print(f"Error in watch_progress_by_course_all: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_watch_progress(request):
    """시청 진행률 생성/업데이트"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        course_id = data.get('courseId')
        chapter_id = data.get('chapterId')
        video_id = data.get('videoId')
        
        if not all([user_id, course_id]):
            return JsonResponse({'error': 'userId와 courseId가 필요합니다'}, status=400)
        
        # chapterId와 videoId가 없으면 자동 생성
        if not chapter_id:
            # 기존 최대 챕터 ID + 1
            max_chapter = WatchProgress.objects.filter(courseId=course_id).aggregate(Max('chapterId'))['chapterId__max']
            chapter_id = (max_chapter or (course_id * 1000)) + 1
            
        if not video_id:
            # 해당 챕터의 최대 비디오 ID + 1
            max_video = WatchProgress.objects.filter(
                courseId=course_id, 
                chapterId=chapter_id
            ).aggregate(Max('videoId'))['videoId__max']
            video_id = (max_video or (chapter_id * 100)) + 1
        
        # 기존 진행률 찾기 또는 새로 생성
        try:
            progress = WatchProgress.objects.get(
                userId=user_id,
                courseId=course_id,
                chapterId=chapter_id,
                videoId=video_id
            )
            created = False
            
            # 기존 데이터 업데이트
            progress.currentTime = data.get('currentTime', progress.currentTime)
            progress.totalDuration = data.get('totalDuration', progress.totalDuration)
            progress.watchedPercentage = data.get('watchedPercentage', progress.watchedPercentage)
            progress.isCompleted = data.get('isCompleted', progress.isCompleted)
            progress.totalWatchTime = data.get('totalWatchTime', progress.totalWatchTime)
            progress.sessionCount += 1
            progress.watchSpeed = data.get('watchSpeed', progress.watchSpeed)
            
            if progress.isCompleted and not progress.completedAt:
                progress.completedAt = timezone.now()
            elif not progress.isCompleted:
                progress.completedAt = None
                
            progress.save()
            
        except WatchProgress.DoesNotExist:
            # 새로운 진행률 생성
            created = True
            
            # 순서 정보 계산
            chapter_order = WatchProgress.objects.filter(
                courseId=course_id,
                chapterId=chapter_id
            ).aggregate(Max('chapterOrder'))['chapterOrder__max'] or 0
            
            video_order = WatchProgress.objects.filter(
                courseId=course_id,
                chapterId=chapter_id
            ).count()  # 간단하게 개수로 순서 결정
            
            # 인덱스 정보 계산
            chapter_index = chapter_order + 1
            video_index = video_order + 1
            
            progress = WatchProgress.objects.create(
                userId=user_id,
                courseId=course_id,
                chapterId=chapter_id,
                videoId=video_id,
                currentTime=data.get('currentTime', 0),
                totalDuration=data.get('totalDuration', 400),
                watchedPercentage=data.get('watchedPercentage', 0),
                isCompleted=data.get('isCompleted', False),
                totalWatchTime=data.get('totalWatchTime', 0),
                sessionCount=1,
                watchSpeed=data.get('watchSpeed', 1.0),
                chapterOrder=chapter_order,
                videoOrder=video_order,
                chapterIndex=chapter_index,
                videoIndex=video_index,
                completedAt=timezone.now() if data.get('isCompleted', False) else None
            )
        
        # 마지막 시청 위치 업데이트
        UserLastWatched.objects.update_or_create(
            userId=user_id,
            courseId=course_id,
            defaults={
                'lastChapterId': progress.chapterId,
                'lastVideoId': progress.videoId,
                'lastChapterOrder': progress.chapterOrder,
                'lastVideoOrder': progress.videoOrder,
                'lastChapterIndex': progress.chapterIndex,
                'lastVideoIndex': progress.videoIndex,
            }
        )
        
        return JsonResponse({
            'success': True,
            'created': created,
            'progress': {
                'userId': progress.userId,
                'courseId': progress.courseId,
                'chapterId': progress.chapterId,
                'videoId': progress.videoId,
                'chapterIndex': progress.chapterIndex,
                'videoIndex': progress.videoIndex,
                'currentTime': progress.currentTime,
                'totalDuration': progress.totalDuration,
                'watchedPercentage': progress.watchedPercentage,
                'isCompleted': progress.isCompleted,
                'sessionCount': progress.sessionCount,
            }
        })
        
    except Exception as e:
        print(f"Error in create_watch_progress: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_next_video(request):
    """새로운 비디오 순차 생성 (같은 챕터 내에서 다음 비디오 생성)"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        course_id = data.get('courseId')
        chapter_id = data.get('chapterId')
        
        if not all([user_id, course_id, chapter_id]):
            return JsonResponse({'error': 'userId, courseId, chapterId가 필요합니다'}, status=400)
        
        # 해당 챕터의 마지막 비디오 ID 찾기
        max_video_id = WatchProgress.objects.filter(
            courseId=course_id,
            chapterId=chapter_id
        ).aggregate(Max('videoId'))['videoId__max']
        
        # 새로운 비디오 ID 생성
        new_video_id = (max_video_id or (chapter_id * 100)) + 1
        
        # 비디오 순서 계산
        video_count = WatchProgress.objects.filter(
            courseId=course_id,
            chapterId=chapter_id
        ).count()
        
        # 챕터 정보 가져오기
        existing_chapter = WatchProgress.objects.filter(
            courseId=course_id,
            chapterId=chapter_id
        ).first()
        
        if existing_chapter:
            chapter_order = existing_chapter.chapterOrder
            chapter_index = existing_chapter.chapterIndex
        else:
            # 새로운 챕터인 경우
            max_chapter_order = WatchProgress.objects.filter(
                courseId=course_id
            ).aggregate(Max('chapterOrder'))['chapterOrder__max'] or -1
            chapter_order = max_chapter_order + 1
            chapter_index = chapter_order + 1
        
        # 중복 확인
        if WatchProgress.objects.filter(
            userId=user_id,
            courseId=course_id,
            chapterId=chapter_id,
            videoId=new_video_id
        ).exists():
            return JsonResponse({
                'error': f'비디오 {new_video_id}가 이미 존재합니다'
            }, status=400)
        
        # 새로운 비디오 생성
        progress = WatchProgress.objects.create(
            userId=user_id,
            courseId=course_id,
            chapterId=chapter_id,
            videoId=new_video_id,
            currentTime=0,
            totalDuration=data.get('totalDuration', 400),
            watchedPercentage=0,
            isCompleted=False,
            totalWatchTime=0,
            sessionCount=1,
            watchSpeed=data.get('watchSpeed', 1.0),
            chapterOrder=chapter_order,
            videoOrder=video_count,
            chapterIndex=chapter_index,
            videoIndex=video_count + 1
        )
        
        # 마지막 시청 위치 업데이트
        UserLastWatched.objects.update_or_create(
            userId=user_id,
            courseId=course_id,
            defaults={
                'lastChapterId': progress.chapterId,
                'lastVideoId': progress.videoId,
                'lastChapterOrder': progress.chapterOrder,
                'lastVideoOrder': progress.videoOrder,
                'lastChapterIndex': progress.chapterIndex,
                'lastVideoIndex': progress.videoIndex,
            }
        )
        
        return JsonResponse({
            'success': True,
            'created': True,
            'progress': {
                'userId': progress.userId,
                'courseId': progress.courseId,
                'chapterId': progress.chapterId,
                'videoId': progress.videoId,
                'chapterIndex': progress.chapterIndex,
                'videoIndex': progress.videoIndex,
                'currentTime': progress.currentTime,
                'totalDuration': progress.totalDuration,
            }
        })
        
    except Exception as e:
        print(f"Error in create_next_video: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def create_watch_progress(request):
    """시청 진행률 생성/업데이트"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        course_id = data.get('courseId')
        chapter_id = data.get('chapterId')
        video_id = data.get('videoId')
        
        if not all([user_id, course_id]):
            return JsonResponse({'error': 'userId와 courseId가 필요합니다'}, status=400)
        
        # chapterId와 videoId가 없으면 자동 생성
        if not chapter_id:
            # 기존 최대 챕터 ID + 1
            max_chapter = WatchProgress.objects.filter(courseId=course_id).aggregate(Max('chapterId'))['chapterId__max']
            chapter_id = (max_chapter or (course_id * 1000)) + 1
            
        if not video_id:
            # 해당 챕터의 최대 비디오 ID + 1
            max_video = WatchProgress.objects.filter(
                courseId=course_id, 
                chapterId=chapter_id
            ).aggregate(Max('videoId'))['videoId__max']
            video_id = (max_video or (chapter_id * 100)) + 1
        
        # 기존 진행률 찾기 또는 새로 생성
        try:
            progress = WatchProgress.objects.get(
                userId=user_id,
                courseId=course_id,
                chapterId=chapter_id,
                videoId=video_id
            )
            created = False
            
            # 기존 데이터 업데이트
            progress.currentTime = data.get('currentTime', progress.currentTime)
            progress.totalDuration = data.get('totalDuration', progress.totalDuration)
            progress.watchedPercentage = data.get('watchedPercentage', progress.watchedPercentage)
            progress.isCompleted = data.get('isCompleted', progress.isCompleted)
            progress.totalWatchTime = data.get('totalWatchTime', progress.totalWatchTime)
            progress.sessionCount += 1
            progress.watchSpeed = data.get('watchSpeed', progress.watchSpeed)
            
            if progress.isCompleted and not progress.completedAt:
                progress.completedAt = timezone.now()
            elif not progress.isCompleted:
                progress.completedAt = None
                
            progress.save()
            
        except WatchProgress.DoesNotExist:
            # 새로운 진행률 생성
            created = True
            
            # 순서 정보 계산
            chapter_order = WatchProgress.objects.filter(
                courseId=course_id,
                chapterId=chapter_id
            ).aggregate(Max('chapterOrder'))['chapterOrder__max'] or 0
            
            video_order = WatchProgress.objects.filter(
                courseId=course_id,
                chapterId=chapter_id
            ).count()  # 간단하게 개수로 순서 결정
            
            # 인덱스 정보 계산
            chapter_index = chapter_order + 1
            video_index = video_order + 1
            
            progress = WatchProgress.objects.create(
                userId=user_id,
                courseId=course_id,
                chapterId=chapter_id,
                videoId=video_id,
                currentTime=data.get('currentTime', 0),
                totalDuration=data.get('totalDuration', 400),
                watchedPercentage=data.get('watchedPercentage', 0),
                isCompleted=data.get('isCompleted', False),
                totalWatchTime=data.get('totalWatchTime', 0),
                sessionCount=1,
                watchSpeed=data.get('watchSpeed', 1.0),
                chapterOrder=chapter_order,
                videoOrder=video_order,
                chapterIndex=chapter_index,
                videoIndex=video_index,
                completedAt=timezone.now() if data.get('isCompleted', False) else None
            )
        
        # 마지막 시청 위치 업데이트
        UserLastWatched.objects.update_or_create(
            userId=user_id,
            courseId=course_id,
            defaults={
                'lastChapterId': progress.chapterId,
                'lastVideoId': progress.videoId,
                'lastChapterOrder': progress.chapterOrder,
                'lastVideoOrder': progress.videoOrder,
                'lastChapterIndex': progress.chapterIndex,
                'lastVideoIndex': progress.videoIndex,
            }
        )
        
        return JsonResponse({
            'success': True,
            'created': created,
            'progress': {
                'userId': progress.userId,
                'courseId': progress.courseId,
                'chapterId': progress.chapterId,
                'videoId': progress.videoId,
                'chapterIndex': progress.chapterIndex,
                'videoIndex': progress.videoIndex,
                'currentTime': progress.currentTime,
                'totalDuration': progress.totalDuration,
                'watchedPercentage': progress.watchedPercentage,
                'isCompleted': progress.isCompleted,
                'sessionCount': progress.sessionCount,
            }
        })
        
    except Exception as e:
        print(f"Error in create_watch_progress: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def watch_progress_detail(request, user_id, course_id, chapter_id):
    """특정 챕터의 시청 진행률 상세 조회"""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        progress_list = WatchProgress.objects.filter(
            userId=user_id,
            courseId=course_id,
            chapterId=chapter_id
        ).order_by('videoOrder').values(
            'userId', 'courseId', 'chapterId', 'videoId',
            'chapterOrder', 'videoOrder', 'chapterIndex', 'videoIndex',
            'currentTime', 'totalDuration', 'watchedPercentage', 'isCompleted',
            'totalWatchTime', 'sessionCount', 'watchSpeed',
            'firstWatchedAt', 'lastWatchedAt', 'completedAt'
        )
        
        return JsonResponse({
            'userId': user_id,
            'courseId': course_id,
            'chapterId': chapter_id,
            'videos': list(progress_list)
        })
        
    except Exception as e:
        print(f"Error in watch_progress_detail: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    """개별 챕터 진행률 조회"""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        wp = WatchProgress.objects.get(
            user_id=user_id,
            course_id=course_id,
            chapter_id=chapter_id
        )
        
        return JsonResponse({
            'userId': wp.user_id,
            'courseId': wp.course_id,
            'chapterId': wp.chapter_id,
            'currentTime': wp.current_time,
            'totalDuration': wp.total_duration,
            'watchedPercentage': wp.watched_percentage,
            'isCompleted': wp.is_completed,
        })
    except WatchProgress.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)