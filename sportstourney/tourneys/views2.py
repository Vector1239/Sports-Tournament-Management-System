from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout 
from itertools import permutations, islice
from .models import *
import math,random

def landing(request):
    if request.method=="POST":
        return redirect('/account/')
    else: return render(request,'tourneys/landing.html')

def account(request):
    return render(request,'tourneys/account.html') 

def ulogin(request):
    if request.method=='POST':
      user=authenticate(request,username='test123',password='test123')

      if user is not None:
           login(request,user)
           return redirect('Tourney')
      else:
           messages.info(request,'Username or password is incorrect')
    return render(request,'tourneys/ulogin.html')    

def logoutUser(request):
     logout(request)
     return redirect('account')

def Tourney(request):
    return render(request,'tourneys/tour.html') 

def createT(request):
    if request.method=="POST":
         f=userg.objects.get(userg_nam='bro')
         t1=Tournament()
         t1.user_t=f
         t1.save()
         return redirect('/eventS/'+str(t1.tourney_id)+'/')
    return render(request,'tourneys/createT.html') 

def eventS(request,pk_t):
    context={'key':pk_t}
    return render(request,'tourneys/eventS.html',context) 
# Create your views here.
def noT(request):
	if request.method=="POST":
		global n
		n=int(request.POST.get('number'))
		# print(n)
		return redirect('/brackets/14')
	else: return render(request,'tourneys/noT.html')

def brackets(request,pk_e):
    res,final=makeBracket(n,pk_e)
    print("BELOW")
    print(res)
    print(final)
    i=0
    while 2 ** i < n:
        i += 1
    row=2**i
    col=2*i-1
    print(row)
    print(col)
    context={'n' : range(n),'row':range(i),'col':range(col),'res':res,'final':final,'acol':col}
    return render(request,'tourneys/gridTime.html',context)

def nth(iterable, n, default=None):
    # "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)
    
def makeBracket(n,pk_e):
    total_team = []
    for i in range(1, n + 1): total_team.append(i)
    random.shuffle(total_team)
    print(total_team)
    print("TT")
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
        #RES IS ACTUAL
        #FINAL IS INDEX
        print(res)
        print(final)
        return res,final
        # insertTeam(final,res,pk_e)
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
        # insertTeam(final,res,pk_e)
        # print(res)
