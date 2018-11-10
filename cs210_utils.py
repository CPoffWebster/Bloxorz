##############################################################################
#
# File:         cs210_utils.py
# Date:         Wed 31 Aug 2011  12:03
# Author:       Ken Basye (from Onyx code by Hugh Secker-Walker)
# Description:  Some basic utilities for testing
#
##############################################################################

"""



"""

from __future__ import division
import sys, os

def cs210_mainstartup():
    """
    Boilerplate function that should be called explicitly by almost every module
    when run as standalone script.  It does the doctest work on a module and
    reports summary statistics.  It is called from the ``if __name__ ==
    '__main__':`` clause at the bottom of most modules.  It is intended that
    this function be called by modules that are also scripts, typically prior to
    argument parsing and the actual work of the script.

    If there are no command-line arguments, this function logs the result
    message, and if there were failures it calls sys.exit() with the number of
    failures.

    If there are command-line arguments and there were no failures then nothing
    gets logged -- this silence supports the module's use as a script.  If there
    are command-line arguments and there were failures, then the result message
    is logged to both stdout and stderr, but sys.exit() is not called.

    Note: this doctest-calling function is difficult to test explicitly via the
    doctest facility, particularly its failure modes.  So there's no doctest in
    this documentation string.
    """
    import sys
    num_ok, num_bad, msg = doctestmod()
    if len(sys.argv) <= 1:
        sys.stdout.write(msg)
        sys.stdout.flush()
        if num_bad != 0:
            sys.exit(num_bad)
    if num_bad != 0:
        # note: we write to both stdout and stderr
        sys.stdout.write(msg)
        sys.stdout.flush()
        sys.stderr.write(msg)


def make_doctest_message(fullfile, num_bad, num_test, elapsed_time_sec):
    """
    Create a well-defined error message for summarizing doctests.

    """
    DOCTESTMODTAG = 'doctestmod'
    _, file = os.path.split(fullfile)
    passfail = "pass" if num_bad == 0 else ("*** fail *** : file %r" % (fullfile,))
    num_ok = num_test - num_bad
    elapsed_time_usec_str, elapsed_time_sec_str = time_usec_sec_str(elapsed_time_sec)
    msg = "%s : %s : total %r  ok %r  bad %r : %s : elapsed time %s usec (%s seconds) \n" % (DOCTESTMODTAG, file, num_test, num_ok, num_bad, passfail, elapsed_time_usec_str, elapsed_time_sec_str)
    return msg


def doctestmod(module=None):
    """
    A doctest wrapper that runs doctest.testmod() on the module.  It
    returns a tuple: (num_ok, num_bad, string with a summary of the
    testing results).  The one-line string is prefixed with the value
    of DOCTESTMODTAG and terminated with a newline.

    Optional 'module' argument is the module to test.  If not given,
    or None, the module called '__main__' will be used.

    This function is particularly difficult to test other than
    functionally in the working system.
    """
    if module is None:
        module = sys.modules.get('__main__')

    import doctest
    import time
    start = time.time()
    num_bad, num_test = doctest.testmod(module, report=False, verbose=False)
    elapsed_time = time.time() - start
    msg = make_doctest_message(module.__file__, num_bad, num_test, elapsed_time)
    return num_test - num_bad, num_bad, msg


def time_usec_sec_str(duration_sec):
    """
    Format a duration (given as a number in seconds) into strings.  Return a
    pair of strings where the first string gives the duration in microseconds
    and the second string gives the duration as decimal seconds with exactly six
    digits following the decimal point.  Implementation avoids floating-point
    formatting issues by only using integer arithmetic.

    >>> duration = 2478 / 1000000  # 2478 microseconds
    >>> time_usec_sec_str(duration)
    ('2478', '0.002478')
    >>> duration = 2478002478 / 100000  # 24780.02478 microseconds
    >>> time_usec_sec_str(duration)
    ('24780024780', '24780.024780')

    """

    # format time without using floating point formatting such as %g
    USEC_PER_SEC = 1000000
    duration_usec = int(duration_sec * USEC_PER_SEC + 0.5)
    duration_usec_str = '%d' % (duration_usec,)
    duration_digits = list('%07d' % (duration_usec,))
    duration_digits.insert(-6, '.')
    duration_sec_str = ''.join(duration_digits)
    return duration_usec_str, duration_sec_str


if __name__ == '__main__':
    cs210_mainstartup()
