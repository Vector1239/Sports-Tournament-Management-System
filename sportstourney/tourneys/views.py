from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout 
from itertools import permutations, islice
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,Group
from .models import *
import math,random

def landing(request):
    if request.method=="POST":
        return redirect('/login_register/'+str(0)+'/')
    else: 
        eve=Event.objects.all()[:5]
        te=Tournament.objects.all()[:5]
        print(len(eve))
        context={'lene':len(eve),'fulle':eve,'te':te}
        return render(request,'tourneys/new_homepage.html',context)
        

def my_view(request):
    numbers = range(5)
    return render(request, 'tourneys/new_homepage.html', {'numbers': numbers})

def account(request):
    if request.user.is_authenticated:
          return redirect('userP')
    return render(request,'tourneys/account.html') 

def ulogin(request):
    if request.user.is_authenticated:
          return redirect('userP')
    if request.method=='POST':
      ruser=request.POST.get("loginin")
      passin=request.POST.get("passin")
      user=authenticate(request,username=ruser,password=passin)
      print(user)
      if user is not None:
           # print('yay')
           login(request,user)
           return redirect('userP')
      else:
          print('No')
          messages.info(request,'Username or password is incorrect')
    return render(request,'tourneys/ulogin.html') 

def uregister(request):
    if request.user.is_authenticated:
          return redirect('userP')
    if request.method=='POST':
        ssuser=request.POST.get("suser")
        # print(ssuser)
        spassword=request.POST.get("spass")
        smail=request.POST.get("smail")
        if(len(ssuser) == 0 or len(spassword) == 0 or len(smail) == 0):
            messages.info(request,'Incomplete Field')
            # print("BURH")
            smail="~"
            return render(request,'tourneys/registers.html') 
        UserModel = get_user_model()
        if UserModel.objects.filter(username=smail).exists():
            messages.info(request,'Email is in use.')
            return render(request,'tourneys/registers.html') 
            # return render(request,'tourneys/uregister.html')
        # user = User(username= smail, password = spassword)     
        user=UserModel.objects.create_user(username=smail, password=spassword)
        user.is_superuser=False
        user.is_staff=False
        us=userg()
        us.userg_nam=ssuser
        us.userg_email=smail
        us.save()
        user.save()
        return redirect('/account/')
      # ruser=request.POST.get("loginin")
      # passin=request.POST.get("passin")
      # user=authenticate(request,username=ruser,password=passin)
      # # print(passin)
      # if user is not None:
      #      # login(request,user)
      #      return redirect('Tourney')
      # else:
      #      messages.info(request,'Username or password is incorrect')
    return render(request,'tourneys/registers.html')  

def login_register(request,pk_e):
    getGroup()
    if request.user.is_authenticated:
        if pk_e==0:  return redirect('userP')
        else: return redirect('/regr/'+str(pk_e)+'/')
    if request.method=='POST':
        # a=request.POST.get("loginn")
        # b=request.POST.get("registerr")
        # print(a)
        # print(b)
        if 'loginn' in request.POST: 
            ruser=request.POST.get("loginin")
            passin=request.POST.get("passin")
            user=authenticate(request,username=ruser,password=passin)
            print(user)
            if user is not None:
                # print('yay')
                login(request,user)
                if pk_e==0: return redirect('userP')
                else: return redirect('/regr/'+str(pk_e)+'/')
            else:
                print('No')
                messages.info(request,'Username or password is incorrect')
        else:
            mode=request.POST.get("language")
            print(mode)
            ssuser=request.POST.get("suser")
            # print(ssuser)
            spassword=request.POST.get("spass")
            smail=request.POST.get("smail")
            print(ssuser,spassword,smail)
            if(len(ssuser) == 0 or len(spassword) == 0 or len(smail) == 0):
                messages.info(request,'Incomplete Field')
                # print("BURH")
                smail="~"
                return render(request,'tourneys/login_register.html') 
            UserModel = get_user_model()
            if UserModel.objects.filter(username=smail).exists():
                messages.info(request,'Email is in use.')
                return render(request,'tourneys/login_register.html')
                # return render(request,'tourneys/uregister.html')
            # user = User(username= smail, password = spassword)     
            user=UserModel.objects.create_user(username=smail, password=spassword)
            user.is_superuser=False
            user.is_staff=False
            us=userg()
            us.userg_nam=ssuser
            us.userg_email=smail
            us.save()
            user.save()
            #Adding in AdminORg
            if mode == "Admin":
                my_group = Group.objects.get(name='AdminOrg')
                my_users = User.objects.filter(username=smail)
                for my_user in my_users:
                    my_group.user_set.add(my_user)
            else:
                my_group = Group.objects.get(name='Viewer')
                my_users = User.objects.filter(username=smail)
                for my_user in my_users:
                    my_group.user_set.add(my_user)
            if pk_e==0:return redirect('/login_register/'+str(0)+'/')
            else: return redirect('/regr/'+str(pk_e)+'/')
    return render(request,'tourneys/login_register.html')

