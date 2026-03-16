from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, CheckInRecord, CheckOutRequest
from django.urls import reverse
import datetime


class UserProfileTest(TestCase):
    """测试用户档案模型和权限"""

    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(username='teststudent', password='test123456')
        self.profile = UserProfile.objects.create(user=self.user, role='student', student_id='S123456')

        self.admin_user = User.objects.create_user(username='testadmin', password='admin123456')
        self.admin_profile = UserProfile.objects.create(user=self.admin_user, role='admin',
                                                        admin_department='Accommodation')

    def test_user_role(self):
        """测试用户角色是否正确"""
        self.assertEqual(self.profile.role, 'student')
        self.assertEqual(self.admin_profile.role, 'admin')
        self.assertEqual(self.profile.get_role_display(), 'Student')

    def test_student_dashboard_access(self):
        """测试学生只能访问自己的仪表盘"""
        client = Client()
        client.login(username='teststudent', password='test123456')
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Dashboard')


class CheckOutRequestTest(TestCase):
    """测试退房申请模型"""

    def setUp(self):
        # 创建测试数据
        self.user = User.objects.create_user(username='teststudent', password='test123456')
        self.profile = UserProfile.objects.create(user=self.user, role='student', student_id='S123456')
        self.check_in = CheckInRecord.objects.create(student=self.profile, room_number='A101',
                                                     check_in_date=datetime.date.today())
        self.check_out = CheckOutRequest.objects.create(
            student=self.profile,
            check_in_record=self.check_in,
            requested_check_out_date=datetime.date.today() + datetime.timedelta(days=7)
        )

    def test_check_out_status(self):
        """测试退房申请默认状态"""
        self.assertEqual(self.check_out.status, 'pending')
        # 修改状态
        self.check_out.status = 'approved'
        self.check_out.save()
        self.assertEqual(self.check_out.get_status_display(), 'Approved')