from django.http import request
import requests
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import * 
from .models import *
import math
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

from datetime import date,datetime
from datetime import timedelta  
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator , EmptyPage ,InvalidPage
import json as js
from django.contrib.auth.decorators import user_passes_test

from django.http import JsonResponse






# from allauth.socialaccount.adaptor import DefaultSocialAccountAdapter

# import json as js

# # Create your views here.

# class MySocialAccount(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         u = sociallogin.account.user
#         if not u.email.split('@')[1] == "ku.th":
#             raise ImmediateHttpResponse(render_to_response('error.html'))



def index(request):         #หน้าข่าวประชาสัมพันธ์หน้าแรกก่อนเข้า login 
    file_my = None 
    data= Scholar_news.objects.all()
    time = datetime.now()
    for i in data:
        dateNew = datetime.fromisoformat(str(i.sn_expire_date)).timestamp()
        dateToday = datetime.fromisoformat(str(time)).timestamp()
        if dateNew <= dateToday:
            Scholar_news.objects.filter(sn_header=i.sn_header).update(sn_status = 1)   

    news = Scholar_news.objects.exclude(sn_status = 1)
    return render(request, 'index/index2.html',{'files':file_my,'news':news})

def login(request):
    file_my = None
    if request.user.is_authenticated:
        file_my = MyModel.objects.filter(upload_by=request.user.id)
        
    news = Scholar_news.objects.all()
    return render(request, 'index/login.html',{'files':file_my,'news':news})
    



def test2(request):
    return render(request,'t.html',{'test':'<h2>HELLOWORLD</h2><br><h6>this is h 6 </h6>'})

def log_user_out(request):
    logout(request)
    return redirect('/')

@login_required (login_url='index')
def home(request):                  #หน้าหลังจาก login ของทุกคน
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]
    findInfo = ""
    if request.method == 'POST': 
        findInfo = request.POST['findInfo']
   
   
    data= Scholar_info.objects.all()
    time = datetime.now()
    for i in data:
        dateInfo = datetime.fromisoformat(str(i.si_expire_time)).timestamp()
        dateToday = datetime.fromisoformat(str(time)).timestamp()
        if dateInfo <= dateToday:
            Scholar_info.objects.filter(id=i.id).update(si_status = 1) 
    
    apps = Scholar_app.objects.filter(sa_status = 41)
    for app in apps:
        Scholar_info.objects.filter(id=app.sa_si_id.id).update(si_status = 2) 

    news = Scholar_info.objects.exclude(si_status = 2)
    if findInfo != "":
        news = news.filter(si_name__contains = findInfo)
    paginator = Paginator(news,4)
    

    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        newsperPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        newsperPage = paginator.page(paginator.num_pages)
    
    return render(request,'home-std.html',{'scholars': newsperPage})
    
@user_passes_test(lambda u: u.is_superuser)
def information(request):           #หน้าสร้างข่าวประชาสัมพันธ์ของ admin
    if request.method == 'POST':  
        head_news = request.POST['head_news']
        detail_news = request.POST['detail_news']
        date_news = request.POST['date_news']

        img = None
        file_to = None
        if request.FILES.get('images_news'):
            img =  request.FILES.get('images_news')
        if request.FILES.get('file_news'):
            file_to = request.FILES.get('file_news')

        
        data = Scholar_news.objects.create(
        sn_header = head_news,
        sn_description = detail_news,
        sn_expire_date = date_news,
        sn_photo_bg = img,
        sn_path_to_pdf = file_to
        )
        data.save()
        messages.success(request, 'สร้างประชาสัมพันธ์แล้ว')
        return redirect('InformationHome')
    return render(request,'Create_Admin/information.html')


def viewpost(request,id_post):              #หน้าดูรายละเอียดเพิ่มเติมของหน้า index
    news = Scholar_news.objects.filter(id=id_post)
    return render(request,'index/view-post.html',{'news':news})

@user_passes_test(lambda u: u.is_superuser)
def CreateScholar (request):                #หน้าสร้างประกาศรับทุน admin
    if request.method == 'POST':
        name_scholar = request.POST['name_scholar']
        detail = request.POST['mytextarea']
        amount = request.POST['amount']
        amount_per_person = request.POST['amount_per_person']
        if int(amount_per_person) >= int(amount):
            messages.error(request, "จำนวนเงินต่อคนมากกว่าจำนวนเงินทั้งหมดไม่ได้")
            return redirect("CreateScholar")
        total = math.floor(int(amount)/int(amount_per_person))
        
        date_e = request.POST['date_news']
        option = request.POST['option']
        namelst = request.POST.getlist('text[]')
        type_scholar=request.POST['type_scholar']
        news = request.POST.get('news',None)  
        year = request.POST['year']
        year = int(year)
        if year>2400:
            year = year - 543
            year = str(year)

        file_to = None
        img =None
        if request.FILES.get('img'):
            img =  request.FILES.get('img')
        if request.FILES.get('file_t'):
            file_to = request.FILES.get('file_t')

        name_db =""
        
        for i in range(len(namelst)):
            if namelst[i] != "" :
                if i == len(namelst)-2:
                    name_db += str(namelst[i])
                else:   
                    name_db += str(namelst[i]) + ","
            
     
        data = Scholar_info.objects.create(
            si_name =name_scholar,
            si_description = detail,
            si_total_amount = amount,
            si_individual_amount =amount_per_person,
            si_max_scholar = total,
            si_remain_scholar = total,
            si_source =type_scholar,
            si_source_name =name_db,
            si_photo_bg =  img,
            si_path_to_pdf= file_to,
            si_note =option,
            si_expire_time =date_e,
            #si_year = datetime.date.today().year,
            si_year= year,
            si_semester = 2
        ) 
        data.save()
        
        weight = Scholar_weight_score.objects.create(sws_si_id=data,sws_info={'หัวข้อที่1':'0'})
        weight.save()


        if news == "1" :
            data = Scholar_news.objects.create(
            sn_header = name_scholar,
            sn_description = detail,
            sn_expire_date = date_e,
            sn_photo_bg = img,
            sn_path_to_pdf = file_to
            )
            data.save()
            messages.success(request, "เพิ่มในข่าวหน้าประชาสัมพัมธ์เรียบร้อยแล้ว")
        messages.success(request, "สร้างทุนเรียบร้อยแล้ว")
        return redirect("home")
        #return JsonResponse({"result":"สร้างเรียบร้อยแล้วพ่อหนุ่ม"})
    #form = Contents()

    return render(request,'Create_Admin/CreateScholar.html')
    
@login_required (login_url='index')
def editScholar(request,order_id):
    if request.method == 'POST':
        name_scholar_text = request.POST['name_scholar']
        detail = request.POST['mytextarea']
        amount = request.POST['amount']
        amount_per_person = request.POST['amount_per_person']
        if int(amount_per_person) >= int(amount):
            print("HELLOWORLD")
            messages.error(request, "จำนวนเงินต่อคนมากกว่าจำนวนเงินทั้งหมดไม่ได้")
            return redirect("/editScholar/"+str(order_id))

        total = math.floor(int(amount)/int(amount_per_person))
        date_e = request.POST['date_news']
        option = request.POST['option']
        namelst = request.POST.getlist('text[]')
        type_scholar=request.POST['type_scholar']
        news = request.POST.get('news',None)  
        year = request.POST['year']
        year = int(year)
        if year>2500:
            year = year - 543
            year = str(year)
        keys =[]
        
        for i in range(len(namelst)):
            keys.append(str("ผู้สนับสนุนทุนท่านที่ ")+str(i+1))

        
        name_db =""
        
        for i in range(len(namelst)):
            if namelst[i] != "" :
                if i == len(namelst)-2:
                    name_db += str(namelst[i])
                else:   
                    name_db += str(namelst[i]) + ","


        name_scholar_obj = Scholar_info.objects.filter(id=order_id)
        name_scholar_obj = name_scholar_obj[0].si_name
        bool_name_news = Scholar_news.objects.filter(sn_header=name_scholar_obj).exists()

        data = Scholar_info.objects.filter(id=order_id).update(
            si_name =name_scholar_text,
            si_description = detail,
            si_total_amount = amount,
            si_individual_amount =amount_per_person,
            si_max_scholar = total,
            si_remain_scholar = total,
            si_source =type_scholar,
            si_source_name =name_db,
            si_note =option,
            si_expire_time =date_e,
           # si_year = datetime.date.today().year,
            si_year =year,
            si_semester = 2
            
        )
        

        if len(request.FILES)!=0:
                if request.FILES.get('img',False):
                    data2 = Scholar_info.objects.get(id=order_id)
                    data2.si_photo_bg = request.FILES.get('img')
                    data2.save()

                if request.FILES.get('file_t',False):
                    data2 = Scholar_info.objects.get(id=order_id)
                    data2.si_path_to_pdf = request.FILES.get('file_t')
                    data2.save()  


        if bool_name_news :
            data = Scholar_news.objects.filter(sn_header=name_scholar_obj).update(
            sn_header = name_scholar_text,
            sn_description = detail,
            sn_expire_date = date_e,
            )

            if request.FILES.get('img',False):
                data = Scholar_news.objects.get(sn_header=name_scholar_obj)
                data.sn_photo_bg = request.FILES.get('img')
                data.save()

            if request.FILES.get('file_t',False):
                data = Scholar_news.objects.filter(sn_header=name_scholar_obj).update
                data.sn_path_to_pdf = request.FILES.get('file_t')
                data.save()
            
                
                
            messages.success(request, "แก้ไขข่าวหน้าประชาสัมพัมธ์เรียบร้อยแล้ว")
        messages.success(request, "แก้ไขทุนเรียบร้อยแล้ว")
        return redirect('home')
    scholar_info = Scholar_info.objects.filter(id=order_id)  
    scholar_info = scholar_info[0]
    json = scholar_info.si_source_name
    json = json.split(",")
    print(json)
    return render(request,'Create_Admin/editScholar.html',{'scholar_info':scholar_info,'json':json})

    

