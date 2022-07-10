"""seproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from etune import views
from etune.views import*
import private_storage.urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('login',login,name="login"),
    path('accounts/', include('allauth.urls')),
    path('tts',test2,name="test"),
    path('loginn2',login,name="test2"),
    path('logout',log_user_out,name="logout"),
    path('home',views.home,name="home"),
    path('information',views.information,name="information"), #หน้าสร้างข่าวประชาสัมพันธ์
    path('viewpost/<int:id_post>',views.viewpost,name="viewpost"),#หน้าดูข่าวประชาสัมพันธ์แต่ละทุน
    path('CreateScholar',views.CreateScholar,name="CreateScholar"),#หน้าสร้างข่าวทุน
    path('editScholar/<int:order_id>',views.editScholar,name="editScholar"),#แก้ไขทุนการศึกษา
    path('InformationHome',views.InformationHome,name="InformationHome"),#หน้าข่าวประชาสัมพันธ์ของ admin
    path('viewInfomation/<int:order_id>',views.viewInfomation,name="viewInfomation"),#หน้าข่าวประชาสัมพันธ์ต่อจาก InformationHome
    path('editInfomation/<int:edit_id>',views.editInfomation,name="editInfomation"), #หน้าแก้ไขข่าวประประชาสัมพันธ์ของ admin
    path('addEditInfomation',views.addEditInfomation,name="addEditInfomation"), #เป็นหน้าที่หลังจากกดปุ่มแก้ไขค่าแล้ว
    path('viewHome/<int:home_id>/<int:user_id>',views.viewHome,name="viewHome"), #หน้าต่อจากหน้า home ของ admin
    path('manageCommitteeHome',views.manageCommitteeHome,name="manageCommitteeHome"),  #หน้าจัดการรายชื่อคณะกรรมการของ admin
    path('delmanageCommitteeHome/<int:user_id>',views.delmanageCommitteeHome,name="delmanageCommitteeHome"),  #ลบรายชื่อ admin
    path('viewManageCommitteeHome/<int:home_id>',views.viewManageCommitteeHome,name="viewManageCommitteeHome"),
    path('addCommittee',views.addCommittee,name="addCommittee"),
    path('scholarScore',views.viewScore,name="scholarScore"), # แบบฟอร์มการสัมภาษณ์(admin) 1
    path('scholarWeightScore/<int:id_info>',views.viewWightScore,name="scholarWeightScore"), # แบบฟอร์มการสัมภาษณ์(admin) 2
    path('profileHistoryNisit',views.profileHistoryNisit,name="profileHistoryNisit"),# แบบฟอร์มของนิสิตสำหรับเข้าครั้งแรก
    path('editHistoryNisit',views.editHistoryNisit,name="editHistoryNisit"),  #แก้ไขข้อมูลแบบฟอร์มของนิสิต
    path('statusNisit',views.statusNisit,name="statusNisit"),  #ประวัติคำร้องนิสิต
    path('checkInfo/<int:info_id>',views.checkInfo,name="checkInfo"),  #ตรวจสอบข้อมูลก่อนสมัครทุน
    path('interview',views.interview,name="interview"), #สัมภาษณ์
    path('historyGetScholar',views.historyGetScholar,name="historyGetScholar"), #ประวัติรายชื่อผู้ได้รับทุน
    path('firstAppilcationAdmin',views.firstAppilcationAdmin,name="firstAppilcationAdmin"), #รายชื่อทุนแต่ละทุน สำหรับตรวจสอบรายชื่อนิสิต(admin) 1
    path('secondAppilcationAdmin/<int:home_id>',views.secondAppilcationAdmin,name="secondAppilcationAdmin"), #รายชื่อนิสิตในทุนนั้นๆ สำหรับตรวจสอบรายชื่อนิสิต(admin) 2
    path('interviewStudent/<int:info_id>',views.interviewStudent,name="interviewStudent"),
    path('interviewStudentTest/<int:info_id>/<int:user_id>',views.interviewStudentTest,name="interviewStudentTest"),
    path('checkStatus/<int:home_id>/<int:user_id>',views.checkStatus,name="checkStatus"), #เช็คสถานะนิสิต
    path('delApp/<int:home_id>/<int:user_id>',views.delApp,name="delApp"), #ลบใบสมัคร
    path('changeStatus/<int:home_id>/<int:user_id>/<int:status>',views.changeStatus,name="changeStatus"), #สำหรับเปลี่ยนสถานะ 21 20 31 30 41
    #path('historyGetScholarFind',views.historyGetScholarFind,name="historyGetScholarFind"),
    path('limitaccount',views.limitaccount,name="limitaccount"),
    path('payment/<int:info_id>',views.payment,name = "payment"),
    path('removeScholar/<int:info_id>',views.removeScholar,name="removeScholar"),
    path('removeInformation/<int:news_id>',views.removeInformation,name="removeInformation"),
    path('pdf_genScholar/<int:info_id>',views.pdf_genScholar,name="pdf_genScholar"),
    path('checkInfoAdmin/<int:home_id>/<int:user_id>',views.checkInfoAdmin,name="checkInfoAdmin"),
    path('payment_admin/<int:home_id>/<int:user_id>',views.payment_admin,name="payment_admin"),
    path('editPayment/<int:info_id>/<int:user_id>',views.editPayment,name="editPayment"),
    ]

urlpatterns += [
    re_path('^private-media/', include(private_storage.urls)),
    
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)