from __future__ import annotations
from dataclasses import replace
from tokenize import Floatnumber
from urllib import request
from django.shortcuts import render, redirect
from .models import Athlete, Meet, User, Event, Performance
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q,Sum, Max, Min, OuterRef, Subquery
from .forms import AthleteForm, PerformanceForm, MyUserCreationForm, UserForm
from datetime import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.db import connection


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def TopAthletes(Field,Male):
    

    sql1 = 'select PerformanceMinusAthlete.performance_id,MarkRawLarge,MarkRawSmall,EventName,CY, Mark, group_concat(Athlete) as Athletes  FROM ' \
        '(' \
        'select performance_id,MarkRawLarge,MarkRawSmall,EventName,CY, Mark from ' \
        '(' \
        'select performance_id,MarkRawLarge,MarkRawSmall,EventID_id,CY, Mark from base_performance ' \
        'inner join ' \
        '(' \
        'select * from base_performance_AthleteID ' \
        'inner JOIN ' \
        'base_athlete on '\
        'base_performance_AthleteID.athlete_id = base_athlete.id ' \
        'where Male=0) as AthletesMatch ' \
        'on AthletesMatch.performance_id = base_performance.id ' \
        'order by EventID_id,MarkRawLarge,MarkRawSmall) as tmp ' \
        'inner join base_event on base_event.id=tmp.EventID_id ' \
        'where Current=1 and FieldEvent=0 ' \
        'group by EventName) as PerformanceMinusAthlete ' \
        'inner JOIN(select performance_id,Athlete from base_performance_AthleteID ' \
        'inner JOIN ' \
        'base_athlete ' \
        'on base_performance_AthleteID.athlete_id = base_athlete.id) as AthletesCombined ' \
        'on AthletesCombined.performance_id = PerformanceMinusAthlete.performance_id ' \
        'group by  PerformanceMinusAthlete.performance_id,MarkRawLarge,MarkRawSmall,EventName,CY, Mark ' \
        'order by EventName' 

    if Field == True:
        sql1 = sql1.replace('order by EventID_id,MarkRawLarge,MarkRawSmall','order by EventID_id,MarkRawLarge DESC,MarkRawSmall DESC')
        sql1 = sql1.replace('FieldEvent=0','FieldEvent=1')
    if Male == True:
        sql1 = sql1.replace('where Male=0','where Male=1')

    with connection.cursor() as cursor:
        cursor.execute(sql1)
        row = dictfetchall(cursor)    
    return row

def TopAllEvents():
   
    performancesmen = Performance.objects.filter(id=OuterRef('pk'),AthleteID__Male=False).values('EventID').annotate(topMark=Max('MarkRawLarge')).order_by()   
    performancesmen = Performance.objects.filter(AthleteID__Male=False).values('EventID').annotate(topMark=Max('MarkRawLarge')).order_by()   
    return performancesmen

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    qr = request.GET.get('qr') if request.GET.get('qr') != None else ''
    
    if qr != '':
        active_athletes = Athlete.objects.filter(Athlete__icontains=qr).order_by('Athlete')
        mobilemode = "ActiveAthletes"
    else:
        active_athletes = Athlete.objects.filter(Active=1).order_by('Athlete')
        inactive_athletes =  Athlete.objects.filter(Active=0).order_by('Graduation','Athlete')
        mobilemode = ''
    inactive_athletes =  Athlete.objects.filter(Active=0).order_by('Graduation','Athlete')
    TopMaleField = TopAthletes(True,True)
    TopMaleRun = TopAthletes(False,True)
    TopFemaleField = TopAthletes(True,False)
    TopFemaleRun = TopAthletes(False,False)
    TopAllEvents()
    meets = Meet.objects.all()
    events = Event.objects.all()
    performance_newest_first = Performance.objects.order_by('-updated')[0:5]
    performance_needapproval = Performance.objects.filter(Confirmed=0).order_by('-updated')[0:5]
  
    events_field = Event.objects.filter(FieldEvent=1,Current=1).order_by('EventName')
    events_run = Event.objects.filter(FieldEvent=0,Current=1).order_by('EventName')
    statechamps =  Performance.objects.filter(StateChamp=1).order_by('CY')
    leaderboardathletes = TopAllEvents()

    context = {'events_run':events_run,'events_field':events_field,'active_athletes':active_athletes, 
                    'performance_newest_first':performance_newest_first,'performance_needapproval':performance_needapproval,
                    'leaderboardathletes':leaderboardathletes,
                    'statechamps':statechamps,'meets':meets,'events':events,'q':q,'qr':qr,'mobilemode':mobilemode }
 
    context['inactive_athletes'] = inactive_athletes 

    TopAthletesMatrix = (TopMaleRun,TopMaleField,TopFemaleRun,TopFemaleField)
    context['TopAthletesMatrix'] = TopAthletesMatrix

    if request.method == 'POST':
        print("Post")                
    return render(request, 'base/home.html',context )


def recentActivityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    performance_newest_first = Performance.objects.order_by('-updated')[0:5]
    context = {'performance_newest_first':performance_newest_first}
    return render(request, 'base/recent_updates_mobile.html',context )


def testpage(request):
    return render(request,'base/trial.html') 

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request,"User does not exist")
                    
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')    

def registerPage(request):
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')    

    return render(request,'base/login_register.html',{'form':form})


def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
       
        if form.is_valid():
            form.save()
            
            return redirect('user-profile', pk=user.id)

    return render(request,'base/update-user.html',{'form':form})




def PerformanceTopTen(FieldEvent,pk,ShowAwaitingConfirmation):
    
    if ShowAwaitingConfirmation == True:
        if FieldEvent == 1:
            performancesmen =   Performance.objects.filter(EventID=pk,AthleteID__Male=True,Archive=0).\
                    order_by('-MarkRawLarge','-MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
            performanceswomen = Performance.objects.filter(EventID=pk,AthleteID__Male=False,Archive=0).\
                order_by('-MarkRawLarge','-MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
        else:  
            performancesmen =   Performance.objects.filter(EventID=pk,AthleteID__Male=True,Archive=0).\
                order_by('MarkRawLarge','MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
            performanceswomen = Performance.objects.filter(EventID=pk,AthleteID__Male=False,Archive=0).\
                order_by('MarkRawLarge','MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
    else:
        if FieldEvent == 1:
            performancesmen =   Performance.objects.filter(EventID=pk,AthleteID__Male=True,Archive=0,Confirmed=1).\
                    order_by('-MarkRawLarge','-MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
            performanceswomen = Performance.objects.filter(EventID=pk,AthleteID__Male=False,Archive=0,Confirmed=1).\
                order_by('-MarkRawLarge','-MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
        else:  
            performancesmen =   Performance.objects.filter(EventID=pk,AthleteID__Male=True,Archive=0,Confirmed=1).\
                order_by('MarkRawLarge','MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
            performanceswomen = Performance.objects.filter(EventID=pk,AthleteID__Male=False,Archive=0,Confirmed=1).\
                order_by('MarkRawLarge','MarkRawSmall').annotate(total_athletes=Sum('AthleteID'))[0:10]
    
    print (performancesmen)
    return{'performancesmen':performancesmen,'performanceswomen':performanceswomen}

def user_status(request):
    user = request.user
    if request.user.is_authenticated:
        if user.Maintainer == True:
            Maintainer = True
        else:
            Maintainer = False    
        if user.Editor == True:    
            Editor = True
        else:
            Editor = False    
    else:
        Maintainer = False
        Editor = False
    return (Maintainer,Editor)

def resultEvent(request,pk):

    Maintainer,Editor = user_status(request)
    if Maintainer or Editor:
        ShowAwaitingConfirmation = True
    else:
        ShowAwaitingConfirmation = False
    
    event = Event.objects.get(id=pk)

    resultscombined = PerformanceTopTen(event.FieldEvent,pk,ShowAwaitingConfirmation)
    performancesmen = resultscombined['performancesmen']
    performanceswomen = resultscombined['performanceswomen'] 
    performance_men_women = (performancesmen,performanceswomen)

    event = Event.objects.get(id=pk)
    

    context = {'performance_men_women':performance_men_women,'event':event}
    context['Maintainer'] = Maintainer
    context['Editor'] = Editor
    return render(request,'base/results.html',context)    


def createAthlete(request):
   
    form = AthleteForm()
    
    if request.method == 'POST':
        form = AthleteForm(request.POST)
       
        if form.is_valid():
            print('Athlete',request.POST.get('Athlete'))
            AthleteVarChar = request.POST.get('Athlete')
            if AthleteVarChar == '':
                print('Uau')
            form.save()
            
            return redirect('home')

    return render(request,'base/update-athlete.html',{'form':form})

def updateAthlete(request,pk):
    athlete = Athlete.objects.get(id=pk)
    form = AthleteForm(instance=athlete)
    
    if request.method == 'POST':
        form = AthleteForm(request.POST, request.FILES, instance=athlete)
       
        if form.is_valid():
            form.save()
            
            return redirect('home')

    return render(request,'base/update-athlete.html',{'form':form})

def searchAthlete(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    athletes = Athlete.objects.filter(Athlete__icontains=q)
    context = {'athletes':athletes}
    return render(request,'base/athlete-search.html',context)

def viewAthlete(request,pk):
   
    athlete = Athlete.objects.get(id=pk)
    performanceResults = Performance.objects.filter(AthleteID=athlete.id,Archive=False)
    context = {'performanceResults':performanceResults,'athlete':athlete}

    return render(request,'base/view-athlete.html',context)


def numberdecimals(inputnumber):
    print("input",inputnumber)
    numberstr = str(inputnumber)
    decimallocation = numberstr.find(".")
    
    return decimallocation

def HumanReadableMark(rawmarklarge,rawmarksmall,measuretype):
    # print('Measure Type: ' + str(measuretype) )
    if measuretype == "inches":
        measure_human = str(rawmarklarge) + "-" + str(rawmarksmall)
        temp = {'measure_human':measure_human}
        temp['measurelabel1'] = "Feet"
        temp['measurelabel2'] = "Inches"
        return temp
     
    elif measuretype == "seconds":
        temp = dict()
        markseconds = float(rawmarksmall)
        markminute = rawmarklarge
        # digits = len(str(markseconds))
        number_dec = numberdecimals(markseconds)

        digits  = int(float(number_dec))
        print ("Digits",digits)
        if digits > 1:
            fillerstr = ":"
        else:
            fillerstr = ":0"

         
        if int(markminute) != 0:
            measure_human = str(markminute) + fillerstr + str(markseconds)
        else:
            measure_human = str(markseconds)

        temp['measure_human'] = measure_human
        temp['measurelabel1'] = "Minutes"
        temp['measurelabel2'] = "Seconds"
        return temp

    elif measuretype == "points":
        temp = dict()
        measure_human = str(rawmarklarge) 
        temp['measure_human'] = measure_human
        temp['measurelabel1'] = "Points"
        temp['measurelabel2'] = "Null"
        return temp
    
    return -1

def calculateRawMark(measure1,measure2,measuretype):
    print('Entering Calc Raw Mark')
    print(measure1)
    if measuretype == "inches":
        print("calc")
        return int(measure1) * 12 + float(measure2)

    elif measuretype == "seconds":
        print("Hello")
        print (measure1)
        return int(measure1) * 60 + float(measure2)
    elif measuretype == "points":
        return int(measure1)
        
    return -1

def convert_form_time_2_db_time(strTime):
   
    dbenttrydate = datetime.strptime(strTime,'%m/%d/%Y')
    return dbenttrydate

def convert_db_time_2_form_time(dbtime):
    # Check if not time inputed and Return None
    if dbtime is not None:
        return dbtime.strftime('%m/%d/%Y')
    else:
        return dbtime

@login_required(login_url='/login')
def updatePerformance(request,pk):
  
  
    # UserStatus = {'Maintainer':request.user.Maintainer,'Editor':request.user.Editor}

    performance = Performance.objects.get(id=pk)  
    athletes = Athlete.objects.filter(performance__id=pk)
    eventID = performance.EventID_id
    eventtemp = Event.objects.get(id=eventID)
    measure_system = eventtemp.MeasurementSystem

    eventselectcontext = {'MarkRaw':0}
    form = PerformanceForm(instance=performance,athletepk=athletes,eventselect=eventselectcontext)
 
    
    measuresystem = HumanReadableMark(performance.MarkRawLarge,performance.MarkRawSmall,measure_system)
    performancedate = convert_db_time_2_form_time(performance.EventDate)
    eventname = performance.EventID
   
    context = {'form':form,'measure':measuresystem,'eventdate':performancedate,'EventID':eventID,
                'EventName':eventname,'Maintainer':request.user.Maintainer,'Editor':request.user.Editor}
            

    if request.method == 'POST':
        if 'Update' in request.POST:
            
            if form.is_valid():
                print('Valid')
            else:
                print('not valid')
                print(form.is_valid())
                print(form.errors)
                messages.error(request,"Form not valid")

            eventid = request.POST.get('EventID')
            meetid = request.POST.get('MeetID')
            athleteid = request.POST.get('AthleteID')
            event, created = Event.objects.update_or_create(id=eventid)
            meet, created = Meet.objects.update_or_create(id=meetid)

            athlete, created = Athlete.objects.update_or_create(id=athleteid)
            performance.EventID = event
            
            performance.MeetID = meet
            athleteid = athlete
       
            pdate = request.POST.get('EventDateDP')
            # If no date is give, keep CY date since Event Date is Unknown

            if (pdate != 'None'):
                dbenttrytime = datetime.strptime(pdate,'%m/%d/%Y')
                performance.EventDate = dbenttrytime.strftime('%Y-%m-%d')
                performance.CY = dbenttrytime.strftime('%Y')

            performance.MarkRawLarge = request.POST.get('MarkRawLarge')
            performance.MarkRawSmall =  request.POST.get('MarkRawSmall')
            calcmeasure = HumanReadableMark(request.POST.get('MarkRawLarge'),request.POST.get('MarkRawSmall'),measure_system)            
            performance.Mark = calcmeasure['measure_human']
            performance.Confirmed = True if request.POST.get('Confirmed') == "on" else False

            print("aaaa",request.POST.get('Confirmed') )
            performance.save()
          

            return redirect('results-event',pk=event.id)

        elif 'Delete' in request.POST:
            
            performance.delete()
            return redirect('home')
    return render(request,'base/update-performance.html',context)

   

@login_required(login_url='/login')
def createPerformance(request,eventid, male):
  

    athletes = Athlete.objects.filter(Active=1,Male=male)
    eventid2= {'eventid':eventid}
    form = PerformanceForm(athletepk=athletes,eventselect=eventid2)
 
    eventname = Event.objects.get(id=eventid2['eventid'])

    eventtemp = Event.objects.get(id=eventid2['eventid'])
    measure_system = eventtemp.MeasurementSystem
    context = {'form':form,'measure':measure_system,'EventID':eventid2['eventid'],'EventName':eventname.EventName}
    
    if request.method == 'POST':
        EventIDp = request.POST.get('EventID')
        MeetIDp = request.POST.get('MeetID')
        AthleteIDp = request.POST.getlist('AthleteID')

        # Check for Not Athletes
        if AthleteIDp == []:
            print("No athlete selected")
            return render(request,'base/update-performance.html',context)

        event, created = Event.objects.update_or_create(id=EventIDp)
        meet, created = Meet.objects.update_or_create(id=MeetIDp)

        # measure =  Event.objects.get(id=EventIDp)
        dbenttrytime = convert_form_time_2_db_time(request.POST.get('EventDateDP'))

        humanMark = HumanReadableMark(request.POST.get('MarkRawLarge'), request.POST.get('MarkRawSmall'),measure_system)
        
        instance = Performance.objects.create(
            
            EventID = event,
            MeetID = meet,
            Mark = humanMark['measure_human'],
            MarkRawLarge = request.POST.get('MarkRawLarge'),
            MarkRawSmall =request.POST.get('MarkRawSmall'),
            Notes = request.POST.get('Notes'),
            Archive = 0,
            EventDate = dbenttrytime.strftime('%Y-%m-%d'),
            CY = dbenttrytime.strftime('%Y')
            
        )       
     
        for athid in AthleteIDp:
            athtoadd = Athlete.objects.get(id=athid)
            instance.AthleteID.add(athtoadd)
        
        return redirect('home')

        

    return render(request,'base/update-performance.html',context)


