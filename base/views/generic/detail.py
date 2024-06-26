from django.views.generic import DetailView

from ..mixins import LoginPermissionRequiredMixin


class BaseDetailView(LoginPermissionRequiredMixin, DetailView):
    login_required = True
    permission_required = ()
    title = None

    def get_title(self):
        if self.title is not None:
            return self.title
        verbose_name = self.model._meta.verbose_name
        return f"{verbose_name}: {self.object}".title()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["opts"] = self.model._meta
        context["title"] = self.get_title()

        return context
