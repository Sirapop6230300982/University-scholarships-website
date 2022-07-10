from django.conf import settings
from django.db import models
from private_storage.fields import PrivateFileField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from tinymce.models import HTMLField
#from ckeditor_uploader.fields import RichTextUploadingField
#from ckeditor.fields import RichTextField


import os



class Scholar_news (models.Model):          #Database สำหรับข่าวประชาสัมพันธ์ท้งหมด
    sn_header = models.CharField(max_length=256)
    sn_description = HTMLField() #text
    sn_expire_date = models.DateField() #วันที่
    sn_photo_bg = ResizedImageField(upload_to='uploads/',size=[1280, 720], crop=['middle', 'center'],quality=100)
    sn_path_to_pdf = models.FileField(upload_to='documents/') #pdf
    sn_create_time = models.DateField(default=timezone.now)
    sn_status = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-sn_create_time']

    def __str__(self):
        return str(self.sn_header)


class Scholar_info (models.Model):           #Database สำหรับข่าวรับทุนทั้งหมด
    
    si_name	= models.CharField(max_length=256)
    si_description	= models.TextField()
    si_description = HTMLField(blank=True,null=True)
    
    si_total_amount	= models.IntegerField() #จำนวนเงินทั้งหมด
    si_individual_amount = models.IntegerField() #เงินหารเฉลี่ยต่อคน
    si_max_scholar	= models.IntegerField() #จำนวนคนที่ได้รับ
    si_remain_scholar = models.IntegerField() #จำนวนเงินทุนที่เหลือปัจจุบัน
    si_source	 = models.CharField(max_length=256) #ภายนอก/ใน
    si_source_name	= models.CharField(null=True,blank=True,max_length=500) #ผู้ให้ทุน
    si_note	= models.TextField()	
    si_grade_require = 	models.FloatField(null=True)
    si_create_time = models.DateField(default=timezone.now)
    si_expire_time = models.DateField()
    si_year = models.CharField(max_length=4)
    si_semester = models.IntegerField()
    si_photo_bg = ResizedImageField(upload_to='uploads/info',size=[1280, 720], crop=['middle', 'center'],quality=100)
    si_path_to_pdf = models.FileField(upload_to='documents/info')
    si_status = models.IntegerField(default=0) #แสดงสถานะการดำเนินงานทุนนิสิต
    si_endtime = models.DateField(null=True,blank=True) #วันหมดการแสดงของแอดมิน
    class Meta:
        ordering = ['si_expire_time']


    def __str__(self):
        return str(self.si_name)
    

class add_commit(models.Model):     #Database เพิ่มรายชื่อกรรมการ
    ac_email	=  models.CharField(max_length=256)
    ac_firstname =  models.CharField(max_length=256)
    ac_lastname = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.ac_firstname)

class add_scholar_Commit(models.Model):     #Database เพิ่มทุนให้กรรมการ
    id_commit = models.ForeignKey(User, on_delete=models.CASCADE) #id ของกรรมการ
    Scholar_name = models.ForeignKey(Scholar_info,on_delete=models.CASCADE) #id ของทุน
    def __str__(self):
        return str(str(self.id_commit)+" เข้าถึงทุน"+str(self.Scholar_name))

    
class Scholar_weight_score(models.Model): #สร้างแบบฟอร์มการให้คะแนนสัมภาษณ์
    sws_si_id = models.OneToOneField(Scholar_info,on_delete=models.CASCADE)
    sws_info = models.JSONField()
    sws_date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sws_date']

    def __str__(self):
        return str(self.sws_si_id)



