import boto.glacier
import boto
import shelve

class GlacierVault:
  """
  Wrapper for uploading/download archive to/from Amazon Glacier Vault
  Makes use of shelve to store archive id corresponding to filename and waiting jobs.
  """
  def __init__(self, vault_name, aws_access_key, aws_secret_key, shelve_file):
    """
    Initialize the vault
    """
    self.shelve_file = shelve_file
    layer2 = boto.connect_glacier(
      aws_access_key_id=aws_access_key,
      aws_secret_access_key=aws_secret_key
    )
    self.vault = layer2.get_vault(vault_name)

  def upload(self, filepath, description):
    """
    Upload filename and store the archive id for future retrieval
    """
    archive_id = self.vault.upload_archive(filepath, description=description)

    shelf = shelve.open(self.shelve_file)
    if not 'archives' in shelf:
      shelf['archives'] = dict()
    shelf['archives'][description] = archive_id
    shelf.close()

  def get_archive_id(self, description):
    """
    Get the archive_id corresponding to the filename
    """
    shelf = shelve.open(self.shelve_file, flag='r')
    if not 'archives' in shelf:
      return None
    if description in shelf['archives']:
       return shelf['archives'][description]
    return None

  def is_description_already_archived(self, description):
    """
    Determine if we've already archived a description
    """
    shelf = shelve.open(self.shelve_file, flag='r')
    if not 'archives' in shelf:
      return False
    if description in shelf['archives']:
     return True
    return False
