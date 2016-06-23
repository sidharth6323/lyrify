from django.shortcuts import render, render_to_response, HttpResponse, RequestContext
import urllib
import json
from bs4 import BeautifulSoup
import re
from django.core.mail import send_mail
from django.template.loader import render_to_string

def angular(request):
    return render_to_response("angular.html",{})


def handleMatch(match):
    #for match in soup.find_all("match"):
    	m_id = match['id']
        series = match['srs']
        mtype = match['type']
        if mtype== "TEST":
            return;
        match_desc = match["mchdesc"]
        states = match.find_all("state")
        for state in states:
            match_cstate = state["mchstate"]
            mstatus = state["status"]
            if match_cstate == "Result":
                return; 
            if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                return;
        ground = match["grnd"]
        try:
            batting_team = match.find("bttm")
            bowling_team = match.find("blgtm")
            batting_team_name = batting_team["sname"]
            bowling_team_name = bowling_team["sname"]
            innings = match.find_all("inngs")
            bat_runs = innings[0]["r"]
            bat_overs = innings[0]["ovrs"]
            bat_wkts = innings[0]["wkts"]
        except Exception:
            batting_team = None
            bowling_team = None
            batting_team_name = None
            bowling_team_name = None
            innings = None
            bat_runs = None
            bat_overs = None
            bat_wkts = None
        try:
            bowl_runs = innings[1]["r"]
            bowl_overs = innings[1]["ovrs"]
            bowl_wkts = innings[1]["wkts"]
        except:
            bowl_runs = None
            bowl_overs = None
            bowl_wkts= None
            pass
        return {"ID":m_id, "Series": series, "Match_Format": mtype, "Team":match_desc, "Venue":ground, "Match_State":match_cstate,"Match_Status":mstatus, "Batting_team":batting_team_name, "Bowling_team":bowling_team_name, "Batting_Team_Runs":bat_runs, "Batting_Team_Overs":bat_overs, "Batting_Team_Wickets":bat_wkts, "Bowling_Team_Runs":bowl_runs, "Bowling_Team_Overs": bowl_overs, "Bowling_Team_Wickets": bowl_wkts }
                       
        #print series,mtype,match_desc,ground,mstatus, batting_team_name, bowling_team_name, bat_runs, bat_overs
        #time.sleep(100000)
        #print bat_wkts, bowl_runs, bowl_overs, bowl_wkts

def all_matches(request):
    b=[]
    url="http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
    res=urllib.urlopen(url)
    html=res.read()
    soup=BeautifulSoup(html,"html5lib")
    for match in soup.find_all("match"):
                a={}
                if handleMatch(match):
                        b.append(handleMatch(match))
    return HttpResponse(json.dumps(b))










#-------------lyrify starts-----------------------


def about(request):
	return render_to_response("about.html",{})

def report(request):
	if request.method=="POST":
		name=request.POST.get("name")
		email=request.POST.get("email")
		bug=request.POST.get("bug")
		msg_html=""
		if name and email and bug:
			msg_html= render_to_string('email_template.html', {'name': name,'email':email,'bug':bug})
			send_mail('Lyrify Bug Report','hey','sidharth6323@gmail.com',("sidharth6323@gmail.com",),html_message=msg_html)
			status="Your Bug has been reported. Thanks for Feedback"
		else:
			status="All fields are mandatory"
	else:
		status=""
	return render_to_response("report.html",{'status':status},context_instance=RequestContext(request))


def base(request):
	return render_to_response("base.html",{})
	
def hindi(request,year,month,song):
	query=song
	try:
		url="http://www.lyricsmint.com/%s/%s/%s.html"%(year,month,song)
		res=urllib.urlopen(url)
		html=res.read()
		soup=BeautifulSoup(html,"html5lib")
		div=soup.find("div",{"id":"lyric"})
		if div:
			data=div.find("p").get_text()
		else:
			div=soup.find("div",{"class":"post-entry"})
			data=div.get_text()
	except:
		data=""
	return render_to_response("hindi.html",{"data":data,"query":query})

