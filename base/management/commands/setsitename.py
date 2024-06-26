from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = "Set the default django.contrib.sites Site"  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument(
            "--name",
            dest="site_name",
            default=None,
            help="Default site name.",
        )
        parser.add_argument(
            "--domain",
            dest="site_domain",
            default=None,
            required=True,
            help="Default site domain.",
        )

    def handle(self, *args, **options):
        if not apps.is_installed("django.contrib.sites"):
            msg = "The sites framework is not installed."
            raise CommandError(msg)

        from django.contrib.sites.models import Site

        domain = options["site_domain"]
        name = options["site_name"] or domain

        if not domain:
            msg = "Domain cannot be empty."
            raise CommandError(msg)

        site_id = settings.SITE_ID
        try:
            site = Site.objects.get(pk=site_id)

            if domain and domain == site.domain and (name and name == site.name):
                self.stdout.write("Nothing to update.")
            else:
                if name and name != site.name:
                    site.name = name
                if domain and domain != site.domain:
                    site.domain = domain

                site.save()
                self.stdout.write(
                    "Updated default site. "
                    "Restart Django as sites are cached aggressively."
                )
        except Site.DoesNotExist:
            msg = (
                f"Default site with pk={site_id} does not exist. "
                "Creating default site."
            )
            self.stdout.write(msg)
            site = Site.objects.create(pk=site_id, name=name, domain=domain)

        msg = """Default Site:
\tid = {:d}
\tname = {:s}
\tdomain = {:s}
"""
        self.stdout.write(msg.format(site.id, site.name, site.domain))