def getGroup():
     global ug
     ug = Group.objects.get(name="AdminOrg").user_set.all()

def regr(request,pk_e):
     eve=Event.objects.get(eve_id=pk_e)
     context={'eve':eve}
     if request.method=='POST':
            tnum=request.POST.get("event_name")
            t=Team()
            t.tem_name=tnum
            t.tem_pos=0
            e=Event.objects.get(eve_id=pk_e)
            t.eve_n=e
            t.save()
            return redirect('/indeve/'+str(pk_e)+'/')


     return render(request,'tourneys/partreg.html',context)

def about_us(request):
    
    # print("eeeeeeeeeeeeeeeeeeeeeeeeeee")
    return render(request,'tourneys/about_us.html')
    
def contact_us(request):
    # print("eeeeeeeeeeeeeeeeeeeeeeeeeee")
    return render(request,'tourneys/contact_us.html')

def logoutUser(request):
     logout(request)
     return redirect('/login_register/'+str(0)+'/')

def userP(request):
    sus=Tournament.objects.all()
    mine=request.user 
    ct=0
    if str(mine)=="hackathon":
        logout(request)
        return redirect('account')
    a1=userg.objects.get(userg_email=mine)
    uname=a1.userg_nam
    uid=a1.userg_id 
    te=Tournament.objects.filter(user_t=uid)
       
    for i in sus:
        # print(i.user_t)
        # print(uname)
        if str(i.user_t)== uname:
            ct+=1
    print(ct)
    context={'name':uname,'count':ct,'te':te,'ug':ug}
    return render(request,'tourneys/userp.html',context) 

def tourcreate(request):
    mine=request.user 
    ct=0
    a1=userg.objects.get(userg_email=mine)
    uid=a1.userg_id
    print(uid)
    if request.method=='POST':
        t=Tournament()
        t.user_t=a1
        t.tourney_nam=request.POST.get("tor_name")
        t.tourney_org=request.POST.get("org_name")
        t.date_created=request.POST.get("start_date")
        t.date_ended=request.POST.get("end_date")
        # print(susdate)
        t.save()
        return redirect('/userP/')
    return render(request,'tourneys/tourcreate.html') 


def Tourney(request):
    return render(request,'tourneys/tour.html') 

def fullEvent(request,pk_t):
    eve=Event.objects.filter(tour_n=pk_t)
    ted=Tournament.objects.get(tourney_id=pk_t)
    print(len(eve))
    context={'lene':len(eve),'fulle':eve,'pk_t':pk_t,'ted':ted,'ug':ug}
    return render(request,'tourneys/fullEvent.html',context) 

def evecreate(request,pk_t):
    eve=Event.objects.filter(tour_n=pk_t)
    duh=Tournament.objects.get(tourney_id=pk_t)
    if request.method=='POST':
        e=Event()
        e.tour_n=duh
        e.eve_nam =request.POST.get("event_name")
        e.eve_sport=request.POST.get("sport")
        e.eve_no_teams=request.POST.get("noteams")
        e.eve_info=request.POST.get("event_info")
        e.eve_date=request.POST.get("event_date")
        e.eve_venue=request.POST.get("venue")
        e.eve_mode=request.POST.get("event_mode")
        # print(susdate)
        e.save()
        return redirect('/fullEvent/'+str(duh.tourney_id)+'/')
    return render(request,'tourneys/evecreate.html')

def AllTourney(request):
    mine=request.user 
    ct=0
    a1=userg.objects.get(userg_email=mine)
    uid=a1.userg_id
    nie=Tournament.objects.filter(user_t=uid)
    context={'len':len(nie),'full':nie,'ug':ug}
    return render(request,'tourneys/AllTourney.html',context) 

