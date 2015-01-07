from GlacierVault import GlacierShelve, GlacierVault
import os


class BNIImageArchiver(object):
    def __init__(self, root_dir, relative_filepath, shelf_file, auth_id, auth_key, vault_name):
        self.root_dir = root_dir
        self.shelf_file = shelf_file
        self.auth_id = auth_id
        self.auth_key = auth_key
        self.vault_name = vault_name
        self.relative_filepath = relative_filepath
        self.archive_description = "".join([c for c in relative_filepath if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

    def archive_file(self):
        if not self.is_file_already_archived():
            vault = GlacierVault.GlacierVault(
                self.vault_name,
                self.auth_id,
                self.auth_key,
                self.shelf_file)
            vault.upload(os.path.join(self.root_dir, self.relative_filepath), self.archive_description)

    def is_file_already_archived(self):
        with GlacierShelve.GlacierShelve(self.shelf_file) as d:
            if not 'archives' in d:
                return False
            if self.archive_description in d['archives']:
                return True
        return False
