"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-05-25, 2021-08-31
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script 'pfu replicate'

You can run this file directly::

  env python3 script_pfu_replicate.py

  pytest-3 script_pfu_replicate.py

Or you can run only one test, e. g.::

  env python3 script_pfu_replicate.py \
    ScriptPfuReplicate.test_script_pfu_replicate_1

  pytest-3 -k test_script_pfu_replicate_1 script_pfu_replicate.py
"""

import os
import subprocess
import tempfile
import unittest

try:
    from .create_random_directory_tree import create_random_directory_tree
    from .checkoutput_check_checksum import checkoutput
except (ModuleNotFoundError, ImportError):
    from create_random_directory_tree import create_random_directory_tree
    from checkoutput_check_checksum import checkoutput


class ScriptPfuReplicate(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-05-25, 2021-08-31
    """

    def test_script_pfu_replicate_1(self):
        """
        tests the script 'pfu replicate'

        :Author: Daniel Mohr
        :Date: 2021-05-25, 2021-08-31
        """
        if not os.name == 'posix':
            self.skipTest('"pfu replicate" is only working on posix systems')
            return
        # check if sha256sum is available
        cpi = subprocess.run(
            'sha256sum --version',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True,
            timeout=42, check=False)
        extraparam = ''
        if cpi.returncode != 0:
            # self.skipTest('sha256sum not available, skipping test')
            # check if sha256 is available
            cpi = subprocess.run(
                'sha256 -s foo',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=42, check=False)
            if cpi.returncode != 0:
                self.skipTest(
                    'sha256sum and sha256 not available, skipping test')
                return
            # else:
            extraparam = '-checksum_program sha256'
            extraparam += ' -checksum_create_parameter \\\"\\\"'
            extraparam += ' -checksum_check_parameter \\\"-c\\\"'
            # check parameter will not work, but produces no error
        else:  # sha256sum is available and default for pfu replicate
            extraparam = ''
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, 'src')
            dest_dirs = [os.path.join(tmpdir, 'dest1'),
                         os.path.join(tmpdir, 'dest2'),
                         os.path.join(tmpdir, 'dest3')]
            os.mkdir(src_dir)
            # create random data
            create_random_directory_tree(src_dir, levels=3)
            # create destinations
            param = '-source ' + src_dir
            param += ' -destination ' + ' '.join(dest_dirs)
            param += ' ' + extraparam
            subprocess.run(
                'pfu replicate ' + param,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True,
                timeout=28, check=True)
            # check checksums
            for dest_dir in dest_dirs:
                param = '-loglevel 20 -ignore_extension log status'
                param += ' -dir ' + dest_dir
                cpi = subprocess.run(
                    'pfu check_checksum ' + param,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True,
                    timeout=42, check=False)
                self.assertTrue(checkoutput(cpi.stderr))


if __name__ == '__main__':
    unittest.main(verbosity=2)