# Create your views here.
def english(request):
	singer=request.GET.get("singer")
	song=request.GET.get("song")
	try:
		si=singer.replace(" ","")
		so=song.replace(" ","")
		url="http://www.azlyrics.com/lyrics/%s/%s.html"%(si.lower(),so.lower())
		res=urllib.urlopen(url)
		html=res.read()
		soup=BeautifulSoup(html,"html.parser")
		ringtone=soup.find("div",{"class":"ringtone"})
		a=ringtone.find_next("div")
		data=a.get_text()
	except:
		data=""
		pass
	return render_to_response("english.html",{"data":data,"singer":singer,"song":song})

def search(request):
	query=request.GET.get("song")
	if query:
			try:
				url="http://search.azlyrics.com/search.php?q=%s"%(query)
				res=urllib.urlopen(url)
				html=res.read()
				soup=BeautifulSoup(html,"html5lib")
				a=[]
				table=soup.find_all("table",{"class":"table table-condensed"})[-1]
				for i in table.find_all("td",{"class":"text-left visitedlyr"}):
					result=i.find_next("a")
					temp=result.find_next("b")
					song=result["href"].split('/')[-1].replace(".html","")
					singer=result["href"].split('/')[-2]
					a.append((result.get_text()+" by "+temp.find_next("b").get_text(),"singer=%s&song=%s"%(str(singer),str(song))))
			except:
				a=""
				
			# hindi scraping
			try:	
				b=[]
				url2="http://www.lyricsmint.com/search?q=%s"%(query)
				res2=urllib.urlopen(url2)
				html2=res2.read()
				soup2=BeautifulSoup(html2,"html5lib")
				for i in soup2.find_all("div",{"class":"post-title"}):
					result2=i.find("a")
					search2=result2["href"].split('/')
					search_final=search2[-3].replace("?","")+"/"+search2[-2]+"/"+search2[-1].replace(".html","")
					b.append((i.get_text(),search_final))
			except:
				b=""
				
			#return HttpResponse(json.dumps({'a': a,'b':b,'query':query}))
	else:
		a=""
		b=""
	return render_to_response("search.html",{"a":a,"b":b,"query":query})

