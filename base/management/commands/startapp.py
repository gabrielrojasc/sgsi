import os
import re
import shutil

from importlib import import_module

from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand

# others libraries
# utils
from inflection import camelize
from inflection import pluralize
from inflection import singularize
from inflection import underscore


class AppTemplateCommand(TemplateCommand):
    rewrite_template_suffixes = (
        # Allow shipping invalid .py files without byte-compilation.
        (".py-tpl", ".py"),
        (".html-tpl", ".html"),
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            help="Name of the application or project.",
        )
        parser.add_argument(
            "directory",
            nargs="?",
            help="Optional destination directory",
        )
        parser.add_argument(
            "--model-name",
            help="Name fo the defauld model of the app.",
        )
        parser.add_argument(
            "--template",
            help="The path or URL to load the template from.",
            default="project/app_template",
        )
        parser.add_argument(
            "--extension",
            "-e",
            dest="extensions",
            action="append",
            default=["py"],
            help='The file extension(s) to render (default: "py"). '
            "Separate multiple extensions with commas, or use "
            "-e multiple times.",
        )
        parser.add_argument(
            "--name",
            "-n",
            dest="files",
            action="append",
            default=[],
            help="The file name(s) to render. Separate multiple extensions "
            "with commas, or use -n multiple times.",
        )


class Command(AppTemplateCommand):
    help = (  # noqa: A003
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name, target = options.pop("name"), options.pop("directory")

        if options.get("model_name"):
            model_name = options.pop("model_name")
            snake_case_model_name = underscore(model_name)
        else:
            snake_case_model_name = singularize(app_name)
            model_name = camelize(snake_case_model_name)

        options["model_name"] = model_name
        options["snake_case_model_name"] = snake_case_model_name
        options["lower_case_model_name"] = model_name.lower()
        options["model_verbose_name"] = snake_case_model_name.replace("_", " ")
        options["plural_model_verbose_name"] = pluralize(options["model_verbose_name"])
        options["plural_model_name"] = camelize(
            pluralize(options["plural_model_verbose_name"]),
        )
        options["app_name"] = app_name

        self.validate_name(app_name, "app")

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                "%r conflicts with the name of an existing Python module and "
                "cannot be used as an app name. Please try another name." % app_name,
            )

        super().handle("app", app_name, target, **options)

        templates_dir = f"{app_name}/templates/{app_name}/"

        for root, _dirs, files in os.walk(templates_dir):
            for html_file in files:
                html_file_path = f"{root}{snake_case_model_name}_{html_file}"
                shutil.move(
                    f"{root}{html_file}",
                    html_file_path,
                )

                # custom parser to replace variables on html templates
                with open(html_file_path) as file:
                    file_content = file.read()
                for var, value in options.items():
                    template_var = f"{{{{ {var} }}}}"
                    file_content = re.sub(
                        re.escape(template_var), str(value), file_content
                    )
                with open(html_file_path, "w") as file:
                    file.write(file_content)
