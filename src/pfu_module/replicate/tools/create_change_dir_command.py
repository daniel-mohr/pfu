"""
Author: Daniel Mohr.
Date: 2017-02-14 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import platform
import re


def create_change_dir_command(param):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-08-03 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
    """
    change_dir = "cd "
    if platform.system() == "Windows":
        drive_letter = re.findall(r'([a-zA-Z]{1}):[\\\/]{1}', param)
        if len(drive_letter) == 1:
            change_dir = f"{drive_letter[0]}: && cd "
    return change_dir
