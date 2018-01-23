from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.message

# 一个创建一个实例对象，一个创建对象
    @staticmethod
    def send_message(from_user, to_user, message):
        message = message[:1000]
        current_user_message = Message(
            from_user=from_user,
            message=message,
            user=from_user,
            conversation=to_user,
            is_read=True
        )
        current_user_message.save()
        Message(
            from_user=from_user,
            conversation=from_user,
            message=message,
            user=to_user
        ).save()
        return current_user_message

# values 返回字典，不是实例 annotate 查询表达式
    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(user=user).values(
            'conversation').annotate(last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            unread = Message.objects.filter(
                user=user,
                is_read=False,
                conversation__pk=conversation['conversation'],
            ).count()  # 一个数

            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': unread,
            })
        return users  # 返回字典的列表