def createT(request):
    if request.method=="POST":
         f=userg.objects.get(userg_nam='bro')
         t1=Tournament()
         t1.user_t=f
         t1.save()
         return redirect('/eventS/'+str(t1.tourney_id)+'/')
    return render(request,'tourneys/createT.html') 

def indeve(request,pk_e):
    getGroup()
    ern=Event.objects.get(eve_id=pk_e)
    a=Team.objects.filter(eve_n_id=pk_e)
    ern.eve_no_teams=a.count()
    ern.save()
    context={'ern':ern,'ug':ug}
    return render(request,'tourneys/indeve.html',context)

def eventS(request,pk_t):
    context={'key':pk_t}
    return render(request,'tourneys/eventS.html',context) 

def math(request,pk_e):
    tem=Team.objects.filter(eve_n=pk_e)
    vs=[]
    a=[]
    b=[]
    c=0
    for i in tem:
        if(i.tem_by == 0):
             vs.append(i.tem_name)
        # if(c<2):
        #     vs.append(i.tem_name)
        #     c+=1
        # else:
        #     tl.append(vs)
        #     vs=[]
        #     c=0
    # print(tl)
    c=0
    for i in vs:
        if c==0 or c%2==0:
            a.append(i)
        else: b.append(i)
        c+=1

    bold = zip(a, b)
    context={'bold':bold}
    return render(request,'tourneys/matches.html',context) 
# Create your views here.
def noT(request):
	if request.method=="POST":
		global n
		n=int(request.POST.get('number'))
		# print(n)
		return redirect('/brackets/14')
	else: return render(request,'tourneys/noT.html')

def brackets(request,pk_e):
    tem=Team.objects.filter(eve_n=pk_e)
    global n
    em=Event.objects.get(eve_id=pk_e)
    n=em.eve_no_teams
    if em.eve_mode=="knock-out":
        if len(tem)==0:
            makeBracket(n,pk_e)
            tem=Team.objects.filter(eve_n=pk_e)
            makeMatch(pk_e,tem)
        
        #Grab the team
        tem=Team.objects.filter(eve_n=pk_e)
        #grab the matches
        met=Match.objects.filter(eve_n=pk_e)
        tem_a_name=[]
        tem_b_name=[]
        mat_rounds=[]
        for i in met:
            if i.tem_id_a==None:tem_a_name.append("TBD")
            else: 
                node=Team.objects.get(tem_id=i.tem_id_a)
                tem_a_name.append(node.tem_name)

            if i.tem_id_b==None:tem_b_name.append("TBD")
            else: 
                node=Team.objects.get(tem_id=i.tem_id_b)
                tem_b_name.append(node.tem_name)

            mat_rounds.append(i.mat_round)

        name=zip(tem_a_name,tem_b_name)
        context={'n' : n,'tem':tem,'met':met,'name':name,'rounds':mat_rounds}
        return render(request,'tourneys/gridTime.html',context)
    elif em.eve_mode=="robin":
        if len(tem)==0:
            makeRobin(n,pk_e)
        tem=Team.objects.filter(eve_n=pk_e)
        #grab the matches
        met=Match.objects.filter(eve_n=pk_e)
        tem_a_name=[]
        tem_b_name=[]
        mat_rounds=[]
        for i in met:
            if i.tem_id_a==None:tem_a_name.append("TBD")
            else: 
                node=Team.objects.get(tem_id=i.tem_id_a)
                tem_a_name.append(node.tem_name)

            if i.tem_id_b==None:tem_b_name.append("TBD")
            else: 
                node=Team.objects.get(tem_id=i.tem_id_b)
                tem_b_name.append(node.tem_name)

            mat_rounds.append(i.mat_round)
        name=zip(tem_a_name,tem_b_name)
        context={'n' : n-1,'tem':tem,'met':met,'name':name,'rounds':mat_rounds}
        return render(request,'tourneys/round_r.html',context)

def editTeam(request,pk_e):
    tem=Team.objects.filter(eve_n=pk_e)
    orig=[]
    for i in tem:
        orig.append(i.tem_name)

    # for i in tem:
    #     if i.tem_by == 0:
    #         print(i.tem_name)
    context={'tem':tem}
    if request.method=="POST":
        allnam=[]
        for i in range(1,len(tem)+1):
            io=request.POST.get('Team-'+str(i))
            if(io==""):
                allnam.append('Team '+str(i))
            else:
                allnam.append(io)
        
        for i in range(1,len(tem)+1):
            print('Team '+str(i))
            tier=Team.objects.get(tem_name=orig[i-1])
            tier.tem_name=allnam[i-1]
            tier.save()
        # print(n)
        return redirect('/indeve/'+str(pk_e)+'/')
    return render(request,'tourneys/team_edit.html',context) 

