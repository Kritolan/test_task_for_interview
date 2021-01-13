import tempfile

import nox
from nox.sessions import Session


locations = "test_task", "tests.py", "noxfile.py"
nox.options.sessions = "lint", "mypy", "tests"


def install_with_constraints(session: Session, *args, **kwargs) -> None:  # type: ignore
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.9"])
def tests(session: Session) -> None:
    session.run("poetry", "install", external=True)
    session.run("pytest", "tests.py")


@nox.session(python=["3.9"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-black",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.9")
def black(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.9")
def mypy(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", "--strict", "--ignore-missing-imports", *args)