@login_required (login_url='index')

def InformationHome(request):  
    news = Scholar_news.objects.filter(sn_status=0)
    findNews = ""
    if request.method == "POST":
        findNews = request.POST['findnews']
    if findNews != "":
        news = news.filter(sn_header__contains = findNews)
    
    paginator = Paginator(news,4)  

    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        newsperPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        newsperPage = paginator.page(paginator.num_pages)

    return render(request,'informationNews_Admin/informationhome.html',{'info':newsperPage})

@login_required (login_url='index')
def viewInfomation(request,order_id):       #หน้าดูข่าวสารของ admin
    news = Scholar_news.objects.filter(id=order_id)
    if news[0].sn_status == 1:
        return redirect('InformationHome')
    
    return render(request,'informationNews_Admin/view-Infomation.html',{'news': news})

@user_passes_test(lambda u: u.is_superuser)
def editInfomation(request,edit_id):       #หน้าแก้ไขข่าวประชาสัมพันธ์ของ admin
    if request.method == 'POST':  
        
        head_news = request.POST['head_news']
        detail_news = request.POST['detail_news']
        date_news = request.POST['date_news']
        news_obj = Scholar_news.objects.filter(id=edit_id).update(
            sn_header = head_news,
            sn_description = detail_news,
            sn_expire_date = date_news,
        )
        if request.FILES.get('images_news') != None:
            img = request.FILES.get('images_news')
            img_name = request.FILES.get('images_news').name

            fs = FileSystemStorage(location='static/images/uploads')
            files  = fs.save(img.name,img)

            fileurl = fs.path(files)
           
            Scholar_news.objects.filter(id=edit_id).update(sn_photo_bg =  fileurl )

        if request.FILES.get('file_news') != None:
            pdf = request.FILES.get('file_news')
            
            fs2 = FileSystemStorage()
            files  = fs2.save(pdf.name,pdf)

            fileurl = fs2.path(files)
            

            Scholar_news.objects.filter(id=edit_id).update(sn_path_to_pdf =fileurl)
        return redirect('InformationHome')
        
    news = Scholar_news.objects.filter(id=edit_id)
    return render(request,'Create_Admin/editinformation.html',{'news': news})

def addEditInfomation(request):
    redirect('InformationHome')

@login_required (login_url='index')
def viewHome(request,home_id,user_id):
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    check = False
    status_homeid = Scholar_info.objects.filter(id=home_id)
    status_homeid = status_homeid[0].si_status
    if status_homeid ==2:
        return redirect('home')
    if status_homeid == 0:
        if Scholar_app.objects.filter(sa_si_id = home_id,sa_userid=user_obj).exists()==False:
            check = True
            
    scholar = Scholar_info.objects.filter(id=home_id)
    datajson  = Scholar_info.objects.get(id=home_id)
    datajson = datajson.si_source_name
    
    return render(request,'apply_info/view-home.html',{'scholars': scholar,'datajson':datajson,'check':check,'status_homeid':status_homeid})


@user_passes_test(lambda u: u.is_superuser)
def manageCommitteeHome(request):   #หน้าแสดงรายชื่อคณะกรรมการทั้งหมด
    news = User.objects.filter(is_staff=True) #ดึงฐานdatabase
    paginator = Paginator(news,5)  
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        newsperPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        newsperPage = paginator.page(paginator.num_pages)


    return render(request,'manageCommittee_Admin/manageCommitteeHome.html',{'scholars':newsperPage})


@user_passes_test(lambda u: u.is_superuser)
def delmanageCommitteeHome(request,user_id):
    user_obj = User.objects.get(id=user_id)
    tempdata = user_obj.email
    user_obj.delete()
    ad = add_commit.objects.filter(ac_email= tempdata)
    ad = ad[0]
    ad.delete()
    messages.success(request, "ลบบัญชี Admin แล้ว")
    news = User.objects.filter(is_staff=True) #ดึงฐานdatabase
    return redirect('manageCommitteeHome')


@user_passes_test(lambda u: u.is_superuser)
def viewManageCommitteeHome(request,home_id): #หน้ารายชื่อทุนที่คณะกรรมการท่านนั้นทำการสอบสัมภาษณ์
    scholar = Scholar_info.objects.all()    #ชื่อทุนทั้งหมด
    users_obj = User.objects.filter(id=home_id)
    
    if request.method == 'POST':
        lst_idScholar = request.POST.getlist('idScholar')

        for idScholar in lst_idScholar:
            # print(idScholar)
            getID = idScholar
            obj_scholar = Scholar_info.objects.get(id=getID)
            users_obj = User.objects.get(id=home_id)

            if add_scholar_Commit.objects.filter(id_commit=users_obj).filter(Scholar_name=obj_scholar).exists()==False:
                news_obj = add_scholar_Commit.objects.create(
                    id_commit = users_obj,
                    Scholar_name = obj_scholar
                )
                news_obj.save()


        users_obj = User.objects.filter(id=home_id)
        users_obj = users_obj[0]
      
        if add_scholar_Commit.objects.filter(id_commit=users_obj).count() >=1:
            lstDBs = add_scholar_Commit.objects.filter(id_commit=users_obj)
        else:
            lstDBs = add_scholar_Commit.objects.filter(id_commit__in=users_obj)

        
        for lstDB in lstDBs:
            users_obj2 = User.objects.get(id=home_id)
            countInDB = 0
            for idScholar in lst_idScholar:
                if(int(lstDB.Scholar_name.id)==int(idScholar)):
                    countInDB = countInDB+1
                    print(countInDB)
                    break
                
            if countInDB != 1:
                add_scholar_Commit.objects.filter(id_commit=users_obj2).filter(Scholar_name=lstDB.Scholar_name.id).delete()
                
        messages.success(request, "เพิ่มการเข้าถึงทุนของกรรมการแล้ว")
        return redirect("/viewManageCommitteeHome/"+str(home_id))
    
    user_obj_id= home_id                      
    scholar_n = add_scholar_Commit.objects.filter(id_commit=users_obj[0])
    dic = {}
    for i in range(len(scholar)):
        # print(scholar[i].si_status)
        if(len(scholar_n)>0 and (scholar[i].si_status<=1)):
            for j in range(len(scholar_n)):
                if(scholar_n[j].Scholar_name.id==scholar[i].id):
                    dic[str(scholar[i].si_name),int(scholar[i].id)]=True
                    break
                elif(scholar_n[j].Scholar_name.id!=scholar[i].id):
                    dic[str(scholar[i].si_name),int(scholar[i].id)]=False
        elif(len(scholar_n)==0 and (scholar[i].si_status<=1)):
            dic[str(scholar[i].si_name),int(scholar[i].id)]=False
        # else:
    # print(dic)
            

    return render(request,'manageCommittee_Admin/view-manageCommitteeHome.html',{'users_obj':users_obj,'user_id':user_obj_id,'json':dic,'scholar':scholar})

@user_passes_test(lambda u: u.is_superuser)
def addCommittee(request):
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        email = request.POST['email']
        print(firstname,lastname,email)

        #สิ่งที่ต้องแก้ คือ email ยังไม่รู้ว่าจะเช็คยังไงว่าเขาเป็นกรรมการไหม'tuple' object has no attribute 'get'
        news_obj = add_commit.objects.create(
            ac_email = email,
            ac_firstname = firstname,
            ac_lastname = lastname,
        )
        news_obj.save()
        messages.success(request, "เพิ่มบัญชีกรรมการแล้ว")
    return render(request,'manageCommittee_Admin/addCommittee.html')

@user_passes_test(lambda u: u.is_superuser)    
def viewScore(request):

    infoes = Scholar_info.objects.all() #ดึงฐานdatabase
    scholar = Scholar_weight_score.objects.all()
    res={}
    for key in scholar:
        res[key] = key.status
    

    
    
    return render(request,'score/scholar_score.html',{'infoes':infoes,'scholars':scholar,'res':res}) 

@user_passes_test(lambda u: u.is_superuser)
def viewWightScore(request,id_info):
    info = Scholar_info.objects.filter(id=id_info)
    info_data =info[0]
    info2 = info[0]
    info2 = info2.id
    


    if request.method == 'POST':
        name_lst = request.POST.getlist('name[]')
        weight_lst = request.POST.getlist('weight[]')
        res = {}
        for key in name_lst:
            for value in weight_lst:
                res[key] = value
                weight_lst.remove(value)
                break  
        now = datetime.now()
        data = Scholar_weight_score.objects.filter(sws_si_id=id_info).update(
                sws_info = res,
                sws_date = now,
                status =True,
        )
        infoes = Scholar_info.objects.all()
        return redirect('scholarScore')
    json= {"หัวข้อ":"คะแนน"}
    if  Scholar_weight_score.objects.filter(sws_si_id=info_data).exists() == True:
        json = Scholar_weight_score.objects.filter(sws_si_id=info_data.id)
        json = json[0]
        json = json.sws_info

    return render(request,'score/weight_score.html',{'info':info,'info2':info2,'json':json})

#def NisitAppilcateScholar(request): #หน้าสมัครทุน

  #  return render(request,'nisitAppilcateScholar/viewNisitAppilcate.html') 