def test(request):
    t1=Team.objects.all()
    real=[]
    bye=[]
    c=0
    for i in t1:
        if c==2:
            real.append('?')
        if i.tem_by == 0:
            real.append(i.tem_name)
            c+=1
        else:
            bye.append(i.tem_name)
    sus=Bracket.objects.get(brac_id=2)
    context={'tems':t1,'n' : range(sus.brac_roun),'real':real,'bye':bye}
    return render(request,'tourneys/teest.html',context)

def nth(iterable, n, default=None):
    # "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)


def makeRobin(n,pk_e):
    total_team = []
    for i in range(1, n + 1): total_team.append(i)
    #Creating Team
    for i in range(n):
        t=Team()
        a="Team "+str(i+1)
        t.tem_name=a
        t.tem_pos=i+1
        t.tem_Round=1000
        e=Event.objects.get(eve_id=pk_e)
        t.eve_n=e
        t.save()
    #Even
    if n%2==0:
        x=1
        y=0
        node=1
        curr=2
        tot=(n*(n-1))//2
        #For 6 teams we have 5 rounds so 5 columns
        col=n-1
        prev=n+1
        row=tot//col
        rounds=[[0 for i in range(col*2)]for j in range(row)]
        for i in range(col):
            #First Round
            rounds[0][node]=1
            for j in range(1,row):
                rounds[j][node]=curr
                curr+=1
                if curr==n+1:curr=2
            node-=1
            for k in range(row):
                rounds[j][node]=curr
                j-=1
                curr+=1
                if curr==n+1:curr=2
            curr=prev-1
            prev=curr
            node+=3
        
        node=1
        for r in range(col*2):
            print(node)
            for j in range(row):
                m=Match()
                e=Event.objects.get(eve_id=pk_e)
                m.eve_n=e
                alt=Team.objects.filter(eve_n=pk_e)
                aalt=alt.filter(tem_pos=rounds[j][node-1])
                balt=alt.filter(tem_pos=rounds[j][node])
                m.tem_id_a=aalt[0].tem_id
                m.tem_id_b=balt[0].tem_id 
                m.mat_round=r+1
                m.save()
            node+=2
            if node>col*2:break

    
def makeBracket(n,pk_e):
    total_team = []
    for i in range(1, n + 1): total_team.append(i)
    random.shuffle(total_team)
    print(total_team)
    # key = random.randint(2, math.factorial(n))
    # total_team = list(nth(permutations(total_team), key))
    # print(total_team)
    if n & 1:
        no_uh = (n + 1) // 2
        no_lh = (n - 1) // 2

        i = 0
        while 2 ** i < n:
            i += 1
        no_bye = 2 ** i - n
        # print(no_bye)
        no_round = i
        bye_uh = (no_bye - 1) // 2
        bye_lh = (no_bye + 1) // 2

        no_match = n - 1

        team_uh = total_team[:no_uh]
        # print(team_uh)
        team_lh = total_team[no_uh:]
        # print(team_lh)

        pt1 = 0
        c = 0

        # byes for upper house
        for j in range(1, bye_uh + 1):
            team_uh[pt1] *= -1
            if j % 2 == 0: c += 1
            if j & 1:
                pt1 = no_uh - 1 - c
            else:
                pt1 = 0 + c

        # byes for lower house
        pt1 = no_lh - 1
        c = 0
        for j in range(1, bye_lh + 1):
            team_lh[pt1] *= -1
            if j % 2 == 0: c += 1
            if j & 1:
                pt1 = 0 + c
            else:
                pt1 = no_lh - 1 - c

        res = team_uh + team_lh
        final = []
        for i in range(1, n + 1):
            if i in res:
                final.append(res.index(i) + 1)
            else:
                final.append(res.index(-i) + 1)
        # insertTeam(res)
        print(res)
        print(final)
        insertTeam(final,res,pk_e)
        # makeMatch(final,res,pk_e)
        # print(res)
    else:
        no_uh = n // 2
        no_lh = n // 2

        i = 0
        while 2 ** i < n:
            i += 1
        no_bye = 2 ** i - n
        # print(no_bye)
        no_round = i
        bye_uh = no_bye // 2
        bye_lh = no_bye // 2

        no_match = n - 1
        # print(no_bye)
        # b=Bracket()
        # b.brac_round=no_match
        # e=Event.objects.get(eve_id=1)

        # b.breve_n=e
        # total=0
        # total+=no_bye+(n-no_bye)//2
        # div=total
        # while(True):
        #     div=div//2
        #     if div==1: break
        #     total+=div
        # b.brac_box=total
        # b.save()

        team_uh = total_team[:no_uh]
        # print(team_uh)
        team_lh = total_team[no_uh:]
        # print(team_lh)

        pt1 = 0
        c = 0

        # byes for upper house
        for j in range(1, bye_uh + 1):
            team_uh[pt1] *= -1
            if j % 2 == 0: c += 1
            if j & 1:
                pt1 = no_uh - 1 - c
            else:
                pt1 = 0 + c

        # byes for lower house
        pt1 = no_lh - 1
        c = 0
        for j in range(1, bye_lh + 1):
            team_lh[pt1] *= -1
            if j % 2 == 0: c += 1
            if j & 1:
                pt1 = 0 + c
            else:
                pt1 = no_lh - 1 - c

        res = team_uh + team_lh
        final = []
        for i in range(1, n + 1):
            if i in res:
                final.append(res.index(i) + 1)
            else:
                final.append(res.index(-i) + 1)
        # insertTeam(res)
        print(res)
        print(final)
        insertTeam(final,res,pk_e)
        # print(res)