def scorecard(request,id):
    url="http://www.cricbuzz.com/api/html/cricket-scorecard/"+id
    res=urllib.urlopen(url)
    html=res.read()
    soup=BeautifulSoup(html,"html5lib")
    Match_Status=soup.find("div").get_text()
    innings_1=soup.find("div",{"id":"innings_1"})
    i1_main_div=innings_1.find("div")
    i1_info=i1_main_div.find("div").get_text()
    temp=0
    i1_bat_all=[]
    for p in i1_main_div.find_all("div",{"class":"cb-col cb-col-100 cb-scrd-itms"}):
        i1_bat=p
        i1_bat_p= i1_bat.find("div")
        i1_bat_curr=i1_bat_p.find_next("div")
        i1_bat_runs=i1_bat_curr.find_next("div")
        i1_bat_balls=i1_bat_runs.find_next("div")
        i1_bat_4s=i1_bat_balls.find_next("div")
        i1_bat_6s=i1_bat_4s.find_next("div")
        i1_bat_sr=i1_bat_6s.find_next("div")
        if i1_bat_p.get_text()=="Extras":
            break;
        i1_bat_dict={}
        i1_bat_dict["i1_bat_p"]    =  i1_bat_p.get_text()
        i1_bat_dict["i1_bat_curr"] =  i1_bat_curr.get_text()
        i1_bat_dict["i1_bat_runs"] =  i1_bat_runs.get_text()
        i1_bat_dict["i1_bat_balls"]=  i1_bat_balls.get_text()
        i1_bat_dict["i1_bat_4s"]   =  i1_bat_4s.get_text()
        i1_bat_dict["i1_bat_6s"]   =  i1_bat_6s.get_text()
        i1_bat_dict["i1_bat_sr"]   =  i1_bat_sr.get_text()
        i1_bat_all.append(i1_bat_dict)
    '''i1_bat=innings_1.find("table")
    i1_bat_table=i1_bat.find_all("tr")
    temp=0
    i1_bat_all=[]
    for p in i1_bat_table:
        if temp==0:
            temp=temp+1
            continue 
        i1_bat_p=p.find("td")
        i1_bat_curr=i1_bat_p.find_next("td")
        i1_bat_runs= i1_bat_curr.find_next("td")
        i1_bat_balls=i1_bat_runs.find_next("td")
        i1_bat_4s=i1_bat_balls.find_next("td")
        i1_bat_6s=i1_bat_4s.find_next("td")
        i1_bat_sr=i1_bat_6s.find_next("td")
        i1_bat_dict={}
        i1_bat_dict["i1_bat_p"]    =  i1_bat_p.get_text()
        i1_bat_dict["i1_bat_curr"] =  i1_bat_curr.get_text()
        i1_bat_dict["i1_bat_runs"] =  i1_bat_runs.get_text()
        i1_bat_dict["i1_bat_balls"]=  i1_bat_balls.get_text()
        i1_bat_dict["i1_bat_4s"]   =  i1_bat_4s.get_text()
        i1_bat_dict["i1_bat_6s"]   =  i1_bat_6s.get_text()
        i1_bat_dict["i1_bat_sr"]   =  i1_bat_sr.get_text()
        i1_bat_all.append(i1_bat_dict)
'''
    #end of for 

    i1_bat_fow=i1_main_div.find_next("div",{"class":"cb-col cb-col-100 cb-col-rt cb-font-13"})
    i1_bowl=i1_bat_fow.find_next("div",{"class":"cb-col cb-col-100 cb-ltst-wgt-hdr"})
    i1_bat_all.append({'i1_bat_fow':i1_bat_fow.get_text()})
    i1_bowl_all=[]
    temp=0
    for q in i1_bowl.find_all("div",{"class":"cb-col cb-col-100 cb-scrd-itms "}):
        i1_bowl_p=q.find("div")
        i1_bowl_overs=i1_bowl_p.find_next("div")
        i1_bowl_maiden = i1_bowl_overs.find_next("div")
        i1_bowl_runs = i1_bowl_maiden.find_next("div")
        i1_bowl_wicket = i1_bowl_runs.find_next("div")
        i1_bowl_nb = i1_bowl_wicket.find_next("div")
        i1_bowl_wd = i1_bowl_nb.find_next("div")
        i1_bowl_eco = i1_bowl_wd.find_next("div")
        i1_bowl_dict={}
        i1_bowl_dict['i1_bowl_p']     = i1_bowl_p.get_text()
        i1_bowl_dict['i1_bowl_overs'] = i1_bowl_overs.get_text()
        i1_bowl_dict['i1_bowl_maiden']= i1_bowl_maiden.get_text()
        i1_bowl_dict['i1_bowl_runs']  = i1_bowl_runs.get_text()
        i1_bowl_dict['i1_bowl_wicket']= i1_bowl_wicket.get_text()
        i1_bowl_dict['i1_bowl_nb']    = i1_bowl_nb.get_text()
        i1_bowl_dict['i1_bowl_wd']    = i1_bowl_wd.get_text()
        i1_bowl_dict['i1_bowl_eco']   = i1_bowl_eco.get_text()
        i1_bowl_all.append(i1_bowl_dict)
    innings_1={"i1_info":i1_info,"i1_bat":i1_bat_all,"i1_bowl":i1_bowl_all}
    
    # innings 2

    innings_2=soup.find("div",{"id":"innings_2"})
    i2_main_div=innings_2.find("div")
    i2_info=i2_main_div.find("div").get_text()
    temp=0
    i2_bat_all=[]
    for r in i2_main_div.find_all("div",{"class":"cb-col cb-col-100 cb-scrd-itms"}):
        i2_bat=r 
        i2_bat_p=r.find_next("div")
        i2_bat_curr=i2_bat_p.find_next("div")
        i2_bat_runs= i2_bat_curr.find_next("div")
        i2_bat_balls=i2_bat_runs.find_next("div")
        i2_bat_4s=i2_bat_balls.find_next("div")
        i2_bat_6s=i2_bat_4s.find_next("div")
        i2_bat_sr=i2_bat_6s.find_next("div")
        if i2_bat_p.get_text()=="Extras":
            break;
        i2_bat_dict={}
        i2_bat_dict["i2_bat_p"]    =  i2_bat_p.get_text()
        i2_bat_dict["i2_bat_curr"] =  i2_bat_curr.get_text()
        i2_bat_dict["i2_bat_runs"] =  i2_bat_runs.get_text()
        i2_bat_dict["i2_bat_balls"]=  i2_bat_balls.get_text()
        i2_bat_dict["i2_bat_4s"]   =  i2_bat_4s.get_text()
        i2_bat_dict["i2_bat_6s"]   =  i2_bat_6s.get_text()
        i2_bat_dict["i2_bat_sr"]   =  i2_bat_sr.get_text()
        i2_bat_all.append(i2_bat_dict)

    i2_bat_fow=i2_main_div.find_next("div",{"class":"cb-col cb-col-100 cb-col-rt cb-font-13"})
    i2_bowl=i2_bat_fow.find_next("div",{"class":"cb-col cb-col-100 cb-ltst-wgt-hdr"})
    i2_bat_all.append({'i2_bat_fow':i2_bat_fow.get_text()})
    i2_bowl_all=[]
    for s in i2_bowl.find_all("div",{"class":"cb-col cb-col-100 cb-scrd-itms "}):
        i2_bowl_p=s.find("div")
        i2_bowl_overs=i2_bowl_p.find_next("div")
        i2_bowl_maiden = i2_bowl_overs.find_next("div")
        i2_bowl_runs = i2_bowl_maiden.find_next("div")
        i2_bowl_wicket = i2_bowl_runs.find_next("div")
        i2_bowl_nb = i2_bowl_wicket.find_next("div")
        i2_bowl_wd = i2_bowl_nb.find_next("div")
        i2_bowl_eco = i2_bowl_wd.find_next("div")
        i2_bowl_dict={}
        i2_bowl_dict['i2_bowl_p']     = i2_bowl_p.get_text()
        i2_bowl_dict['i2_bowl_overs'] = i2_bowl_overs.get_text()
        i2_bowl_dict['i2_bowl_maiden']= i2_bowl_maiden.get_text()
        i2_bowl_dict['i2_bowl_runs']  = i2_bowl_runs.get_text()
        i2_bowl_dict['i2_bowl_wicket']= i2_bowl_wicket.get_text()
        i2_bowl_dict['i2_bowl_nb']    = i2_bowl_nb.get_text()
        i2_bowl_dict['i2_bowl_wd']    = i2_bowl_wd.get_text()
        i2_bowl_dict['i2_bowl_eco']   = i2_bowl_eco.get_text()
        i2_bowl_all.append(i2_bowl_dict)
    innings_2={"i2_info":i2_info,"i2_bat":i2_bat_all,"i2_bowl":i2_bowl_all}


    scorecard={"Match_Status":Match_Status,"innings_1":innings_1,"innings_2":innings_2}
    return HttpResponse(json.dumps(scorecard))


def commentary(request,m_id):
    url="http://push.cricbuzz.com/match-api/"+m_id+"/commentary-full.json"
    res=urllib.urlopen(url)
    html=json.loads(res.read())
    comm=[]
    for i in html["comm_lines"][::-1]:
        try:
            line=i["comm"]
        except:
            line=""
        try:
            o_summary=i['o_summary']
        except:
            o_summary=""
        if o_summary:
            a={"comm_line":line,"o_summary":o_summary}
        else:
            a={"comm_line":line}
        comm.append(a)
    return HttpResponse(json.dumps(comm),content_type='application/json')