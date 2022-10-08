# -*- coding: utf-8 -*-
#

def check_code(user, code):
    """ Customize the MFA method

    :param user: Login user object
    :param code: MFA custom code

    :returns: True or False
    """
    if code == '666':
        return True
    else:
        return False