@login_required (login_url='index')
def profileHistoryNisit(request):
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]

    if Scholar_profile.objects.filter(sp_userid =user_obj).exists()==True:
        dataScholar = Scholar_info.objects.all()
        time = datetime.now()
        for i in dataScholar:
            dateInfo = datetime.fromisoformat(str(i.si_expire_time)).timestamp()
            dateToday = datetime.fromisoformat(str(time)).timestamp()
            if dateInfo <= dateToday:
                i.si_status = 1
                print(i.si_name)
    
    

    if Scholar_profile.objects.filter(sp_userid =user_obj).exists()==False:
        data = Scholar_profile.objects.create(sp_userid = user_obj )
        data.save()
        data2 = avatar_profile.objects.create(sa_userid=user_obj)
        data2.save
        return render(request,'Form_Nisit/history_nisit.html') 

    
                    
    if request.method == 'POST':
            #ของนิสิต
            advisor_professor = request.POST['advisor_professor'] ##อาจารย์ที่ปรึกษา
            title_thai = request.POST['title-thai']
            print(title_thai)
            firstname_th = request.POST['firstname-th']
            middlename_th = request.POST['middlename-th']
            lastname_th = request.POST['lastname-th']
            std = request.POST['std']  
            title_eng = request.POST['title-eng']
            firstname_eng = request.POST['firstname-eng']
            middlename_eng = request.POST['middlename-eng']
            lastname_eng = request.POST['lastname-eng']
            ## email = request.POST['email']
            birthday = request.POST['birthday']
            if birthday == "":
                birthday = date.today()
            # pdf = request.POST['pdf']
            ## factor = request.POST['factor']
            major = request.POST['major']
            grade = request.POST['grade']
            address = request.POST['address']
            phone = request.POST['phone']
            
            #ของบิดา
            title_dad = request.POST['title-dadthai'] ##title_dad
            firstname_dad = request.POST['firstname-dad']
            middle_dad = request.POST['middlename-dad']
            lastname_dad = request.POST['lastname-dad']
            statuslife_dad = request.POST['statuslife-dad']
            address_dad = request.POST['address-dad']
            Tel_dad = request.POST['Tel-dad']
            birthday_dad =  request.POST['birthday-dad']
            if birthday_dad == "":
                birthday_dad = date.today()
            age_dad =  request.POST['age-dad']
            if age_dad=="":
                age_dad=0
            status_married_dad =  request.POST['status-married-dad']
            Income_dad =  request.POST['Income-dad']
            if Income_dad=="":
                Income_dad=0
            career_dad =  request.POST['career-dad']
            workplace_dad = request.POST['workplace-dad'] 
            
            # ของมารดา
            title_mom = request.POST['title-momthai'] ##title_mom
            firstname_mom = request.POST['firstname-mom']
            middle_mom = request.POST['middlename-mom']
            lastname_mom = request.POST['lastname-mom']
            statuslife_mom = request.POST['statuslife-mom']
            address_mom = request.POST['address-mom']
            Tel_mom = request.POST['Tel-mom']
            birthday_mom = request.POST['birthday-mom']
            if birthday_mom == "":
                birthday_mom = date.today()
            age_mom = request.POST['age-mom']
            if age_mom=="":
                age_mom=0
            status_married_mom = request.POST['status-married-mom']
            Income_mom = request.POST['Income-mom']
            if Income_mom=="":
                Income_mom=0
            career_mom = request.POST['career-mom']
            workplace_mom = request.POST['workplace-mom']

             #ของพี่น้อง
            title_sibling = request.POST.getlist('title-siblingthai')  ##title คำนำหน้า
            firstname_sibling = request.POST.getlist('firstname-sibling')
            middle_sibling = request.POST.getlist('middlename-sibling') ##ชื่อกลาง
            lastname_sibling= request.POST.getlist('lastname-sibling')
            education_sibling = request.POST.getlist('education-sibling')
            career_sibling = request.POST.getlist('career-sibling')
            workplace_sibling = request.POST.getlist('workplace-sibling')
            lst_bro=[]
            for i in range(len(firstname_sibling)):
                dic = {}
                dic['title_sibling']=title_sibling[i]
                dic['firstname_sibling']=firstname_sibling[i]
                dic['middle_sibling'] = middle_sibling[i]
                dic['lastname_sibling'] = lastname_sibling[i]
                dic['education_sibling'] = education_sibling[i]
                dic['career_sibling'] = career_sibling[i]
                dic['workplace_sibling'] = workplace_sibling[i]
                lst_bro.append(dic)
            
            #รายละเอียดราบได้ของผู้สมัครทุน
            moneyPerMonth = request.POST['moneyPerMonth']   #รายได้ต่อเดือน
            if moneyPerMonth=="":
                moneyPerMonth=0
            workplace_patron = request.POST['workplace-patron'] #ผู้ปกครองทำงานที่ไหน
            patron = request.POST['patron'] #ได้รับค่าใช้จ่ายจากใคร
            NumOfChild_patron = request.POST['NumOfChild-patron']   #ผู้ปกครองมีบุตรในอุปการะกี่คน
            if NumOfChild_patron=="":
                NumOfChild_patron=0
            studenloan = request.POST['studenloan'] #กู้ทุนมาไหม
            pastime = request.POST['pastime']   #เคยทำงานพิเศษไหม
            status_patron = request.POST['status-patron']   #ผู้ปกครองเกี่ยวข้องเป็นอะไร
            # #ไม่เอาแล้ว เอาเป็นเดือนไปเลยทีเดียว wages_pasttime = request.POST['wages-pasttime'] #นิสิตได้เงินต่อเดือนหรือสัปดาห์
            career_income = request.POST['career-income'] #รายได้จากงานนิสิต
            if career_income=="":
                career_income=0
            Type_address_pastime = request.POST['Type-pastime']    #ประเภทงานที่ทำและสถานที่ที่นิสิตทำงานพาร์ททาม
            career = request.POST['career-patron']   #อาชีพของผู้ปกครอง
            Tel_patron = request.POST['Tel-patron'] #เบอร์มือถือของผู้ปกครอง
            
            #ทุนการศึกษาของนิสิต
            received_scholar =  request.POST.getlist('received-scholar') #ชื่อทุนที่เคยได้รับ
            received_year_scholar = request.POST.getlist('received-year-scholar')   #ปีที่ได้รับทุน
            prize = request.POST.getlist('prize')   #จำนวนเงินที่ได้รับ
        
            lst=[]
            for i in range(len(received_scholar)):
                dic = {}
                dic['name']=received_scholar[i]
                dic['year']=received_year_scholar[i]
                dic['prize'] = prize[i]
                lst.append(dic)
                
            if prize=="":
                prize=0

            #รายละเอียดเพิ่มเติม
            # details = request.POST['details']   #เขียนรายละเอียดต่างๆ

           
            if len(request.FILES)!=0:
                if request.FILES.get('resume',False):
                    data2 = avatar_profile.objects.get(sa_userid=user_obj)
                    data2.sp_path_to_avatar = request.FILES.get('resume')
                    data2.save()
                
            
            data = Scholar_profile.objects.filter(sp_userid= user_obj).update(
                #ของนิสิต
                sp_advisor_professor = advisor_professor,
                sp_status = 1,
                sp_title_en =title_eng, 
                sp_firstname_en = firstname_eng,
                sp_middlename_en = middlename_eng,
                sp_lastname_en = lastname_eng,
                sp_std_code	= std,
                sp_title_th	= title_thai,
                sp_firstname_th	= firstname_th,
                sp_middlename_th = middlename_th,
                sp_lastname_th = lastname_th,
                sp_date_of_birth = birthday,	
                sp_major = major,
                sp_grade = grade,
                sp_std_address = address, ##json --> address,
                sp_std_tel_no = phone,
                #ของบิดา
                sp_father_title = title_dad,
                sp_father_firstname	= firstname_dad,
                sp_father_middlename = middle_dad,
                sp_father_lastname = lastname_dad,
                sp_father_date_of_birth = birthday_dad,
                sp_father_age = age_dad,
                sp_father_status_married = status_married_dad,
                sp_father_statuslife = statuslife_dad,
                sp_father_income = Income_dad,
                sp_father_career = career_dad,
                sp_father_workplace = workplace_dad,
                sp_father_address = address_dad, ##json --> address_dad,
                sp_father_tel_no = Tel_dad,
                #ของมารดา
                sp_mother_title = title_mom,
                sp_mother_firstname	= firstname_mom,
                sp_mother_middlename = middle_mom,
                sp_mother_lastname = lastname_mom,
                sp_mother_date_of_birth = birthday_mom,
                sp_mother_age = age_mom,
                sp_mother_status_married = status_married_mom,
                sp_mother_statuslife = statuslife_mom,
                sp_mother_income = Income_mom,
                sp_mother_career = career_mom,
                sp_mother_workplace = workplace_mom,
                sp_mother_address = address_mom, ##json --> address_mom,
                sp_mother_tel_no = Tel_mom,
                #ของพี่น้อง
                sp_bro_n_sis = lst_bro, ##json name,educate level,career,workplace
                #รายละเอียดราบได้ของผู้สมัครทุน
                sp_loan = studenloan,
                sp_income = moneyPerMonth,
                sp_income_source = patron,
                sp_patron_relation = status_patron,
                sp_patron_career = career,
                sp_patron_tel_no = Tel_patron,
                sp_patron_workplace = workplace_patron,
                sp_child_in_the_patron = NumOfChild_patron,
                sp_parttime	= pastime,
                sp_parttime_income = career_income,
                sp_parttime_type = Type_address_pastime,

                sp_json_scholar = lst,
                # sp_report = details,
            )
            data_user = User.objects.filter(id = request.user.id).update(first_name =firstname_th,last_name=lastname_th)
        
      
    return redirect('home')


def dict1(sample_dict, key, list_of_values):
    if key not in sample_dict:
        sample_dict[key] = list()
            
    sample_dict[key].extend(list_of_values)
    return sample_dict


