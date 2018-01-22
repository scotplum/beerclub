from __future__ import division
from django.db.models import Avg, Count
from django.db.models.functions import Lower
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Club, Club_User, Club_Announcement, Club_Event, Club_Application
from event.models import Event, Event_Address
from forms import ClubForm, ClubAnnouncementForm, ClubDisplayForm
from event.forms import EventForm, EventAddressForm, EventEditForm, EventAddressEditForm
from django.forms import modelformset_factory
from home.models import Wanted_Beers, Beer_Banner, Beer_Score
from django.utils import timezone
import datetime
from operator import itemgetter
from beerclub.decorators import user_is_admin
from beerclub.utils import navigation, mobile
from django.core.mail import send_mail

# Create your views here.
context = {}

@login_required
def index(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    context['club_user_check'] = Club_User.objects.filter(user=user_object).exists()
    return render(request, 'club/index.html', context)  

@login_required	
def club(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    club_beer = []
    club_admin = Club_User.objects.filter(club=crowd).filter(is_admin=True).select_related('user','club')
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    club_db_user_check = Club_User.objects.filter(club=crowd).filter(user=user_object).exists()
    club_application_pending_check = Club_Application.objects.filter(club=crowd).filter(user=user_object).filter(status='pending').exists()
    club_admin_pending_check = Club_Application.objects.filter(club=crowd).filter(status='pending').exists()
    context['admin'] = Club_User.objects.filter(club=crowd).filter(is_admin=True).values_list('user__email')
    context['club_admin'] = club_admin
    context['club_admin_check'] = club_admin_check
    context['crowd_announcement_check'] = crowd_announcement_check
    context['club_event_check'] = club_event_check
    context['club_user_check'] = club_user_check
    context['crowd'] = crowd
    context['club_db_user_check'] = club_db_user_check
    context['club_application_pending_check'] = club_application_pending_check
    context['club_admin_pending_check'] = club_admin_pending_check
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd).select_related('club')
		context['crowd_announcement'] = crowd_announcement
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd).order_by('-event__event_date').select_related('club', 'event')
		context['club_event'] = club_event
    user_beer_rating = []    
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd).filter(is_active=True).select_related('user','club').order_by(Lower('user__username'))
		context['club_user'] = club_user
		club_users = Club_User.objects.filter(club=crowd).values_list('user')
		club_scores = Beer_Score.objects.filter(user__in=club_users, is_active=True).values('bdb_id', 'beer_company', 'beer_name', 'brewery_id').annotate(count=Count('bdb_id')).annotate(average=Avg('score')).order_by('-average', 'beer_name')[:20]
		context['club_scores'] = club_scores
		club_wanted_beers = Wanted_Beers.objects.filter(user__in=club_users, is_active=True).values('bdb_id', 'beer_company', 'beer_name').annotate(count=Count('bdb_id')).order_by('-count','beer_name')[:15]
		context['club_wanted_beers'] = club_wanted_beers
    if request.method == "POST": 
		rp = request.POST
		if 'apply' in rp:
			#If the applicant already has an application for this crowd in pending status then skip this step (used in case of a refresh issue)
			if club_application_pending_check:
				pass
			else:
				if crowd.auto_approve == True:
					club_member = Club_Application(user=user_object, club=crowd, status='accepted')
					club_member.date_completed = datetime.datetime.now()
					club_member.save()
					club_user_add = Club_User(user=user_object, club=crowd, is_active=True)
					club_user_add.save()
					#Email to applicant / new member
					email_to = user_object.email
					email_from = 'The Beer Crowd <noreply@thebeercrowd.com>'
					email_subject = '[The Beer Crowd]' + crowd.name + 'Application Accepted'
					email_body = 'Congratulations, your application to ' + crowd.name + ' has been accepted.\n\nTheBeerCrowd' 
					send_mail(email_subject, email_body, email_from, [email_to]) 
				else:
					club_member = Club_Application(user=user_object, club=crowd)
					club_member.save()
					#Email to applicant
					email_to = user_object.email
					email_from = 'The Beer Crowd <noreply@thebeercrowd.com>'
					email_subject = '[The Beer Crowd] ' + crowd.name + ' Application Submitted'
					email_body = user_object.username + ',\n\n' + 'Your application to the crowd ' + crowd.name + ' was submitted successfully.  You will receive another email once your application status has changed.  You may also check your membership status at the top of the ' + crowd.name + ' crowd page.\n\nTheBeerCrowd' 
					send_mail(email_subject, email_body, email_from, [email_to])
					#Email to administrators notifying them of a new applicant
					#admin = Club_User.objects.filter(club=crowd).filter(is_admin=True).values_list('user__email')
					email_to = []
					for email in Club_User.objects.filter(club=crowd).filter(is_admin=True):
						email_to.append(str(email.user.email))
					email_from = 'The Beer Crowd <noreply@thebeercrowd.com>'
					email_subject = '[The Beer Crowd] ' + crowd.name + ' Application Submitted for ' + user_object.username
					email_body = crowd.name + ' admins,\n\nAn application to the crowd ' + crowd.name + ' was submitted for ' + user_object.username +'. Please review at your earliest convenience. \n\nTheBeerCrowd' 
					send_mail(email_subject, email_body, email_from, email_to)
			return redirect('/club/' + id + '/')
		if 'removeannouncement' in rp:
			announcement_id = request.POST.get("removeannouncement")
			club_announcement = Club_Announcement.objects.get(id=announcement_id)
			club_announcement.is_active = False
			club_announcement.save()
			return redirect('/club/' + id + '/')
    return render(request, 'club/club.html', context) 
	
