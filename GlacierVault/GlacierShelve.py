import shelve


class GlacierShelve(object):
    """
    Context manager for shelve
    """
    def __init__(self, shelve_file):
        self.shelve_file = shelve_file

    def __enter__(self):
        self.shelve = shelve.open(self.shelve_file)
        return self.shelve

    def __exit__(self, exc_type, exc_value, traceback):
        self.shelve.close()