@login_required (login_url='index')
@user_passes_test(lambda u: u.is_staff == False)   
@user_passes_test(lambda u: u.is_superuser == False)   
def editHistoryNisit(request):
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]
    

    if request.method == 'POST':
        #ของนิสิต
        advisor_professor = request.POST['advisor_professor'] ##อาจารย์ที่ปรึกษา
        title_thai = request.POST['title-thai']
        firstname_th = request.POST['firstname-th']
        middlename_th = request.POST['middlename-th']
        lastname_th = request.POST['lastname-th']
        std = request.POST['std']  
        title_eng = request.POST['title-eng']
        firstname_eng = request.POST['firstname-eng']
        middlename_eng = request.POST['middlename-eng']
        lastname_eng = request.POST['lastname-eng']
        birthday = request.POST['birthday']
        if birthday == "":
            birthday = date.today()
        major = request.POST['major']
        grade = request.POST['grade']
        address = request.POST['address']
        phone = request.POST['phone']
            
        #ของบิดา
        title_dad = request.POST['title-dadthai'] ##title_dad
        firstname_dad = request.POST['firstname-dad']
        middle_dad = request.POST['middlename-dad']
        lastname_dad = request.POST['lastname-dad']
        statuslife_dad = request.POST['statuslife-dad']
        address_dad = request.POST['address-dad']
        Tel_dad = request.POST['Tel-dad']
        birthday_dad =  request.POST['birthday-dad']
        if birthday_dad == "":
            birthday_dad = date.today()
        age_dad =  request.POST['age-dad']
        if age_dad=="":
            age_dad=0
        status_married_dad =  request.POST['status-married-dad']
        Income_dad =  request.POST['Income-dad']
        if Income_dad=="":
            Income_dad=0
        career_dad =  request.POST['career-dad']
        workplace_dad = request.POST['workplace-dad'] 
        
        # ของมารดา
        title_mom = request.POST['title-momthai'] ##title_mom
        firstname_mom = request.POST['firstname-mom']
        middle_mom = request.POST['middlename-mom']
        lastname_mom = request.POST['lastname-mom']
        statuslife_mom = request.POST['statuslife-mom']
        address_mom = request.POST['address-mom']
        Tel_mom = request.POST['Tel-mom']
        birthday_mom = request.POST['birthday-mom']
        if birthday_mom == "":
            birthday_mom = date.today()
        age_mom = request.POST['age-mom']
        if age_mom=="":
            age_mom=0
        status_married_mom = request.POST['status-married-mom']
        Income_mom = request.POST['Income-mom']
        if Income_mom=="":
            Income_mom=0
        career_mom = request.POST['career-mom']
        workplace_mom = request.POST['workplace-mom']

        #ของพี่น้อง
        title_sibling = request.POST.getlist('title-siblingthai')  ##title คำนำหน้า
        firstname_sibling = request.POST.getlist('firstname-sibling')
        middle_sibling = request.POST.getlist('middlename-sibling') ##ชื่อกลาง
        lastname_sibling= request.POST.getlist('lastname-sibling')
        education_sibling = request.POST.getlist('education-sibling')
        career_sibling = request.POST.getlist('career-sibling')
        workplace_sibling = request.POST.getlist('workplace-sibling')
        lst_bro=[]
        
        for i in range(len(firstname_sibling)):
            dic = {}
            dic['title_sibling']=title_sibling[i]
            dic['firstname_sibling']=firstname_sibling[i]
            dic['middle_sibling'] = middle_sibling[i]
            dic['lastname_sibling'] = lastname_sibling[i]
            dic['education_sibling'] = education_sibling[i]
            dic['career_sibling'] = career_sibling[i]
            dic['workplace_sibling'] = workplace_sibling[i]
            lst_bro.append(dic)
            
        #รายละเอียดราบได้ของผู้สมัครทุน
        moneyPerMonth = request.POST['moneyPerMonth']   #รายได้ต่อเดือน
        if moneyPerMonth=="":
            moneyPerMonth=0
        workplace_patron = request.POST['workplace-patron'] #ผู้ปกครองทำงานที่ไหน
        patron = request.POST['patron'] #ได้รับค่าใช้จ่ายจากใคร
        NumOfChild_patron = request.POST['NumOfChild-patron']   #ผู้ปกครองมีบุตรในอุปการะกี่คน
        if NumOfChild_patron=="":
            NumOfChild_patron=0
        studenloan = request.POST['studenloan'] #กู้ทุนมาไหม
        pastime = request.POST['pastime']   #เคยทำงานพิเศษไหม 
        status_patron = request.POST['status-patron']   #ผู้ปกครองเกี่ยวข้องเป็นอะไร
        # #ไม่เอาแล้ว เอาเป็นเดือนไปเลยทีเดียว wages_pasttime = request.POST['wages-pasttime'] #นิสิตได้เงินต่อเดือนหรือสัปดาห์
        career_income = request.POST['career-income'] #รายได้จากงานนิสิต
        if career_income=="":
            career_income=0
        Type_address_pastime = request.POST['Type-pastime']    #ประเภทงานที่ทำและสถานที่ที่นิสิตทำงานพาร์ททาม
        career = request.POST['career-patron']   #อาชีพของผู้ปกครอง
        Tel_patron = request.POST['Tel-patron'] #เบอร์มือถือของผู้ปกครอง
            
        #ทุนการศึกษาของนิสิต
    
        received_scholar =  request.POST.getlist('received-scholar') #ชื่อทุนที่เคยได้รับ
        received_year_scholar = request.POST.getlist('received-year-scholar')   #ปีที่ได้รับทุน
        prize = request.POST.getlist('prize')   #จำนวนเงินที่ได้รับ
        
        lst=[]
        for i in range(len(received_scholar)):
            dic = {}
            dic['name']=received_scholar[i]
            dic['year']=received_year_scholar[i]
            dic['prize'] = prize[i]
            lst.append(dic)
        
        if prize=="":
            prize=0
        #รายละเอียดเพิ่มเติม
        # details = request.POST['details']   #เขียนรายละเอียดต่างๆ

        if len(request.FILES)!=0:
                if request.FILES.get('resume',False):
                    data2 = avatar_profile.objects.get(sa_userid=user_obj)
                    data2.sp_path_to_avatar = request.FILES.get('resume')
                    data2.save()
            
        data = Scholar_profile.objects.filter(sp_userid= user_obj).update(
            #ของนิสิต
            sp_advisor_professor = advisor_professor,
            sp_status = 1,
            sp_title_en =title_eng, 
            sp_firstname_en = firstname_eng,
            sp_middlename_en = middlename_eng,
            sp_lastname_en = lastname_eng,
            sp_std_code	= std,
            sp_title_th	= title_thai,
            sp_firstname_th	= firstname_th,
            sp_middlename_th = middlename_th,
            sp_lastname_th = lastname_th,
            sp_date_of_birth = birthday,	
            sp_major = major,
            sp_grade = grade,
            sp_std_address = address, ##json --> address,
            sp_std_tel_no = phone,
             #ของบิดา
            sp_father_title = title_dad,
            sp_father_firstname	= firstname_dad,
            sp_father_middlename = middle_dad,
            sp_father_lastname = lastname_dad,
            sp_father_date_of_birth = birthday_dad,
            sp_father_age = age_dad,
            sp_father_status_married = status_married_dad,
            sp_father_statuslife = statuslife_dad,
            sp_father_income = Income_dad,
            sp_father_career = career_dad,
            sp_father_workplace = workplace_dad,
            sp_father_address = address_dad, ##json --> address_dad,
            sp_father_tel_no = Tel_dad,
            #ของมารดา
            sp_mother_title = title_mom,
            sp_mother_firstname	= firstname_mom,
            sp_mother_middlename = middle_mom,
            sp_mother_lastname = lastname_mom,
            sp_mother_date_of_birth = birthday_mom,
            sp_mother_age = age_mom,
            sp_mother_status_married = status_married_mom,
            sp_mother_statuslife = statuslife_mom,
            sp_mother_income = Income_mom,
            sp_mother_career = career_mom,
            sp_mother_workplace = workplace_mom,
            sp_mother_address = address_mom, ##json --> address_mom,
            sp_mother_tel_no = Tel_mom,
            #ของพี่น้อง
            sp_bro_n_sis = lst_bro, ##json name,educate level,career,workplace
            #รายละเอียดราบได้ของผู้สมัครทุน
            sp_loan = studenloan,
            sp_income = moneyPerMonth,
            sp_income_source = patron,
            sp_patron_relation = status_patron,
            sp_patron_career = career,
            sp_patron_tel_no = Tel_patron,
            sp_patron_workplace = workplace_patron,
            sp_child_in_the_patron = NumOfChild_patron,
            sp_parttime	= pastime,
            sp_parttime_income = career_income,
            sp_parttime_type = Type_address_pastime,

            #sp_received_scholar = lst,
            sp_json_scholar = lst,
            #sp_year_received_scholar = received_year_scholar,
            # sp_money_received_scholar = prize,
            # sp_report = details,
        )    
        data_user = User.objects.filter(id = request.user.id).update(first_name =firstname_th,last_name=lastname_th)
        messages.success(request, 'บันทึกข้อมูลส่วนตัวแล้ว')
        return redirect('home')
            
    edit = Scholar_profile.objects.filter(sp_userid = request.user.id)
    edit = edit[0]
    json = edit.sp_json_scholar
    json_bro = edit.sp_bro_n_sis
    #print(json)
    
    data2  = avatar_profile.objects.filter(sa_userid=request.user.id)
    data2 = data2[0]

    return render(request,'Form_Nisit/edit_historyNisit.html',{'edit':edit,'json':json,'json_bro':json_bro,'pic':data2})  

