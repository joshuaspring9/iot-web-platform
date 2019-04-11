from django.shortcuts import render

# Create your views here.

from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'dashboard/signup.html'

class UpdateProfilePic(generic.UpdateView, SuccessMessageMixin):
    '''
    A view to update the profile picture.  Functions as an update or create,
    depending on whether a user profile exists or not.
    '''
    def get_object(self, queryset=None):
        try:
            return self.request.user.profile
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateProfilePic, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateProfilePic, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.avatar_url = self.request.user.profile.avatar_url
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'dashboard/update_profile_pic.html'
    success_message = "Profile picture successfully updated!"

class DashboardView(generic.TemplateView):
    '''
    Same as a template view, but requires a logged in user to render
    '''
    login_required = True
    template_name = 'dashboard/home.html'