@login_required
@user_is_admin
def manage(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/manage.html', context)  

@login_required
@user_is_admin	
def announcement(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    crowd_announcement_check = Club_Announcement.objects.filter(club=crowd).exists()
    context['crowd_announcement_check'] = crowd_announcement_check
    if crowd_announcement_check:
		crowd_announcement = Club_Announcement.objects.filter(club=crowd)
		context['crowd_announcement'] = crowd_announcement
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/manage_announcement.html', context)  
	
@login_required
@user_is_admin
def editannouncement(request, id, announcement_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    crowd_announcement = Club_Announcement.objects.get(id=announcement_id)
    context['crowd_announcement'] = crowd_announcement
    form = ClubAnnouncementForm(instance=crowd_announcement)
    context['form'] = form
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = ClubAnnouncementForm(request.POST)
        post_info = request.POST
        if form.is_valid():
			updated_announcement = crowd_announcement
			updated_announcement.announcement = post_info['announcement']
			date_added = post_info['date_added']
			updated_announcement.date_added = datetime.datetime.strptime(date_added, '%m/%d/%Y')
			if 'is_active' in post_info:
				updated_announcement.is_active = True
			else:
				updated_announcement.is_active = False
			updated_announcement.save()
			return redirect('/club/' + id + '/')
        else:
			context['form_errors'] = form
    return render(request, 'club/editannouncement.html', context)
	
@login_required
@user_is_admin
def newannouncement(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['form'] = ClubAnnouncementForm()
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = ClubAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = crowd
            announcement.save()
            return redirect('/club/' + str(crowd.id) + '/')
        else:
			context['form_errors'] = form
    return render(request, 'club/newannouncement.html', context)

@login_required
@user_is_admin	
def about(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    context['form'] = ClubForm(instance=crowd)
    if request.method == 'POST':
        form = ClubForm(request.POST)
        post_info = request.POST
        if form.is_valid():
            updated_crowd = crowd
            updated_crowd.bio = post_info['bio']
            updated_crowd.name = post_info['name']
            updated_crowd.city = post_info['city']
            updated_crowd.state = post_info['state']
            post_info_established = post_info['established']
            updated_crowd.established = datetime.datetime.strptime(post_info_established, '%m/%d/%Y').strftime('%Y-%m-%d')
            updated_crowd.annual_fee = post_info['annual_fee']
            if 'is_public' in post_info:
				updated_crowd.is_public = True
            else:
				updated_crowd.is_public = False
            updated_crowd.save()
            context['form'] = ClubForm(instance=crowd)
            return redirect('/club/' + id + '/')
        else:
			context['form'] = form
    return render(request, 'club/about.html', context)  

@login_required
@user_is_admin	
def membership(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    club_user_check = Club_User.objects.filter(club=crowd).exists()
    context['club_user_check'] = club_user_check
    club_pending_user_check = Club_Application.objects.filter(club=crowd).filter(status='pending').exists()
    context['club_pending_user_check'] = club_pending_user_check
    if club_pending_user_check:
		club_pending_user = Club_Application.objects.filter(club=crowd).filter(status='pending')
		context['club_pending_user'] = club_pending_user
    club_inactive_user_check = Club_User.objects.filter(club=crowd).filter(is_active=False).exists()
    context['club_inactive_user_check'] = club_inactive_user_check
    if club_user_check:
		club_user = Club_User.objects.filter(club=crowd)
		context['club_user'] = club_user
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == "POST": 
		rp = request.POST
		if 'inactivate' in rp:
			member_id = request.POST.get("inactivate")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_active = False
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'setactive' in rp:
			member_id = request.POST.get("setactive")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_active = True
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'removeadmin' in rp:
			member_id = request.POST.get("removeadmin")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_admin = False
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'addadmin' in rp:
			member_id = request.POST.get("addadmin")
			club_member = Club_User.objects.get(id=member_id, club=crowd)
			club_member.is_admin = True
			club_member.save()
			return redirect('/club/' + id + '/manage/membership/')
		elif 'acceptpending' in rp:
			member_id = request.POST.get("acceptpending")
			member_object = User.objects.get(id=member_id)
			club_member = Club_Application.objects.get(user=member_object, club=crowd, status='pending')
			club_member.status = 'accepted'
			club_member.date_completed = datetime.datetime.now()
			club_member.save()
			club_user_add = Club_User(user=member_object, club=crowd, is_active=True)
			club_user_add.save()
			email_to = member_object.email
			email_from = 'The Beer Crowd <noreply@thebeercrowd.com>'
			email_subject = '[The Beer Crowd] ' + crowd.name + ' Application Accepted'
			email_body = member_object.username + ',\n\n' + 'Congratulations, your application to the crowd ' + crowd.name + ' has been accepted.  Now back to the beer!\n\nTheBeerCrowd' 
			send_mail(email_subject, email_body, email_from, [email_to]) 
			return redirect('/club/' + id + '/manage/membership/')
		elif 'rejectpending' in rp:
			member_id = request.POST.get("rejectpending")
			member_object = User.objects.get(id=member_id)
			club_member = Club_Application.objects.get(user=member_object, club=crowd, status='pending')
			club_member.status = 'rejected'
			club_member.date_completed = datetime.datetime.now()
			club_member.save()
			email_to = member_object.email
			email_from = 'The Beer Crowd <noreply@thebeercrowd.com>'
			email_subject = '[The Beer Crowd] ' + crowd.name + ' Application Declined'
			email_body = member_object.username + ',\n\n' + 'Your application to the crowd ' + crowd.name + ' has been declined.  The usual reason for this is simply that the crowd is not accepting new members.  Not to worry, there are plenty of crowds that would appreciate your membership.\n\nTheBeerCrowd' 
			send_mail(email_subject, email_body, email_from, [email_to]) 
			return redirect('/club/' + id + '/manage/membership/')
    return render(request, 'club/membership.html', context)  

@login_required
@user_is_admin	
def event(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    club_event_check = Club_Event.objects.filter(club=crowd).exists()
    if club_event_check:
		club_event = Club_Event.objects.filter(club=crowd).order_by('-event__event_date').select_related()
		context['club_event'] = club_event
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/event.html', context)
	
@login_required
@user_is_admin	
def display(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['crowd'] = crowd
    context['form'] = ClubDisplayForm(instance=crowd)
    if request.method == 'POST':
        form = ClubDisplayForm(request.POST)
        post_info = request.POST
        if form.is_valid():
            updated_crowd = crowd
            if 'disp_members' in post_info:
				updated_crowd.disp_members = True
            else:
				updated_crowd.disp_members = False
            if 'auto_approve' in post_info:
				updated_crowd.auto_approve = True
            else:
				updated_crowd.auto_approve = False
            if 'require_real_name' in post_info:
				updated_crowd.require_real_name = True
            else:
				updated_crowd.require_real_name = False
            updated_crowd.display_member_vote = post_info['display_member_vote']
            updated_crowd.display_wanted_beer = post_info['display_wanted_beer']
            updated_crowd.save()
            context['form'] = ClubDisplayForm(instance=crowd)
            return redirect('/club/' + id + '/')
    return render(request, 'club/display.html', context)

@login_required
def add(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    context['form'] = ClubForm()
    if request.method == 'POST':
        form = ClubForm(request.POST)
        context['form'] = form
        if form.is_valid():
            crowd = form.save()
            crowd.is_active = True
            crowd.save()
            club = Club.objects.get(id=crowd.id)
            crowd_user = Club_User(user=user_object, club=club, is_admin=True, is_active=True)
            crowd_user.save()
            return redirect('/club/' + str(crowd.id) + '/')
    return render(request, 'club/add.html', context)

@login_required	
def search(request):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    public_crowds = Club.objects.filter(is_public=True).filter(is_active=True).select_related()
    context['public_crowds'] = public_crowds
    context['state_index'] = {"ZZ":"Website Only", "AL":"Alabama","AK":"Alaska","AS":"American Samoa","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District Of Columbia","FM":"Federated States Of Micronesia","FL":"Florida","GA":"Georgia","GU":"Guam","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MH":"Marshall Islands","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","MP":"Northern Mariana Islands","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PW":"Palau","PA":"Pennsylvania","PR":"Puerto Rico","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VI":"Virgin Islands","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
    return render(request, 'club/search.html', context)
	
@login_required
@user_is_admin
def addevent(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['form'] = EventForm(club=id)
    context['crowd'] = crowd
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.is_active = True
            event.save()
            event_object = Event.objects.get(id=event.id)
            crowd_event = Club_Event(club=crowd, event=event_object)
            crowd_event.save()
            return redirect('/club/' + str(crowd.id) + '/')
        else:
			context['form'] = form
    return render(request, 'club/addevent.html', context)
	
@login_required
@user_is_admin
def newaddress(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    context['form'] = EventAddressForm()
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = EventAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.club = crowd
            address.save()
            return redirect('/club/' + str(crowd.id) + '/manage/event/')
    return render(request, 'club/newaddress.html', context)

@login_required
@user_is_admin
def address(request, id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    event_address = Event_Address.objects.filter(club=crowd)
    context['event_address'] = event_address
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    return render(request, 'club/address.html', context)  
	
@login_required
@user_is_admin
def editaddress(request, id, address_id):
    context = {}
    nav = navigation(request)
    user_object = nav['user_object']
    context = nav['context']
    crowd = Club.objects.get(id=id)
    event_address = Event_Address.objects.get(id=address_id)
    context['form'] = EventAddressEditForm(instance=event_address)
    context['crowd'] = crowd
    club_admin_check = Club_User.objects.filter(club=crowd).filter(user=user_object).filter(is_admin=True).exists()
    context['club_admin_check'] = club_admin_check
    if request.method == 'POST':
        form = EventAddressEditForm(request.POST, instance=event_address)
        if form.is_valid():
            form.save()
            return redirect('/club/' + str(crowd.id) + '/manage/event/')
    return render(request, 'club/editaddress.html', context)