@login_required (login_url='index')
@user_passes_test(lambda u: u.is_staff == False)   
@user_passes_test(lambda u: u.is_superuser == False)      
def statusNisit(request):
    time = datetime.now()
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]
    lst = {} 
    states = Scholar_app.objects.filter(sa_userid = user_obj)
    if request.method == 'POST':
        status = request.POST['custId']
        info_id = request.POST['infoId']
        if status == "1":
            Scholar_app.objects.filter(sa_userid = user_obj,sa_si_id = info_id).update(sa_status = 33)
            return redirect('/payment/'+str(info_id))
        elif status == "0":
            Scholar_app.objects.filter(sa_userid = user_obj,sa_si_id = info_id).update(sa_status = 32)
    if states.exists() == True:
        states.select_related('sa_si_id','sa_userid')
        for state in states:
            file_obj = File_Models.objects.filter(fm_state=1,fm_Scholar=state.sa_si_id)
            if file_obj.exists() == True:
                lst[state] = [file_obj[0]]
            else:
                lst[state] = [None]

            dateApp = datetime.fromisoformat(str(state.sa_statusExDate)).timestamp()
            dateToday = datetime.fromisoformat(str(time)).timestamp()
            if dateToday <= dateApp:
                lst[state].append(True)
            else:
                lst[state].append(False)
        return render(request,'Status_Page/statusNisit.html',{'states':lst})
    else:
        return render(request,'Status_Page/statusNisit.html')
        
@login_required (login_url='index')
@user_passes_test(lambda u: u.is_staff == False)  
def checkInfo(request,info_id):
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]
    info_obj = Scholar_info.objects.filter(id=info_id)
    info_obj = info_obj[0]
    check = lambda x : None if ( x == "None" or x == "กรุณาเลือก" or x == "" )  else x
    try:
        if Scholar_app.objects.filter(sa_userid=user_obj ,sa_si_id = info_id).exists()==False:
            if request.method == 'POST':
                #ของนิสิต
                advisor_professor = check(request.POST['advisor_professor'])
                title_thai = check(request.POST['title-thai'])
                    
                firstname_th = request.POST['firstname-th']
                middlename_th = request.POST['middlename-th']
                    
                lastname_th = request.POST['lastname-th']
                std = request.POST['std']  
                title_eng = request.POST['title-eng']
                
                firstname_eng = request.POST['firstname-eng']
                middlename_eng = request.POST['middlename-eng']
                    
                lastname_eng = check(request.POST['lastname-eng'])
                ## email = request.POST['email']
                birthday = check(request.POST['birthday'])
                # pdf = request.POST['pdf']
                ## factor = request.POST['factor']
                major = check(request.POST['major'])
                grade = check(request.POST['grade'])
                address = check(request.POST['address'])
                phone = check(request.POST['phone'])
                            
                #ของบิดา
                title_dad = check(request.POST['title-dadthai']) ##title_dad
                    
                firstname_dad = check(request.POST['firstname-dad'])
                middle_dad = check(request.POST['middlename-dad'])
                    
                lastname_dad = check(request.POST['lastname-dad'])
                statuslife_dad = check(request.POST['statuslife-dad'])
                
                address_dad = check(request.POST['address-dad'])
                Tel_dad = request.POST['Tel-dad']
                birthday_dad =  check(request.POST['birthday-dad'])
                age_dad =  check(request.POST['age-dad'])
                status_married_dad =  check(request.POST['status-married-dad'])
                    
                Income_dad =  check(request.POST['Income-dad'])
                career_dad =  check(request.POST['career-dad'])
                workplace_dad = check(request.POST['workplace-dad'] )
                            
                # ของมารดา
                title_mom = check(request.POST['title-momthai']) ##title_mom
                    
                firstname_mom = check(request.POST['firstname-mom'])
                middle_mom = check(request.POST['middlename-mom'])
                    
                lastname_mom = check(request.POST['lastname-mom'])
                statuslife_mom = check(request.POST['statuslife-mom'])
                    
                address_mom = check(request.POST['address-mom'])
                Tel_mom = check(request.POST['Tel-mom'])
                birthday_mom = check(request.POST['birthday-mom'])
                age_mom = check(request.POST['age-mom'])
                status_married_mom = check(request.POST['status-married-mom'])
                    
                Income_mom = check(request.POST['Income-mom'])
                career_mom = check(request.POST['career-mom'])
                workplace_mom = check(request.POST['workplace-mom'])

                #ของพี่น้อง
                title_sibling = check(request.POST.getlist('title-siblingthai'))  ##title คำนำหน้า
                    
                firstname_sibling = check(request.POST.getlist('firstname-sibling'))
                middle_sibling = check(request.POST.getlist('middlename-sibling')) ##ชื่อกลาง
                    
                lastname_sibling= request.POST.getlist('lastname-sibling')
                education_sibling = request.POST.getlist('education-sibling')
                career_sibling = request.POST.getlist('career-sibling')
                workplace_sibling = request.POST.getlist('workplace-sibling')
                lst_bro=[]
                for i in range(len(firstname_sibling)):
                    dic = {}
                    dic['title_sibling']=title_sibling[i]
                    dic['firstname_sibling']=firstname_sibling[i]
                    dic['middle_sibling'] = middle_sibling[i]
                    dic['lastname_sibling'] = lastname_sibling[i]
                    dic['education_sibling'] = education_sibling[i]
                    dic['career_sibling'] = career_sibling[i]
                    dic['workplace_sibling'] = workplace_sibling[i]
                    lst_bro.append(dic)
                            
                #รายละเอียดราบได้ของผู้สมัครทุน
                moneyPerMonth = check(request.POST['moneyPerMonth'])   #รายได้ต่อเดือน
                workplace_patron = check(request.POST['workplace-patron']) #ผู้ปกครองทำงานที่ไหน
                patron = check(request.POST['patron']) #ได้รับค่าใช้จ่ายจากใคร
                
                NumOfChild_patron = check(request.POST['NumOfChild-patron'])   #ผู้ปกครองมีบุตรในอุปการะกี่คน
                studenloan = check(request.POST['studenloan']) #กู้ทุนมาไหม
                    
                pastime = check(request.POST['pastime'])   #เคยทำงานพิเศษไหม
                    
                status_patron = check(request.POST['status-patron'])   #ผู้ปกครองเกี่ยวข้องเป็นอะไร
                # #ไม่เอาแล้ว เอาเป็นเดือนไปเลยทีเดียว wages_pasttime = request.POST['wages-pasttime'] #นิสิตได้เงินต่อเดือนหรือสัปดาห์
                career_income = check(request.POST['career-income']) #รายได้จากงานนิสิต
                Type_address_pastime = check(request.POST['Type-pastime'])    #ประเภทงานที่ทำและสถานที่ที่นิสิตทำงานพาร์ททาม
                career = check(request.POST['career-patron'])   #อาชีพของผู้ปกครอง
                Tel_patron = check(request.POST['Tel-patron']) #เบอร์มือถือของผู้ปกครอง
                            
                #ทุนการศึกษาของนิสิต
                received_scholar =  request.POST.getlist('received-scholar') #ชื่อทุนที่เคยได้รับ
                received_year_scholar = request.POST.getlist('received-year-scholar')   #ปีที่ได้รับทุน
                prize = request.POST.getlist('prize')   #จำนวนเงินที่ได้รับ
                lst=[]
                for i in range(len(received_scholar)):
                    dic = {}
                    dic['name']=received_scholar[i]
                    dic['year']=received_year_scholar[i]
                    dic['prize'] = prize[i]
                    lst.append(dic)
                                
                if prize=="":
                    prize=0

                #รายละเอียดเพิ่มเติม
                # details = request.POST['details']   #เขียนรายละเอียดต่างๆ        
                            
                data = Scholar_app.objects.create(
                    #ของนิสิต
                    sa_userid = user_obj,
                    sa_si_id = info_obj, #id ทุน
                    sa_status =	11,	#สถานะการยื่นทุน 11=ผ่านรอบยื่นเอกสาร 20=เจ้าหน้าที่ตรวจสอบเอกสารไม่ผ่าน 21=เจ้าหน้าที่ตรวจสอบเอกสารผ่าน 30=ไม่ผ่านการคัดเลือกสอบสัมภาษณ์ 31=ผ่านการคัดเลือกสอบสัมภาษณ์ 41=รับเงินทุนสนับสนุนการศึกษา
                    # sa_path_to_pdf = PrivateFileField("File") ไฟล์ข้อมูลเพิ่มเติม
                    sa_score = 0,
                    sa_score_info =	{},
                    sa_advisor_professor = advisor_professor,
                    sa_title_en =title_eng, 
                    sa_firstname_en = firstname_eng,
                    sa_middlename_en = middlename_eng,
                    sa_lastname_en = lastname_eng,
                    sa_std_code	= std,
                    sa_title_th	= title_thai,
                    sa_firstname_th	= firstname_th,
                    sa_middlename_th = middlename_th,
                    sa_lastname_th = lastname_th,
                    ## sp_path_to_avatar = 	
                    sa_date_of_birth = birthday,	
                    sa_major = major,
                    sa_grade = grade,
                    sa_path_to_pdf_json	= {"key": "value"}, ##json --> pdf,
                    sa_std_address = address, ##json --> address,
                    sa_std_tel_no = phone,
                    #ของบิดา
                    sa_father_title = title_dad,
                    sa_father_firstname	= firstname_dad,
                    sa_father_middlename = middle_dad,
                    sa_father_lastname = lastname_dad,
                    sa_father_date_of_birth = birthday_dad,
                    sa_father_age = age_dad,
                    sa_father_status_married = status_married_dad,
                    sa_father_statuslife = statuslife_dad,
                    sa_father_income = Income_dad,
                    sa_father_career = career_dad,
                    sa_father_workplace = workplace_dad,
                    sa_father_address = address_dad, ##json --> address_dad,
                    sa_father_tel_no = Tel_dad,
                    #ของมารดา
                    sa_mother_title = title_mom,
                    sa_mother_firstname	= firstname_mom,
                    sa_mother_middlename = middle_mom,
                    sa_mother_lastname = lastname_mom,
                    sa_mother_date_of_birth = birthday_mom,
                    sa_mother_age = age_mom,
                    sa_mother_status_married = status_married_mom,
                    sa_mother_statuslife = statuslife_mom,
                    sa_mother_income = Income_mom,
                    sa_mother_career = career_mom,
                    sa_mother_workplace = workplace_mom,
                    sa_mother_address = address_mom, ##json --> address_mom,
                    sa_mother_tel_no = Tel_mom,
                    #ของพี่น้อง
                    sa_bro_n_sis = lst_bro, ##json name,educate level,career,workplace
                    #รายละเอียดราบได้ของผู้สมัครทุน
                    sa_loan = studenloan,
                    sa_income = moneyPerMonth,
                    sa_income_source = patron,
                    sa_patron_relation = status_patron,
                    sa_patron_career = career,
                    sa_patron_tel_no = Tel_patron,
                    sa_patron_workplace = workplace_patron,
                    sa_child_in_the_patron = NumOfChild_patron,
                    sa_parttime	= pastime,
                    sa_parttime_income = career_income,
                    sa_parttime_type = Type_address_pastime,

                    sa_json_scholar = lst,
                    # sp_report = details,
                )
                data.save
                if File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=info_obj).exists() == False:
                    file =  File_Models.objects.create(fm_upload_by=user_obj,
                                        fm_Scholar=info_obj
                            )

                if len(request.FILES)!=0:
                    if request.FILES.get('myPdf',False):
                        data3 = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=info_obj)
                        data3 = data3[0]
                        data3.fm_file = request.FILES.get('myPdf')
                        data3.save()
                return redirect('/viewHome/'+str(info_id)+"/"+str(request.user.id))
            checkin = Scholar_profile.objects.filter(sp_userid = user_obj)
            checkin = checkin[0]
            json = checkin.sp_json_scholar
            json_bro = checkin.sp_bro_n_sis
            data2  = avatar_profile.objects.filter(sa_userid=request.user.id)
            data2 = data2[0]              
            return render(request,'apply_info/checkInfo.html',{'checkin':checkin,'json':json,'json_bro':json_bro,'info_id':info_id,'pic':data2})
        else:
            if request.method == "POST" :
                if len(request.FILES)!=0:
                    if request.FILES.get('myPdf',False):
                        data3 = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=info_obj)
                        data3 = data3[0]
                        data3.fm_file = request.FILES.get('myPdf')
                        data3.save()
                        return redirect("/home")
                else:
                    return redirect("/home")
                        
            checkin = Scholar_app.objects.filter(sa_userid = user_obj,sa_si_id=info_obj)
            checkin = checkin[0]
            json = checkin.sa_json_scholar
            json_bro = checkin.sa_bro_n_sis
            data2  = avatar_profile.objects.filter(sa_userid=request.user.id)
            data2 = data2[0]
            file_obj = File_Models.objects.filter(fm_upload_by=user_obj,fm_Scholar=info_obj,fm_state=0)
            file_obj = file_obj[0]
            return render(request,'apply_info/checkInfo2.html',{'checkin':checkin,'json':json,'json_bro':json_bro,'info_id':info_id,'pic':data2,'file_obj':file_obj})
    except : 
        messages.error(request, 'ท่านกรอกข้อมูลไม่ครบ')
        messages.error(request, 'เว็บไซต์กำลังนำพาท่านไปยัง หน้าแก้ไขประวัติส่วนตัว')
        return redirect('editHistoryNisit')

