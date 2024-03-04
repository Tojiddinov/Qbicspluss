import random
from django.views import generic
from django.shortcuts import reverse
from django.core.mail import send_mail
from leads.models import Agent, UserProfile
from .mixins import OrganiserAndLoginRequiredMixin
from .forms import AgentModelForm

class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agents_lists.html"

    def get_queryset(self):

        organisation = self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agents_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organisor = True
        user.is_agent = True

        user_profile = UserProfile.objects.create(user=user,
                                                  status=form.cleaned_data['status'],
                                                  sex=form.cleaned_data['sex'],
                                                  oboruduvania=form.cleaned_data['oboruduvania'],
                                                  uchastok=form.cleaned_data['uchastok'])



        Agent.objects.create(
            user=user,
            organisation=user_profile
        )
        send_mail(
            subject="Bu Agent yaratilingan",
            message="Yangi Agent yaratilgan",
            from_email="Email@gmail.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agents_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agents_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

    def form_valid(self, form):
      user = form.save(commit=False)
      if 'password' in form.changed_data:
        user.set_password(form.cleaned_data['password'])
      user.save()
      agent = self.get_object()
      agent.save()

    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agents_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")