class Scholar_profile(models.Model): #กรอกแบบฟอร์มนิสิต
    sp_userid = models.OneToOneField(User,on_delete=models.CASCADE)
    sp_advisor_professor =  models.CharField(max_length=64,null=True) #อาจารย์ที่ปรึกษา
    sp_status = models.IntegerField(null=True) #status
    sp_title_en	= models.CharField(max_length=10,null=True) #Title English
    sp_firstname_en	= models.CharField(max_length=64,null=True) #	Firstname English
    sp_middlename_en = models.CharField(max_length=64,null=True)	#Middlename English
    sp_lastname_en = models.CharField(max_length=64,null=True) #lastname English
    sp_std_code	= models.CharField(max_length=10,null=True) #Student ID
    sp_title_th	= models.CharField(max_length=10,null=True) #Title Thai
    sp_firstname_th	= models.CharField(max_length=64,null=True) #	Firstname Thai
    sp_middlename_th = models.CharField(max_length=64,null=True)	#Middlename Thai
    sp_lastname_th = models.CharField(max_length=64,null=True)	#Lastname Thai
    sp_date_of_birth = 	models.DateField(default=timezone.now) #date of birth
    sp_major = models.CharField(max_length=4,null=True) #major
    sp_grade = models.CharField(max_length=4,null=True) #grade
    # sp_path_to_pdf_json	= models.JSONField(null=True) #path to pdf file in json 
    sp_std_address = models.JSONField(null=True) #address
    sp_std_tel_no = models.CharField(max_length=10,null=True) #tel

    #บิดา
    sp_father_title = models.CharField(max_length=10,null=True)    #คำนำหน้า
    sp_father_firstname	= models.CharField(max_length=64,null=True) #firstname dad
    sp_father_middlename = models.CharField(max_length=64,null=True) #middlename dad 
    sp_father_lastname = models.CharField(max_length=64,null=True) #lastname dad
    sp_father_date_of_birth = models.DateField(default=timezone.now)    #วันเกิด
    sp_father_age = models.IntegerField(blank=True,null=True)   #อายุ
    sp_father_status_married = models.CharField(max_length=64,null=True)  #สถานะสมรส
    sp_father_statuslife = models.CharField(max_length=64,null=True)  #สถานะการมีชีวิตอยู่
    sp_father_income = models.IntegerField(blank=True,null=True) #รายได้ต่อเดือน
    sp_father_career = models.CharField(max_length=64,null=True)#อาชีพ
    sp_father_workplace = models.CharField(max_length=128,null=True)#สถานที่ประกอบการ
    sp_father_address = models.JSONField(null=True) #address dad
    sp_father_tel_no = models.CharField(max_length=10,null=True) #Tel dad

    #มารดา
    sp_mother_title = models.CharField(max_length=10,null=True)    #คำนำหน้า
    sp_mother_firstname	= models.CharField(max_length=64,null=True) #firstname mom
    sp_mother_middlename = models.CharField(max_length=64,null=True) #middlename mom
    sp_mother_lastname = models.CharField(max_length=64,null=True) #lastname mom
    sp_mother_address = models.JSONField(null=True) #address mom
    sp_mother_date_of_birth = models.DateField(default=timezone.now)#วันเกิด
    sp_mother_age = models.IntegerField(blank=True,null=True)   #อายุ
    sp_mother_status_married = models.CharField(max_length=64,null=True) #สถานะสมรส
    sp_mother_statuslife = models.CharField(max_length=64,null=True)  #สถานะการมีชีวิตอยู่
    sp_mother_income = models.IntegerField(blank=True,null=True) #รายได้ต่อเดือน
    sp_mother_career = models.CharField(max_length=64,null=True) #อาชีพ
    sp_mother_workplace = models.CharField(max_length=128,null=True)  #สถานที่ประกอบการ
    sp_mother_tel_no = models.CharField(max_length=10,null=True) #Tel mom
    
    #พี่น้อง
    sp_bro_n_sis = models.JSONField(null=True) #ชื่อพี่น้องการศึกษาอาชีพสถานที่ประกอบการ

    #เกี่ยวกับนิสิตและผู้ปกครอง
    sp_loan = models.CharField(max_length=32,null=True) #which are you loan?(กรอ,กยศ,ไม่เคยกู้)
    sp_income = models.IntegerField(blank=True,null=True) #moneyPerMonth 
    sp_income_source = models.CharField(max_length=32,null=True) #income source
    sp_patron_relation = models.CharField(max_length=32,null=True) #patron relation
    sp_patron_career = models.CharField(max_length=64,null=True) #patron career
    sp_patron_tel_no = models.CharField(max_length=64,null=True) #patron tel
    sp_patron_workplace = models.JSONField(null=True) #patron workplace
    sp_child_in_the_patron = models.IntegerField(blank=True,null=True) #child in the patron
    sp_parttime	= models.CharField(max_length=10,null=True) #Have you ever worked part time?
    sp_parttime_income = models.IntegerField(blank=True,null=True) #parttime income
    sp_parttime_type = models.CharField(max_length=128,null=True)	#parttime type

    #ทุนที่เคยได้รับ
    sp_json_scholar = models.JSONField(null=True)

    #เขียนรายละเอียดเพิ่มเติม
    sp_report = models.TextField(null=True) #detail
    


    def __str__(self):
        return str(self.sp_userid)