@login_required (login_url='index')            
@user_passes_test(lambda u: u.is_staff) 
def interview(request):
    user_obj = User.objects.get(id=request.user.id)
    scholars = add_scholar_Commit.objects.filter(id_commit = user_obj)
    findNews = ""
    if request.method == "POST":
        findNews = request.POST['findcommit']
        print(findNews)

    scholars_list_id=[]
    for i in scholars :
        scholars_list_id.append(i.Scholar_name.id)
        
    scholars_list_obj =[]
    for i in scholars_list_id:
        scholar_obj =Scholar_info.objects.filter(id=i)

        if scholar_obj[0].si_status ==1:
            if findNews != "":
                info = Scholar_info.objects.filter(si_name__contains = findNews)
                if scholar_obj[0] in info:
                    scholars_list_obj.append(scholar_obj)
                    print(scholar_obj)
            else:
                scholars_list_obj.append(scholar_obj)
    
    paginator = Paginator(scholars_list_obj,4)  

    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        newsperPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        newsperPage = paginator.page(paginator.num_pages)

    return render(request,'Committee/news_committee.html',{'scholars':newsperPage})


def historyGetScholar(request):
    # infoAll = Scholar_info.objects.all()
    infoAll = Scholar_info.objects.filter(si_status=2)
    data = Scholar_app.objects.all()
    year = [] 
    for info in infoAll:
        if info.si_year not in year:
            year.append(info.si_year)
    year.sort()
    scholarName = "กรุณาเลือก"   #ชื่อทุน
    yearGet = "กรุณาเลือก"  #ปีของทุน
    scholarType = "กรุณาเลือก"
    if request.method == "POST":
        IDStudent = request.POST['studentID']   #เลขรหัสนิสิต
        scholarType = request.POST['scholarType']   #ทุนภายใน/นอก/ผสม
        scholarName = request.POST['scholarName']   #ชื่อทุน
        yearGet = request.POST['year']  #ปีของทุน
        ScholarProvider = request.POST['ScholarProvider']
        if IDStudent != "":
            data = data.filter(sa_std_code__contains = IDStudent,sa_status = 41)
        if scholarType != "กรุณาเลือก":
            infoes = Scholar_info.objects.filter(si_source=scholarType)
            info_id = []
            for info in infoes:
                info_id.append(info.id)
            data = data.filter(sa_si_id__in = info_id,sa_status = 41)
        if scholarName != "กรุณาเลือก":
            infoes = Scholar_info.objects.filter(si_name=scholarName)
            info_id = []
            for info in infoes:
                info_id.append(info.id)
            data = data.filter(sa_si_id__in = info_id,sa_status = 41)
        if yearGet != "กรุณาเลือก":
            infoes = Scholar_info.objects.filter(si_year=yearGet) 
            info_id = []
            for info in infoes:
                info_id.append(info.id)
            data = data.filter(sa_si_id__in = info_id,sa_status = 41)
        if ScholarProvider != "":
            infoes = Scholar_info.objects.filter(si_source_name__contains=ScholarProvider)
            info_id = []
            for info in infoes:
                info_id.append(info.id)
            data = data.filter(sa_si_id__in = info_id,sa_status = 41)

        dic = []
        money = 0
        for info in infoAll:
            d = data.filter(sa_si_id = info.id)
            if d.exists() == True:
                money += len(d)*info.si_individual_amount
                dic.append([info,d])


        paginator = Paginator(dic,10)

        try:
            page = int(request.GET.get('page','1'))
        except:
            page=1
        
        try:
            dataperPage =  paginator.page(page)
        except(EmptyPage,InvalidPage):
            dataperPage = paginator.page(paginator.num_pages)


        return render(request,'historyGetScholar_addmin/historyGetScholar.html',{'infoes':infoAll,'year':year,'studentID' :IDStudent,'scholarType':scholarType,'scholarName':scholarName,'yearGet':yearGet,'ScholarProvider':ScholarProvider,'money':money,'history':dataperPage})
    return render(request,'historyGetScholar_addmin/historyGetScholar.html',{'infoes':infoAll,'year':year,'scholarType':scholarType,'scholarName':scholarName,'yearGet':yearGet})

@login_required (login_url='index')            
@user_passes_test(lambda u: u.is_superuser)
def firstAppilcationAdmin(request): #หน้าแรกของรายชื่อนิสิตแต่ละทุน
    news = Scholar_info.objects.all()
    findNews = ""
    if request.method == "POST":
        findNews = request.POST['findstudent']
    if findNews != "":
        news = news.filter(si_name__contains = findNews)
    paginator = Paginator(news,4)
    today = date.today()

    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        newsperPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        newsperPage = paginator.page(paginator.num_pages)

    return render(request,'appilcationList_addmin/firstAppList.html',{'scholars': newsperPage,'today':today})

