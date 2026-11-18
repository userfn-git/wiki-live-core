"""
WikiLife Core - GCP Adapter
Handles defensive authentication and storage operations for Google Cloud Platform.
"""
import os
import sys
import logging
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [FN-WIKILIFE GCP] | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class GCPAdapter:
    def __init__(self, project_id=None):
        self.project_id = project_id
        self.client = None
        self._authenticate()

    def _authenticate(self):
        """Silently authenticates using GOOGLE_APPLICATION_CREDENTIALS or default profile."""
        try:
            self.client = storage.Client(project=self.project_id)
            logging.info(f"Authentication successful. Active Project: {self.client.project}")
        except DefaultCredentialsError:
            logging.warning("Credentials missing. Set GOOGLE_APPLICATION_CREDENTIALS env var.")
        except Exception as e:
            logging.error(f"Critical connection failure: {str(e)}")

    def is_connected(self):
        return self.client is not None

if __name__ == '__main__':
    print("=== Testing WikiLife GCP Adapter ===")
    adapter = GCPAdapter()
    if adapter.is_connected():
        print("[OK] GCP Adapter is ready for integration.")
    else:
        print("[WARN] GCP Adapter requires authentication setup.")