from django.shortcuts import render, redirect
from datetime import date
from .models import Team, Attendance, Worker, Mark
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def index(request):
    if request.user.sinf == True:
       return redirect(f'{request.user.sinf_nomi}/attendance/')
    if request.user.der == True:
        return redirect('der')
    teams = Team.objects.all()
    return render(request, 'index.html', {'teams':teams})

def derektor(request):
    teams = Team.objects.all()
    today = date.today()
    do = Attendance.objects.filter(date=today).count()
    dq = Mark.objects.filter(is_attended='yashil',dt=today).count()
    ds = Mark.objects.filter(is_attended='ko`k').count()
    dy = Mark.objects.filter(is_attended='qizil').count()
    return render(request,'der.html',{'do':do,'dq':dq,'ds':ds,'dy':dy,'teams':teams})

def do(request):
    teams = Team.objects.all()
    today = date.today()
    sinf = Attendance.objects.filter(dt=today).order_by('-dt')
    return render(request,'hp/do.html',{'sinf':sinf,'teams':teams})

def dq(request):
    today = date.today()
    teams = Team.objects.all().order_by('-dt')
    dq = Mark.objects.filter(is_attended='yashil',dt=today)
    
    return render(request,'hp/dq.html',{'dq':dq,'teams':teams})

def ds(request):
    teams = Team.objects.all()
    ds = Mark.objects.filter(is_attended='ko`k').order_by('-dt')
    return render(request,'hp/ds.html',{'ds':ds,'teams':teams})

def dy(request):
    teams = Team.objects.all()
    dy = Mark.objects.filter(is_attended='qizil').order_by('-dt')
    return render(request,'hp/dy.html',{'dy':dy,'teams':teams})

def attendance_detail(request, team_id):
    teams = Team.objects.all()
    team = Team.objects.get(id=team_id)
    is_att_taken = True if Attendance.objects.filter(date=date.today(), team=team) else False
    return render(request, "detail.html", {'team':team, "is_att_taken":is_att_taken,'teams':teams})


def attendance_take(request, team_id):
    teams = Team.objects.all()
    team = Team.objects.get(id=team_id)
    today = date.today()
    if not Attendance.objects.filter(date=today, team=team):
        if request.method == 'POST':
            attendance = Attendance.objects.create(team=team, date=today)
            marks = []
            for worker in team.workers.all():
                is_attended= request.POST.get(f"is_attended_{worker.id}")
                mark = Mark(attendance=attendance, worker=worker, is_attended=is_attended)
                marks.append(mark)
            
            Mark.objects.bulk_create(marks)
            return  redirect('detail', team.id)    

                

        return render(request, 'take.html', {"team":team,'teams':teams})
    else:
        return HttpResponse("Davomat allaqachon olib bo'lingan")
    


def attendance_update(request, attendance_id):
    teams = Team.objects.all()
    attendance = Attendance.objects.get(id=attendance_id)
    if attendance.date == date.today():
        if request.method == "POST":
            marks = attendance.marks.all()
            for mark in marks:
                is_attended = request.POST.get(f"is_attended_{mark.id}")
                mark.is_attended = is_attended

            Mark.objects.bulk_update(marks, ['is_attended' ,])
            return redirect("detail", attendance.team.id)
                
        return render(request, "update.html", {'attendance':attendance,'teams':teams})
    else:
        return HttpResponse("Faqatagina bugungi olingan davomadlarni tahrirlash mumkin.")