@login_required (login_url='index')            
@user_passes_test(lambda u: u.is_superuser)
def secondAppilcationAdmin(request,home_id):    #หน้า 2 ของรายชื่อนิสิตแต่ละทุน
    scholars = Scholar_info.objects.filter(id=home_id)
    scholarss = scholars[0]
    scholarss = scholarss.si_status
    
    commit = Scholar_weight_score.objects.filter(sws_si_id=home_id)
    commit = commit[0]
    commit = commit.status
    # print(int(datetime.datetime.utcnow().timestamp()))
    listApps = Scholar_app.objects.filter(sa_si_id=home_id)
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]
    # dateex41 = listApps.sa_statusExDate
    dateToday = date.today()
    
    if request.method == "POST":
        if len(File_Models.objects.filter(fm_Scholar=scholars[0]).filter(fm_state=1)) != 0 :
            data3 = File_Models.objects.filter(fm_Scholar=scholars[0]).filter(fm_state=1)
            data3 = data3[0]
            data3.fm_file = request.FILES.get('myPdf')
            data3.fm_state = 1
            data3.save()

        else:
     
            data3 = File_Models.objects.create(
                    fm_upload_by=user_obj,
                    fm_Scholar=scholars[0],
                    fm_file = request.FILES.get('myPdf'),
                    fm_state = 1

                )
            data3.save()




    json = Scholar_weight_score.objects.filter(sws_si_id=home_id)

    check11 = True
    check31 = True
    check21 = True
    if Scholar_app.objects.filter(sa_si_id=home_id).exists() == False:
        check11 = False
        check21 = False
        check31 = False
    elif Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=11).exists() == True:
        # check11 = False
        check31 = False
    # check21 = True
    # if Scholar_app.objects.filter(sa_si_id=home_id).exists() == False:
    #     check21 = False
    elif Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=31).exists() == True:
        check21 = False
        check31 = False
    elif Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=32).exists() == True:
        check21 = False
        check31 = False
    elif Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=33).exists() == True:
        check21 = False
        check31 = False
    elif Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=41).exists() == True:
        check21 = False
        check31 = False
    # check31 = True
    # if Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=11).exists() == True:
    #     check31 = False

    memberGet = Scholar_info.objects.filter(id=home_id)
    memberGet = memberGet[0]
    memberGet = memberGet.si_max_scholar
    # print(memberGet)
    memberGot = Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=31).count() + Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=41).count()
    memberGot = memberGot + Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=33).count()
    #print(memberGot)
    memberG = memberGet - memberGot

    if memberGet - Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=41).count() == 0:
      enddate = datetime.now() + timedelta(days=2)
      data = Scholar_info.objects.filter(id=home_id).update(si_endtime=enddate)


    
    file_upload = None
    if File_Models.objects.filter(fm_Scholar=scholars[0]).filter(fm_state=1).exists():
        file_upload = File_Models.objects.filter(fm_Scholar=scholars[0]).filter(fm_state=1)
        file_upload = file_upload[0]

    paginator = Paginator(listApps,10)  
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    
    try:
        listAppsPage =  paginator.page(page)
    except(EmptyPage,InvalidPage):
        listAppsPage = paginator.page(paginator.num_pages)


    
    return render(request,'appilcationList_addmin/secondAppList.html',{'scholars': scholars,'scholarss':scholarss,'listApps':listAppsPage,'json':json ,'check':check11,'info_id':home_id,'memberG':memberG,'commit':commit,'file_upload':file_upload,'check21':check21,'check31':check31,'dateToday':dateToday})

@login_required (login_url='index')            
@user_passes_test(lambda u: u.is_staff)
def interviewStudent(request,info_id):
    info_obj = Scholar_info.objects.get(id = info_id)
    obj_info = Scholar_app.objects.filter(sa_si_id = info_id)
    my_userid = User.objects.get(id =request.user.id)
    my_userid = my_userid.id
    my_userid = str(my_userid)
    # print(type(my_userid))
    status =Scholar_app.objects.filter(sa_si_id = info_id).filter(sa_status=21).exists()
    dic = {}
    for i in obj_info:
        if bool(i.sa_json_commit) :
            for j,k in i.sa_json_commit.items():
                # if bool(j):
                if my_userid == j:
                    dic[i.sa_userid.first_name,i.sa_userid.last_name,i.sa_userid.id,info_id,i.sa_status] = True
                    break
                else:
                    dic[i.sa_userid.first_name,i.sa_userid.last_name,i.sa_userid.id,info_id,i.sa_status] = False
        else:
            dic[i.sa_userid.first_name,i.sa_userid.last_name,i.sa_userid.id,info_id,i.sa_status] = False
    print(dic)
    return render(request,'Committee/interviewStudent.html',{'apps':obj_info,'my_userid':my_userid,'dic':dic,'status':status})

@login_required (login_url='index')             
@user_passes_test(lambda u: u.is_staff)
def interviewStudentTest(request,info_id,user_id):
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    info_obj = Scholar_info.objects.filter(id=info_id)
    info_obj = info_obj[0]
    checkin = Scholar_app.objects.filter(sa_userid = user_obj).filter(sa_si_id = info_obj)
    checkin = checkin[0]
    json_scholar = checkin.sa_json_scholar
    json_bro = checkin.sa_bro_n_sis
    data2  = avatar_profile.objects.filter(sa_userid=user_obj)
    data2 = data2[0]
    file_obj = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=info_obj)
    file_obj = file_obj[0]
    test_obj = Scholar_weight_score.objects.filter(sws_si_id=info_obj)
    json_sws = test_obj[0]
    json = json_sws.sws_info
    data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=info_obj).get()

    myidindatabase = []
    
    for key,value in data.sa_json_commit.items():
        myidindatabase.append(int(key))
    
  
    if request.user.id  in myidindatabase:
        messages.success(request, 'ท่านเคยให้คะแนนสัมภาษณ์บุคคลนี้แล้ว')
        return redirect('/interviewStudent/'+str(info_id))      
    else:
        if request.method == 'POST':  

            name_lst = request.POST.getlist('name[]')
            weight_lst = request.POST.getlist('weight[]')
            score_wieght = []
            list_wieght = []
            #---------------fetch databases-------------
            database_score = []
            for key,value in data.sa_score_info.items():
                database_score.append(float(value))
            #-------------------------------------------
            for key,value in json.items():
                score_wieght.append(value)
            #--------นับรายชื่อกรรมการที่กรอกคะแนนมาแล้ว------
            countCommit = len(data.sa_json_commit.items())
            
            ###สมการทั่วไป คือ ซิกม่าคะแนนรวมปัจจุบัน/จำนวนกรรมการปัจจุบัน = คะแนนเฉลี่ย
            # กรณีที่กรรมการ 0 คนก่อนหน้า ให้ใช้คะแนนคนปัจจุบันใส่ได้เลย
            # กรณีมีกรรมการ 2 คนขึ้นไป สมการ คือ คะแนนเฉลี่ย*จำนวนกรรมการก่อนคนปัจจุบัน = ซิกม่าคะแนนรวมก่อนคนปัจจุบัน
                # และหาเฉลี่ยคะแนนคนปัจจุบัน คือ (ซิกม่าคะแนนรวมก่อนคนปัจจุบัน+คะแนนคนปัจจุบัน)/(จำนวนกรรมการก่อนคนปัจจุบัน+1)

            if(len(database_score) !=0 ): #เช็คว่ามีกรรมการลงคะแนนรึยัง? {10, 10}
                res = {}  
                for key in name_lst:
                    for value in range(len(weight_lst)):
                        sigmaScore = database_score[value]*(countCommit)
                        sumSigScore = sigmaScore+float(weight_lst[value])
                        res[key] = sumSigScore/(countCommit+1)
                        weight_lst.remove(weight_lst[value])
                        list_wieght.append(sumSigScore/(countCommit+1))
                        break  
            else: # ถ้าไม่มีใคร {}
                res = {}
                for key in name_lst:
                    for value in weight_lst:
                        res[key] = value
                        weight_lst.remove(value)
                        list_wieght.append(value)
                        break

            sum_weightCom = 0
            sum_weightAll = 0
            for i in range(len(score_wieght)):
                sum_weightAll = sum_weightAll + float(score_wieght[i])
            for i in range(len(score_wieght)):
                sum_weightCom = sum_weightCom + float(list_wieght[i])
                
            sum_weight = (sum_weightCom/sum_weightAll)*100
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=info_obj)
            data = data[0]
            person = data.sa_person 
            score_database = data.sa_score
            # cal = (score_database+sum_weight)/person
            now = datetime.now()
            #add กรรมการลงในที่เคยสัมภาษณ์
            data_commit  = data.sa_json_commit
            data_commit[int(request.user.id)] = "True"
            #--------------------- add log กรรมการ 
            my_user = User.objects.get(id = request.user.id)
            student_user = User.objects.get(id = user_id)
            log_data  = Log_score.objects.filter(ls_commit = my_user).filter(ls_student =  student_user).filter(ls_Scholar = info_obj).update(score = res)

                #-----------------------
                #อัพเดทคะแนนรวม และรายข้อ
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=info_obj).update(
                        sa_score_info = res,
                        sa_score = sum_weight,
                        sa_person = person+1,
                    sa_json_commit = data_commit
            )
                #--------------------------
            return redirect('/interviewStudent/'+str(info_id))
        



    my_user = User.objects.get(id = request.user.id)
    student_user = User.objects.get(id = user_id)
    log_data  = Log_score.objects.create(
        ls_commit = my_user,
        ls_student =  student_user,
        ls_Scholar = info_obj,
        score = "",
    )
    log_data.save()
        
    return render(request,'Committee/interviewStudentTest.html',{'checkin':checkin,'json':json,'json_bro':json_bro,'info_id':info_id,'pic':data2,'file_obj':file_obj,'json_scholar':json_scholar})

@login_required (login_url='index')            
@user_passes_test(lambda u: u.is_superuser)
def checkStatus(request,home_id,user_id):   #หน้าตรวจสอบเอกสารของแอดมิน
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    info_obj = Scholar_info.objects.filter(id=home_id)
    info_obj = info_obj[0]
    checkin = Scholar_app.objects.filter(sa_userid = user_obj).filter(sa_si_id = home_id)
    checkin = checkin[0]
    json_scholar = checkin.sa_json_scholar
    json_bro = checkin.sa_bro_n_sis
    data2  = avatar_profile.objects.filter(sa_userid=user_id)
    data2 = data2[0]

    file_obj = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=home_id)
    file_obj = file_obj[0]

    test_obj = Scholar_weight_score.objects.filter(sws_si_id=home_id)
    json = test_obj[0]
    json = json.sws_info
    if request.method == 'POST':
        button = request.POST['button']
        if button == "ยืนยัน":
            status = 21
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 21)
            return redirect('/checkStatus/'+str(home_id)+'/'+str(user_id))
        elif button == "ไม่ผ่าน":
            status = 20
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 20)
            return redirect('/checkStatus/'+str(home_id)+'/'+str(user_id))
    
    protect= Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id)
    
    if protect[0].sa_status != 11 and protect[0].sa_status != 20:
        print("เข้า")
        return redirect('firstAppilcationAdmin')


    return render(request,'appilcationList_addmin/check_status.html',{'checkin':checkin,'json':json,'json_bro':json_bro,'info_id':home_id,'pic':data2,'file_obj':file_obj,'json_scholar':json_scholar})

