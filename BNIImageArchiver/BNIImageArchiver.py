from GlacierVault import GlacierVault
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
        print self.archive_description

    def archive_file(self):
      vault = GlacierVault.GlacierVault(
                self.vault_name,
                self.auth_id,
                self.auth_key,
                self.shelf_file)
       
       if not vault.is_file_already_archived(self.archive_description):
            vault.upload(os.path.join(self.root_dir, self.relative_filepath), self.archive_description)
            print "File archived"
       else:
            print "File already archived!"
