# standard library
import subprocess
import traceback


def print_to_dos():
    try:
        common_args = (
            "rg",
            "--word-regexp",
            "--pretty",
        )

        # We write this string in this way because if we write it plainly, it will
        # detect itself.
        pattern = f"{'T'}ODO|{'F'}IXME"
        subprocess.run(  # noqa: PLW1510
            (  # noqa: S603
                *common_args,
                "--ignore-file=project/.todoignore",
                pattern,
                ".",
            ),
        )
        subprocess.run(  # noqa: PLW1510
            (  # noqa: S603
                *common_args,
                "--glob=*.env*",
                pattern,
                ".",
            ),
        )
        # Run twice because of unoverridable precedences
        # (See https://github.com/BurntSushi/ripgrep/issues/1734#issuecomment-730769439)
    except Exception:  # noqa: BLE001
        # Continue instead of breaking runserver
        print(traceback.format_exc())  # noqa: T201
