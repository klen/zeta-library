import os


LAST_MTIME = 0


def files_changed(path, prefix):
    """Return True if the files have changed since the last check"""
    def file_times(path):
        """Return the last time files have been modified"""
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [x for x in dirs if x[0] != '.']
                for f in files:
                    if not f.startswith(prefix):
                        yield os.stat(os.path.join(root, f)).st_mtime
        else:
            yield os.stat(path).st_mtime

    global LAST_MTIME
    mtime = max(file_times(path))
    if mtime > LAST_MTIME:
        LAST_MTIME = mtime
        return True
    return False
