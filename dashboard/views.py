from django.shortcuts import render

# Create your views here.

from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from api.models import DataFile


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

@login_required
def dashboard(request, data_file_id):
    data_file = get_object_or_404(DataFile, pk=data_file_id)

    dic = {
            'processed': data_file.processed,
            'start_time': data_file.start_time,
            'end_time': data_file.end_time,
            'devices_captured': data_file.devices_captured,
        }


    if data_file.processed:
        try:
            handle = data_file.processed_file.open()
            contents = handle.read()
            handle.close()
        except:
            contents = ""

        dic['contents'] = contents
    
    return render(request, 'dashboard/home.html', dic)

@login_required
def dashboard_list(request):
    return render(request, 'dashboard/home.html', {
            'data_files': DataFile.objects.all(),
        })

class AccountView(LoginRequiredMixin, generic.TemplateView ):
    """
    Same as template view, but login is required
    """
    template_name = 'dashboard/account.html'