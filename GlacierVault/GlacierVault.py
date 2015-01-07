import boto.glacier
import boto
from boto.glacier.exceptions import UnexpectedHTTPResponseError
from GlacierVault import GlacierShelve

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
        archive_id = self.vault.create_archive_from_file(filepath, description=description)

        with GlacierShelve(self.shelve_file) as d:
            if not d.has_key('archives'):
                d['archives'] = dict()
            d['archives'][description] = archive_id

    def get_archive_id(self, description):
        """
        Get the archive_id corresponding to the filename
        """
        with GlacierShelve(self.shelve_file) as d:
            if not d.has_key('archives'):
                d['archives'] = dict()

            archives = d['archives']

            if description in archives:
                return archives[description]

        return None

    def retrieve(self, description, file_output_path, wait_mode=False):
        """
        Initiate a Job, check its status, and download the archive when it's completed.
        """
        job_id = None
        archive_id = self.get_archive_id(description)
        if not archive_id:
            return

        with GlacierShelve(self.shelve_file) as d:
            if not d.has_key('jobs'):
                d['jobs'] = dict()

            jobs = d['jobs']
            job = None

            if description in jobs:
                # The job is already in shelve
                job_id = jobs[description]
                try:
                    job = self.vault.get_job(job_id)
                except UnexpectedHTTPResponseError: # Return a 404 if the job is no more available
                    pass

            if not job:
                # Job initialization
                job = self.vault.retrieve_archive(archive_id)
                jobs[description] = job.id
                job_id = job.id

            # Committing changes in shelve
            d['jobs'] = jobs

        print "Job {action}: {status_code} ({creation_date}/{completion_date})".format(**job.__dict__)

        # checking manually if job is completed every 10 secondes instead of using Amazon SNS
        if wait_mode:
            import time
            while 1:
                job = self.vault.get_job(job_id)
                if not job.completed:
                    time.sleep(10)
                else:
                    break

        if job.completed:
            print "Downloading..."
            job.download_to_file(file_output_path)
        else:
            print "Not completed yet"
