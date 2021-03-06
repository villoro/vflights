"""
    Utilities for pandas dataframes
"""

from v_crypt import Cipher

import constants as c

CIPHER = Cipher(secrets_file=c.FILE_SECRETS, environ_var_name=c.SECRET_ENV_VAR_NAME)


def get_secret(key):
    """ Retrives one encrypted secret """
    return CIPHER.get_secret(key)
