import copy

import pytest

import pip_run.deps as deps


class TestInstallCheck:
    def test_installed(self):
        assert deps.pkg_installed('pip-run')

    def test_not_installed(self):
        assert not deps.pkg_installed('not_a_package')

    def test_installed_version(self):
        assert not deps.pkg_installed('pip-run==0.0')

    def test_not_installed_args(self):
        args = [
            '-i',
            'https://devpi.net',
            '-r',
            'requirements.txt',
            'pip-run',
            'not_a_package',
            'pip-run==0.0',
        ]
        expected = copy.copy(args)
        expected.remove('pip-run')
        filtered = deps.not_installed(args)
        assert list(filtered) == expected


@pytest.mark.usefixtures('run_mode')
class TestLoad:
    def test_no_args_passes(self):
        """
        If called with no arguments, load() should still provide
        a context.
        """
        with deps.load():
            pass

    def test_only_options_passes(self):
        """
        If called with only options, but no installable targets,
        load() should still provide a context.
        """
        with deps.load('-q'):
            pass


@pytest.mark.usefixtures('run_mode')
def test_target_mode_context():
    """Verify a target exists or can be created."""
    mode = deps.mode()
    with mode.context([]) as target:
        target.mkdir(exist_ok=True)
