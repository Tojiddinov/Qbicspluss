from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_time
from django.views.generic import *
from .models import *
from .forms import *
from agents.mixins import OrganiserAndLoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import LeadModelForm
from .models import Lead
from django.contrib.auth.views import LogoutView

class SigupView(CreateView):
    template_name = "registration/signup.html"
    form_class = NewUserForm

    def get_success_url(self):
        return reverse("leads:lead-list")

class HomeView(TemplateView):
    template_name = "home.html"

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/leads_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.profile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user = self.request.user)

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(LeadListView, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     form = LeadModelForm(initial={'vremya': datetime.now().strftime('%Y-%m-%dT%H:%M')})
    #     if user.is_organisor:
    #         queryset = Lead.objects.filter(
    #             organisation=user.profile,
    #             agent__isnull=True
    #         )
    #         context.update({
    #             "unassigned_leads": queryset
    #         })
    #     return context

class LeadDetailView(OrganiserAndLoginRequiredMixin, DetailView):
    template_name = "leads/leads_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
    template_name = "leads/leads_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.profile

        # # Faqat vaqt qismi kiritilganligini tekshirish, masalan '13:00' yoki '1:00 PM'
        # vremya_input = form.cleaned_data.get('vremya')
        # if isinstance(vremya_input, str):
        #     # Agar vaqt string formatida kiritilgan bo'lsa, uni parse_time yordamida vaqt obyektiga aylantirish
        #     vremya_time = parse_time(vremya_input)
        #     if vremya_time:
        #         lead.vremya = vremya_time
        #     else:
        #         # Agar vaqt noto'g'ri formatda bo'lsa, xato qo'shish va forma novalid deb belgilash
        #         form.add_error('vremya', 'Enter a valid time.')
        #         return self.form_invalid(form)
        #
        # lead.save()

        # Lead yaratilgandan so'ng xabar jo'natish
        send_mail(
            subject="Bu lead yaratilingan",
            message="Yangi lead yarat",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )

        return super(LeadCreateView, self).form_valid(form)

# class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
#     template_name = "leads/leads_create.html"
#     form_class = LeadModelForm
#
#     def get_success_url(self):
#         return reverse("leads:lead-list")
#
#     def form_valid(self, form):
#       # `vremya` ma'lumotini validatsiya qilish
#       vremya_string = form.cleaned_data.get('vremya')
#       if isinstance(vremya_string, str):
#         vremya = parse_time(vremya_string)
#       else:
#         vremya = vremya_string.time()
#       return self.form_invalid(form)
#       # Vaqt to'g'ri bo'lsa, uni modelga saqlash
#       lead = form.save(commit=False)
#       lead.vremya = vremya_obj
#       lead.save()
#       return super().form_valid(form)
#
#     def form_valid(self, form):
#         lead = form.save(commit=False)
#         lead.organisation = self.request.user.profile
#         lead.save()
#         send_mail(
#             subject="Bu lead yaratilingan",
#             message="Yangi lead yarat",
#             from_email="test@test.com",
#             recipient_list=["test2@test.com"],
#         )
#         return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganiserAndLoginRequiredMixin, UpdateView):
    template_name = "leads/leads_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganiserAndLoginRequiredMixin, DeleteView):
    template_name = "leads/leads_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

class AssignAgentView(OrganiserAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.profile
            )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
            )
        context.update({
            "unassigned_category_leads": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation = user.profile
            )
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, DeleteView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation = user.profile
            )
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation
            )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation = user.profile
            )
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation
            )
        return queryset


    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_create_view(request):
  form = LeadModelForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('lead-list')
  context = {
    'form': form,
  }
  return render(request, "leads/lead_create.html", context)

  class LogoutViaGetView(LogoutView):
    def get(self, request, *args, **kwargs):
      return self.post(request, *args, **kwargs)
