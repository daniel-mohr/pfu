"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

aggregation of tests

run with::

  env python3 setup.py run_unittest

or::

  env python3 setup.py run_pytest

Or you can run this script directly (only the tests definded in this file)::

  env python3 main.py

  pytest-3 main.py

Or you can run only one test, e. g.::

  env python3 main.py TestModuleImport.test_module_import

  pytest-3 -k TestModuleImport main.py
"""

import subprocess
import unittest


class TestModuleImport(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25
    """

    def test_module_import(self):
        """
        tests the import of the module and the submodules

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # pylint: disable=unused-variable
        # pylint: disable=bad-option-value,import-outside-toplevel
        # pylint: disable=unused-import
        import pfu_module
        import pfu_module.check_checksum
        import pfu_module.checksum_tools
        import pfu_module.create_checksum
        import pfu_module.replicate
        import pfu_module.replicate.script
        import pfu_module.replicate.tools
        import pfu_module.scripts
        import pfu_module.simscrub
        import pfu_module.simscrub.script
        import pfu_module.simscrub.scrubbing
        import pfu_module.simscrub.tools
        import pfu_module.speed_test
        import pfu_module.speed_test.script


class TestScriptExecutable(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25
    """

    def test_script_fuse_git_bare_fs_executable(self):
        """
        test if all scripts (with all commands) are executable

        :Author: Daniel Mohr
        :Date: 2021-05-25
        """
        # pylint: disable=invalid-name
        for cmd in ['pfu -h', 'pfu simscrub -h',
                    'pfu create_checksum -h', 'pfu check_checksum -h',
                    'pfu replicate -h', 'pfu speed_test -h']:
            out = subprocess.check_output(
                cmd,
                shell=True)
            # check at least minimal help output
            self.assertGreaterEqual(len(out), 775)
            # check begin of help output
            self.assertTrue(out.startswith(
                b'usage: pfu '))


def scripts(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-05-17
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    add tests for the scripts
    """
    print('add tests for the scripts')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(TestScriptExecutable))
    # pfu simscrub
    suite.addTest(loader.loadTestsFromName(
        'tests.script_pfu_simscrub'))
    # pfu create_checksum
    suite.addTest(loader.loadTestsFromName(
        'tests.script_pfu_create_checksum'))
    # pfu check_checksum
    suite.addTest(loader.loadTestsFromName(
        'tests.script_pfu_check_checksum'))
    # pfu replicate
    suite.addTest(loader.loadTestsFromName(
        'tests.script_pfu_replicate'))
    # pfu speed_test
    suite.addTest(loader.loadTestsFromName(
        'tests.script_pfu_speed_test'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