class File_Models(models.Model):
    fm_upload_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    fm_Scholar = models.ForeignKey(Scholar_info,on_delete=models.CASCADE)
    fm_file = PrivateFileField("File",null=True,blank=True)
    fm_state = models.IntegerField(default=0)

    def __str__(self):
        return str(self.fm_upload_by)+" "+str(self.fm_Scholar)


class Scholar_app(models.Model):
    sa_userid = models.ForeignKey(User,on_delete=models.CASCADE) 
    sa_si_id = models.ForeignKey(Scholar_info,on_delete=models.CASCADE) #id ทุน
    sa_status =	models.IntegerField(default=11)	#สถานะการยื่นทุน 11=ผ่านรอบยื่นเอกสาร 20=เจ้าหน้าที่ตรวจสอบเอกสารไม่ผ่าน 21=เจ้าหน้าที่ตรวจสอบเอกสารผ่าน 30=ไม่ผ่านการคัดเลือกสอบสัมภาษณ์ 31=ผ่านการคัดเลือกสอบสัมภาษณ์ 41=รับเงินทุนสนับสนุนการศึกษา
    sa_statusExDate = models.DateField(default=timezone.now)
    sa_score = models.FloatField(default=0) #คะแนนเฉลี่ยรวม(คะเเนนสอบสัมภาษณ์)
    sa_person = models.IntegerField(default=1)
    sa_score_info =	models.JSONField()  #คะแนนรายข้อ(คะเเนนสอบสัมภาษณ์)

    #ข้อมูลส่วนตัว
    sa_advisor_professor =  models.CharField(max_length=64,) #อาจารย์ที่ปรึกษา
    sa_title_en	= models.CharField(max_length=10,) #Title English
    sa_firstname_en	= models.CharField(max_length=64,) #	Firstname English
    sa_middlename_en = models.CharField(max_length=64,)	#Middlename English
    sa_lastname_en = models.CharField(max_length=64,) #lastname English
    sa_std_code	= models.CharField(max_length=10,) #Student ID
    sa_title_th	= models.CharField(max_length=10,) #Title Thai
    sa_firstname_th	= models.CharField(max_length=64,) #	Firstname Thai
    sa_middlename_th = models.CharField(max_length=64,)	#Middlename Thai
    sa_lastname_th = models.CharField(max_length=64,)	#Lastname Thai
    sa_date_of_birth = 	models.DateField(default=timezone.now) #date of birth
    sa_major = models.CharField(max_length=4,) #major
    sa_grade = models.CharField(max_length=4,) #grade
    sa_path_to_pdf_json	= models.JSONField() #path to pdf file in json 
    sa_std_address = models.JSONField() #address
    sa_std_tel_no = models.CharField(max_length=10,) #tel

    #บิดา
    sa_father_title = models.CharField(max_length=10,)    #คำนำหน้า
    sa_father_firstname	= models.CharField(max_length=64,) #firstname dad
    sa_father_middlename = models.CharField(max_length=64,) #middlename dad 
    sa_father_lastname = models.CharField(max_length=64,) #lastname dad
    sa_father_date_of_birth = models.DateField(default=timezone.now,)    #วันเกิด
    sa_father_age = models.IntegerField()   #อายุ
    sa_father_status_married = models.CharField(max_length=64,)  #สถานะสมรส
    sa_father_statuslife = models.CharField(max_length=64,)  #สถานะการมีชีวิตอยู่
    sa_father_income = models.IntegerField() #รายได้ต่อเดือน
    sa_father_career = models.CharField(max_length=64,)#อาชีพ
    sa_father_workplace = models.CharField(max_length=128,)#สถานที่ประกอบการ
    sa_father_address = models.JSONField() #address dad
    sa_father_tel_no = models.CharField(max_length=10,) #Tel dad

    #มารดา
    sa_mother_title = models.CharField(max_length=10,)    #คำนำหน้า
    sa_mother_firstname	= models.CharField(max_length=64,) #firstname mom
    sa_mother_middlename = models.CharField(max_length=64,) #middlename mom
    sa_mother_lastname = models.CharField(max_length=64,) #lastname mom
    sa_mother_address = models.JSONField() #address mom
    sa_mother_date_of_birth = models.DateField(default=timezone.now,)#วันเกิด
    sa_mother_age = models.IntegerField()   #อายุ
    sa_mother_status_married = models.CharField(max_length=64,) #สถานะสมรส
    sa_mother_statuslife = models.CharField(max_length=64,)  #สถานะการมีชีวิตอยู่
    sa_mother_income = models.IntegerField() #รายได้ต่อเดือน
    sa_mother_career = models.CharField(max_length=64,) #อาชีพ
    sa_mother_workplace = models.CharField(max_length=128,)  #สถานที่ประกอบการ
    sa_mother_tel_no = models.CharField(max_length=10,) #Tel mom
    
    #พี่น้อง
    sa_bro_n_sis = models.JSONField() #ชื่อพี่น้องการศึกษาอาชีพสถานที่ประกอบการ

    #เกี่ยวกับนิสิตและผู้ปกครอง
    sa_loan = models.CharField(max_length=32,) #which are you loan?(กรอ,กยศ,ไม่เคยกู้)
    sa_income = models.IntegerField() #moneyPerMonth 
    sa_income_source = models.CharField(max_length=32,) #income source
    sa_patron_relation = models.CharField(max_length=32,) #patron relation
    sa_patron_career = models.CharField(max_length=64,) #patron career
    sa_patron_tel_no = models.CharField(max_length=64,) #patron tel
    sa_patron_workplace = models.JSONField() #patron workplace
    sa_child_in_the_patron = models.IntegerField() #child in the patron
    sa_parttime	= models.CharField(max_length=10,) #Have you ever worked part time?
    sa_parttime_income = models.IntegerField() #parttime income
    sa_parttime_type = models.CharField(max_length=128,)	#parttime type

    #ทุนที่เคยได้รับ
    sa_json_scholar = models.JSONField()

    #เขียนรายละเอียดเพิ่มเติม
    # sa_report = models.TextField() #detail
    #ได้รับการสอบสัมภาษณ์หรือยัง+

    sa_json_commit = models.JSONField(null=True,default={})

    class Meta:
        ordering = ['-sa_score']

    def __str__(self):
        return str(self.sa_userid)+" สมัครทุน "+str(self.sa_si_id)
    
class avatar_profile (models.Model):
    sa_userid = models.OneToOneField(User,on_delete=models.CASCADE) 
    sp_path_to_avatar = ResizedImageField(upload_to='uploads/avatar',size=[300, 300], crop=['middle', 'center'],quality=100,default="noimg.png")	#	path to avatar

    def __str__(self):
        return str(self.sa_userid)

class Log_score (models.Model):
    ls_commit = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_requests_created') 
    ls_student = models.ForeignKey(User,on_delete=models.CASCADE) 
    ls_Scholar = models.ForeignKey(Scholar_info,on_delete=models.CASCADE)
    score = models.JSONField()
    

    def __str__(self):
        return str(self.ls_commit) +" ให้คะแนน "+ str(self.ls_student) + " ในทุน " + str(self.ls_Scholar)