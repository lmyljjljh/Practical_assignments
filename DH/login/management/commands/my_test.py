# coding=utf-8
import concurrent.futures

from login.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "创建30000个用户测试性能优化"

    def handle(self, *args, **options):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [
                executor.submit(
                    User.objects.create,
                    username=f'user{i:05d}',
                    phone_number=f'user{i:05d}',
                    password='123456',
                    email=f'user{i:05d}@mail.example',
                ) for i in range(30000)
            ]
            concurrent.futures.wait(futures)