@login_required (login_url='index')               
def delApp(request,home_id,user_id):  
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    Scholar_app.objects.filter(sa_userid=user_obj,sa_si_id=home_id).delete()
    return redirect('/viewHome/'+str(home_id)+"/"+str(user_id))

@login_required (login_url='index')
def changeStatus(request,home_id,user_id,status):
    user_obj = User.objects.get(id=user_id)
    checkin = Scholar_app.objects.filter(sa_userid = user_obj).filter(sa_si_id = home_id)
    checkin = checkin[0]

    memberGet = Scholar_info.objects.filter(id=home_id)
    memberGet = memberGet[0]
    memberGet = memberGet.si_max_scholar
    memberGot = Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=31).count()+Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=41).count()
    memberGot = memberGot + Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=33).count()
    memberGot = memberGot - Scholar_app.objects.filter(sa_si_id=home_id).filter(sa_status=32).count()
    memberG = memberGet - memberGot

    if checkin.sa_status == 11:
        if status == 1:
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 21)
            return redirect('/secondAppilcationAdmin/'+str(home_id))
        elif status == 0:
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 20)
            return redirect('/secondAppilcationAdmin/'+str(home_id))
    elif checkin.sa_status == 20:
        if status == 1:
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 21)
            return redirect('/secondAppilcationAdmin/'+str(home_id))
    elif checkin.sa_status == 21:
        if status == 1:
            if(memberG==0):
                messages.success(request, 'ไม่สามารถทำรายการได้ เนื่องจากมีผู้รับทุนครบเรียบร้อยแล้ว')
                return redirect('/secondAppilcationAdmin/'+str(home_id))
            else:
                enddate = datetime.now() + timedelta(days=7)
                data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                    sa_status = 31 ,sa_statusExDate = enddate)
                return redirect('/secondAppilcationAdmin/'+str(home_id))
        elif status == 0:
            data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                sa_status = 30)
            return redirect('/secondAppilcationAdmin/'+str(home_id))
    elif checkin.sa_status == 30:
        if status == 1:
            if(memberG==0):
                messages.success(request, 'ไม่สามารถทำรายการได้ เนื่องจากมีผู้รับทุนครบเรียบร้อยแล้ว')
                return redirect('/secondAppilcationAdmin/'+str(home_id))
            else:
                enddate = datetime.now() + timedelta(days=7)
                data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                    sa_status = 31 ,sa_statusExDate = enddate)
                return redirect('/secondAppilcationAdmin/'+str(home_id))
    elif checkin.sa_status == 33:       
        if status == 1:            
            if checkin.sa_statusExDate <= date.today():                
                data = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id=home_id).update(
                    sa_status = 41)
                return redirect('/secondAppilcationAdmin/'+str(home_id))
            else:
                #messages.success(request, 'ไม่สามารถเปิดเอกสารได้\nเนื่องจากยังไม่หมดเวลาส่งเอกสารของนิสิต')
                messages.success(request, "ไม่สามารถเปลี่ยนสถานะได้ เนื่องจากยังไม่หมดเวลาส่งเอกสารของนิสิต")
                return redirect('/secondAppilcationAdmin/'+str(home_id))

    return redirect('/secondAppilcationAdmin/'+str(home_id))

@login_required (login_url='index')            
def limitaccount(request):
    if request.user.is_superuser == True:
        return redirect('home')

    a = request.user.email
    b= a
    a = a.split("@")
    a = a[1]
    if request.user.is_staff == True:
        return redirect('interview')

    if request.user.is_staff == False:
            obj2 = add_commit.objects.filter(ac_email=request.user.email).exists() 
            if obj2 == True:
                obj2 = add_commit.objects.filter(ac_email=request.user.email)
                if obj2 != None:
                    user_obj = User.objects.filter(email=request.user.email)
                    obj2=obj2[0]
                    for i in user_obj:
                        i.is_staff = True
                        i.first_name = obj2.ac_firstname
                        i.last_name = obj2.ac_lastname
                        i.save()
                        messages.success(request, 'สวัสดีคุณ'+ str(obj2.ac_firstname)+ 'เข้าสู่ระบบ โดยเป็นคณะกรรมการ')
                        return redirect('home')

    if b =="seg7.nisit@gmail.com" or b=="seg7.nisit.s@gmail.com" :
        return redirect('profileHistoryNisit')

        
    if a != "ku.th":
        messages.error(request, 'กรุณา Login ด้วย @ku.th เท่านั้น')
        u = User.objects.get(username = request.user.username)
        u.delete()
        return redirect('logout')
    else:           
        return redirect('profileHistoryNisit')


@login_required (login_url='index')
def payment(request,info_id):
    scholars = Scholar_info.objects.filter(id=info_id)
    scholarss = scholars[0]
    scholarss = scholarss.si_status

    # print(int(dastatusNisittetime.datetime.utcnow().timestamp()))
    user_obj = User.objects.filter(id=request.user.id)
    user_obj = user_obj[0]

    
    check = Scholar_app.objects.filter(sa_userid=user_obj).filter(sa_si_id =scholars[0])
    check = check[0].sa_status
    if check == 33 or check == 34:
        if request.method == "POST":
    
            if len(File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=scholars[0]).filter(fm_state=2)) != 0 :
                print(File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=scholars[0]).filter(fm_state=2))
                data3 = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=scholars[0]).filter(fm_state=2)
                data3 = data3[0]
                data3.fm_file = request.FILES.get('myPdf')
                data3.save()

            else:
        
                data3 = File_Models.objects.create(
                        fm_upload_by=user_obj,
                        fm_Scholar=scholars[0],
                        fm_file = request.FILES.get('myPdf'),
                        fm_state = 2

                    )
                data3.save()
            
            if check == 34:
                
                today = date.today()
                data = Scholar_app.objects.filter(sa_userid=user_obj,sa_si_id=scholars[0]).update(
                    sa_status = 33 , sa_statusExDate = today)
                print("เข้าที่นี้ : check == 34")

            messages.success(request, 'อัพโหลดเอกสารเรียบร้อย')
            
            return redirect('statusNisit')
    else:
        messages.success(request, 'ท่านสละสิทธิ์ไปแล้ว หรือ หมดเวลาการอัพโหลดไฟล์')
        return redirect('statusNisit')
        

        

    file_upload = None
    if len(File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=scholars[0]).filter(fm_state=2)) != 0:
        data3 = File_Models.objects.filter(fm_upload_by=user_obj).filter(fm_Scholar=scholars[0]).filter(fm_state=2)
        file_upload = data3[0]
    
    return render(request,'payment/payment.html',{'file_upload':file_upload,'info_id':info_id})

@login_required (login_url='index')           
@user_passes_test(lambda u: u.is_superuser)     
def removeScholar(request,info_id):
    data = Scholar_info.objects.filter(id=info_id).delete()
    messages.success(request, 'ลบทุนเรียบร้อยแล้ว')  
    return redirect('home')

@login_required (login_url='index')           
@user_passes_test(lambda u: u.is_superuser)     
def removeInformation(request,news_id):
    data = Scholar_news.objects.filter(id=news_id).delete()
    messages.success(request,'ลบข่าวสารเรียบร้อยแล้ว')
    return redirect('InformationHome')

def pdf_genScholar(request,info_id):
    name = Scholar_info.objects.filter(id = info_id)
    name = name[0].si_name
    datas = Scholar_app.objects.filter(sa_si_id=info_id)
    return render(request,'appilcationList_addmin/printlist.html',{'datas':datas,'name':name})


@login_required (login_url='index')           
@user_passes_test(lambda u: u.is_superuser)     
def checkInfoAdmin(request,home_id,user_id):
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    

    file_obj = None
    if(len(File_Models.objects.filter(fm_upload_by = user_obj,fm_Scholar = home_id,fm_state=0)) != 0):
        file_obj = File_Models.objects.filter(fm_upload_by = user_obj,fm_Scholar = home_id,fm_state=0)
        file_obj= file_obj[0]

    checkin = Scholar_app.objects.filter(sa_userid = user_obj,sa_si_id = home_id)
    checkin = checkin[0]
    json = checkin.sa_json_scholar
    json_bro = checkin.sa_bro_n_sis
    data2  = avatar_profile.objects.filter(sa_userid=user_obj)
    data2 = data2[0]
    return render(request,'appilcationList_addmin/checkInfoAdmin.html',{'checkin':checkin,'info_id':home_id,'pic':data2,'file':file_obj,'json':json,'json_bro':json_bro})

@login_required (login_url='index')           
@user_passes_test(lambda u: u.is_superuser)     
def payment_admin (request,home_id,user_id):
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    info_obj = Scholar_info.objects.filter(id =home_id).get()
    if len(File_Models.objects.filter(fm_upload_by = user_obj,fm_Scholar = info_obj,fm_state=2)) != 0 or File_Models.objects.filter(fm_upload_by = user_obj,fm_Scholar = info_obj,fm_state=2)[0].fm_file != None:

        file_obj = File_Models.objects.filter(fm_upload_by = user_obj,fm_Scholar = info_obj,fm_state=2)
        
        file_obj = file_obj[0]
        return render(request,'payment/payment_admin.html',{'file_upload':file_obj,'home_id':home_id,'user_id':user_id})
    else:
        
        messages.success(request,'นิสิตยังไม่ได้อัพโหลดไฟล์เอกสาร')
        return redirect("/secondAppilcationAdmin/"+str(home_id))

def editPayment(request,info_id,user_id):
    user_obj = User.objects.filter(id=user_id)
    user_obj = user_obj[0]
    info_obj = Scholar_info.objects.filter(id =info_id).get()
    today = datetime.now()+timedelta(days=3)
    Scholar_app.objects.filter(sa_userid=user_obj,sa_si_id=info_obj).update(
        sa_status = 34 , sa_statusExDate = today)
    return redirect("/changeStatus/"+str(info_id) +"/"+str(user_id)+"/1")


    
