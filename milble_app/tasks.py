from celery import shared_task
from .models import Post, CustomUser  # CustomUser 모델을 사용한다고 가정

@shared_task
def handle_like_action(post_id, user_id, liked):
    try:
        print("celery ok")
        post = Post.objects.get(id=post_id)
        user = CustomUser.objects.get(id=user_id)

        if liked:
            # 좋아요 추가
            post.liked_users.add(user)
        else:
            # 좋아요 취소
            post.liked_users.remove(user)

        # 좋아요 수 업데이트
        post.likes = post.liked_users.count()
        post.save()
        
        print("save ok")

    except Post.DoesNotExist:
        print(f"Post with ID {post_id} does not exist.")
    except CustomUser.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
