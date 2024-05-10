"""The users app views"""

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import base36_to_int
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

# views
from base.views.generic import BaseListView
from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from parameters.models import Parameter

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import UserCreationForm
from users.forms import UserForm
from users.forms import UserWithGroupsForm
from users.models.user import User


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(  # noqa: PLR0913
    request,
    uidb36=None,
    token=None,
    token_generator=default_token_generator,
    current_app=None,
    extra_context=None,
):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """
    if uidb36 is None or token is None:
        msg = "uidb36 and token are required"
        raise ValueError(msg)
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(
            request,
            messages.INFO,
            _("Your email address has been verified."),
        )
    else:
        messages.add_message(request, messages.ERROR, _("Invalid verification link"))

    return redirect("login")


class LoginView(auth_views.LoginView):
    """view that renders the login"""

    template_name = "registration/login.html"
    form_class = AuthenticationForm
    title = _("Login")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title

        return context

    def get_form_class(self):
        parameter = Parameter.value_for("ENABLE_LOGIN_RECAPTCHA")
        if parameter:
            return CaptchaAuthenticationForm
        return super().get_form_class()


class PasswordChangeView(auth_views.PasswordChangeView):
    """view that renders the password change form"""

    template_name = "registration/password_change_form.html"


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    """view that handles the recover password process"""

    template_name = "registration/password_reset_form.html"
    email_template_name = "emails/password_reset.txt"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """view that handles the recover password process"""

    template_name = "registration/password_reset_confirm.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """View that shows a success message to the user"""

    template_name = "registration/password_reset_done.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """View that shows a success message to the user"""

    template_name = "registration/password_reset_complete.html"


class UserListView(BaseListView):
    model = User
    template_name = "users/list.html"
    permission_required = "users.view_user"
    ordering = ("first_name", "last_name")

    def get_queryset(self):
        queryset = super().get_queryset()

        # search users
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.search(q)

        return queryset.prefetch_related("groups")


class UserCreateView(BaseCreateView):
    model = User
    form_class = UserCreationForm  # TODO Consider using captcha
    template_name = "users/create.html"
    title = _("Registration")

    def form_valid(self, form):
        form.save(verify_email_address=True, request=self.request)
        messages.add_message(
            self.request,
            messages.INFO,
            _(
                "An email has been sent to you. Please "
                "check it to verify your email.",
            ),
        )

        return redirect("home")


class UserDetailView(BaseDetailView):
    model = User
    template_name = "users/detail.html"
    permission_required = "users.view_user"

    def get_context_object_name(self, obj) -> str | None:
        return None


class UserUpdateView(BaseUpdateView):
    model = User
    form_class = UserWithGroupsForm
    template_name = "users/update.html"
    permission_required = "users.change_user"

    def get_context_object_name(self, obj) -> str | None:
        return None

    def get_object_detail_url(self) -> str:
        return reverse("user_detail", args=(self.object.pk,))

    def get_cancel_url(self):
        return self.get_object_detail_url()

    def get_success_url(self):
        return self.get_object_detail_url()


class UserDeleteView(BaseDeleteView):
    model = User
    template_name = "users/delete.html"
    permission_required = "users.delete_user"

    def get_context_object_name(self, obj) -> str | None:
        return None


class UserProfileView(UserDetailView):
    permission_required = ()
    title = _("My profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user


class UserProfileEditView(UserUpdateView):
    form_class = UserForm
    permission_required = ()
    title = _("Edit profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def get_object_detail_url(self) -> str:
        return reverse("user_profile")
