from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.list import ListView
from . import models
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.forms import inlineformset_factory
import io
from django.http import FileResponse
# from reportlab.pdfgen import canvas
def index(request):
    teamha=models.Team.objects.all()
    leagues= models.League.objects.all()
    c=0
    context = {
        'teamha': teamha,
        'leagues': leagues,
        'c' : c,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))


def chairProfile(request):
    chairr = models.Chair.objects.get(user=request.user)
    league = models.League.objects.get(chair=chairr)
    teamha= models.Team.objects.filter(league=league)
    t = teamha
    context = {
        'teamha': t,
    }
    template = loader.get_template('league_quali.html')
    return HttpResponse(template.render(context,request))

def team_detail(request, id):
    obj = get_object_or_404(models.Team, pk=id)
    teams=models.Team.objects.get(id=id)

    t=teams
    template = loader.get_template('Members.html')
    context = {
        'obj' : obj,
        't' : t.member_set.all(),
    }
    return HttpResponse(template.render(context, request))


def quali(request, id):

    team=models.Team.objects.get(id=id)
    if team.league.chair.user == request.user:
        team.Status = "Qualified"
        team.save()
        return redirect('chairProfile')
    else:
        return redirect('404')

def disquali(request, id):

    team=models.Team.objects.get(id=id)
    if team.league.chair.user == request.user:
        team.Status = "DISQualified"
        team.save()
        return redirect('chairProfile')
    else:
        return redirect('404')


def userteamView(request):
    teamha=models.Team.objects.filter(usern=request.user)

    context = {
        'Team': teamha,

    }
    template = loader.get_template('myteam.html')
    return HttpResponse(template.render(context,request))


class TeamCreate(LoginRequiredMixin,generic.CreateView):
    model = models.Team
    success_url = reverse_lazy('my-teams')
    fields = ['name','league','Affiliation','Website','City','country']


    def form_valid(self, form):

        league = form.cleaned_data['league']
        form.instance.price = league.category.price
        form.instance.usern = self.request.user
        return super().form_valid(form)

class MemberCreate(LoginRequiredMixin,generic.CreateView):
    model = models.Member
    success_url = reverse_lazy('my-teams')
    fields = ['first_name','last_name','type','Gander','email','phone_number','date_of_birth']



    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.id = get_object_or_404(models.Team, pk=kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        dd = self.kwargs['id']

        teamha=models.Team.objects.get(id=dd)
        teamha.member_set.create(self.object)
        #form.instance.team = teamha.Team_name
        return super().form_valid(form)


class TeamUpdate(LoginRequiredMixin,generic.UpdateView):
    model = models.Team
    fields = ('name','league','Affiliation','Website','City','country',)
    success_url = reverse_lazy('my-teams')
    def get_queryset(self):
        queryset = super(TeamUpdate, self).get_queryset()
        queryset = queryset.filter(usern=self.request.user)
        return queryset

class TeamDelete(LoginRequiredMixin,generic.DeleteView):
    model = models.Team
    success_url = reverse_lazy('my-teams')
    def get_queryset(self):
        queryset = super(TeamDelete, self).get_queryset()
        queryset = queryset.filter(usern=self.request.user)
        return queryset

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
#new method

def manage_team(request, id):
    Team = models.Team.objects.get(pk=id)

    if request.user == Team.usern:

        MemberInlineFormSet = inlineformset_factory(models.Team, models.Member, fields=('team','first_name','last_name','Gander','type','email','phone_number','date_of_birth'),extra=3)
        if request.method == "POST":
            formset = MemberInlineFormSet(request.POST, request.FILES, instance=Team )
            if formset.is_valid():
                formset.save()
                # Do something. Should generally end with a redirect. For example:
                return HttpResponseRedirect(Team.get_absolute_url())
        else:
            formset = MemberInlineFormSet(instance=Team)


        return render(request, 'registrations/member_formss.html', {'formset': formset})
    else:
        return render(request,'404.html')

def finish(request,id):
    team = models.Team.objects.get(id=id)
    team.Status = 'Finish'
    team.save()
    members = team.member_set.all()
    Student = 0
    Parent = 0
    Supervisor =0
    for member in members:
        if member.type == 'Student':
            Student+=1
        elif member.type == 'Parent':
            Parent+=1
        elif member.type == 'Supervisor':
            Supervisor+=1
    sprice = models.Membertype.objects.get(name='Student',category=team.league.category)
    context = {
        'Student': sprice.price,
        'team' : team,
        'Parent': Parent,
        'Supervisor': Supervisor,
    }
    template = loader.get_template('finish.html')
    return HttpResponse(template.render(context,request))

from __future__ import unicode_literals
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from . import models

@login_required
def pdf(request, donation_id):
    donation = get_object_or_404(models.Member, pk=donation_id, user=request.user)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename={date}-{name}-donation-receipt.pdf".format(
        date=donation.created.strftime('%Y-%m-%d'),
        name=slugify(donation.donor_name),
    )
    html = render_to_string("pdf.html", {
        'members': donation,
    })

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return respon