def insertTeam(final,res,pk_e):
    # pass
    print('here ',final)
    c=0
    for i in range(1,n+1):
        t=Team()
        a="Team "+str(final[c])
        t.tem_name=a
        t.tem_pos=i
        if(res[c]>0):t.tem_Round=1
        e=Event.objects.get(eve_id=pk_e)
        t.eve_n=e
        if(res[c]<0):t.tem_Round=2
        c+=1
        t.save()


def makeMatch(pk_e,tem):
    c=0
    r=1
    if n%2==0:uh=n//2-1
    else: uh=n//2
    i=0
    #FIRST ROUND FILL UP
    while i<n:
        m=Match()
        e=Event.objects.get(eve_id=pk_e)
        m.eve_n=e
        if tem[i].tem_Round==1 and tem[i+1].tem_Round==1:
            m.tem_id_a=tem[i].tem_id
            m.tem_id_b=tem[i+1].tem_id
            m.mat_round=r
            c+=1
            m.save()
            i+=1
        i+=1
        if i>=n:
            r+=1
            break
    #Round 2
    print("Round 1 Done")
    j=0
    while j<n:
        m=Match()
        e=Event.objects.get(eve_id=pk_e)
        m.eve_n=e
        if tem[j].tem_Round==2 and tem[j+1].tem_Round==1:
            m.tem_id_a=tem[j].tem_id
            m.mat_round=r
            c+=1
            j+=1
            m.save()
        elif tem[j].tem_Round==2 and tem[j+1].tem_Round==2:
            if j==uh:
                m.tem_id_a=tem[j].tem_id
                m.mat_round=r
                c+=1
                m.save()
            else:
                m.tem_id_a=tem[j].tem_id
                m.tem_id_b=tem[j+1].tem_id
                m.mat_round=r
                c+=1
                m.save()
                j+=1
        j+=1
        if j>=n-1:
            r+=1
            break
    if j==n-1:
        if tem[j].tem_Round==2:
            m=Match()
            e=Event.objects.get(eve_id=pk_e)
            m.eve_n=e
            m.tem_id_a=tem[j].tem_id
            m.mat_round=r-1
            c+=1
            j+=1
            m.save()
            
        
    print("Round 2 Done")
    #ROUND 3 TO N
    i=1
    while 2 ** i < n:
        i += 1
    #total rounds = i
    #current round =3
    print(c)
    print("UP")
    now=2**(i-1)
    now/=4
    b=0
    for j in range(0,n-1-c):
        m=Match()
        e=Event.objects.get(eve_id=pk_e)
        m.eve_n=e
        m.mat_round=r
        m.save()
        b+=1
        if b==now:
            now/=2
            r+=1
    #put rounds

    # return redirect('/brackets/')
    