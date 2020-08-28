from django.test import TestCase,Client
from .models import User

class usertestcase(TestCase):
    def setUp(self):      #这是用于创建数据的
        User.objects.create(
            name='qwe',
            password='123123qweqwe',
        )

    def test_login_url(self):    #测试登录
        c=Client()
        response=c.post('/user/login/',{'name':'qwe','password':'123123qweqwe'})
        self.assertEqual(response.status_code,200)
# Create your tests here.
