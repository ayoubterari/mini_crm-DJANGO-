from django.core.mail import send_mail
from django.shortcuts import render,redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.http import HttpResponse
from django.views import generic 
from .models import Agent, Category, lead
from .forms import CustomUserCreationForm, LeadForm, LeadModelForm

#CRUD - Create , Retrieve , Update , Delete

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"



def landing_page(request):
    return render(request,"landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list/html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for entire organisation
        if user.is_organisor:
            queryset = lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = lead.objects.filter(organisation = user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset




def lead_list(request):
    leads = lead.objects.all()
    context = {"leads":leads}
    return render(request,"leads/lead_list.html",context)

class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for entire organisation
        if user.is_organisor:
            queryset = lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = lead.objects.filter(organisation = user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    Lead = lead.objects.get(id=pk)
    context = {
        "lead": Lead
    }
    return render(request,"leads/lead_detail.html",context)


class LeadCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["elhajterari@gmail.com"]
        )
        return super(LeadCreateView,self).form_valid(form)    
     

def lead_create(request):

     form = LeadModelForm()
     if request.method =="POST":
         print("Receiving a post request")
         form = LeadModelForm(request.POST)
         if form.is_valid():
             form.save()
             print("The Lead has been created")
             return redirect("/leads")
     context = {
        "form" : form
    }
     return render(request,"leads/lead_create.html",context)



class LeadUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        return lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self):
        return reverse("leads:lead-list")






def lead_update(request, pk):
    Lead = lead.objects.get(id=pk)
    form = LeadModelForm(instance=Lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=Lead)
        if form.is_valid():
           form.save()
           return redirect("/leads")
    context = {
        "form": form,
        "lead": Lead
    }
    return render(request,"leads/lead_update.html",context)

class LeadDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    def get_queryset(self):
        user = self.request.user
        return lead.objects.filter(organisation=user.userprofile)




def lead_delete(request, pk):
    Lead = lead.objects.get(id=pk)
    Lead.delete()
    return redirect("/leads")


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category"
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
