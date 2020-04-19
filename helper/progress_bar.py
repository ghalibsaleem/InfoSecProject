import sys

progress_flag = False


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    This function is created by a github User Aubrey Taylor with github id-"aubricus" and the link to the file is
    https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a

    Description-Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """

    if progress_flag:
        return
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()