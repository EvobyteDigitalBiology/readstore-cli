# readstore-cli/readstore_cli/rsclient.py

# Copyright 2024 EVOBYTE Digital Biology Dr. Jonathan Alles
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Provides client for interacting with ReadStore API.

Classes:
    - RSClient: Provides client for interacting with ReadStore API.

"""

import requests
from urllib.parse import urlparse
import os
import base64
from typing import List, Dict

try:
    from readstore_cli import rsexceptions
except ModuleNotFoundError:
    import rsexceptions


class RSClient:
    """
        A client for interacting with the ReadStore API

        Attributes:
            username: ReadStore username
            token: ReadStore user token
            endpoint: The endpoint URL for the ReadStore API
            output_format: The default output format for the client

        Methods:
            get_output_format: Get Output Format set for client
            upload_fastq: Upload Fastq Files
            get_fq_file: Get Fastq File
            get_fq_file_upload_path: Get FASTQ file upload  path
            list_fastq_datasets: List FASTQ Datasets
            get_fastq_dataset: Get FASTQ dataset
            list_projects: List Projects
            get_project: Get Project by id or name
            download_project_attachment: Download Project Attachments
            download_fq_dataset_attachment: Download Fastq Attach
    """
    
    REST_API_VERSION = "api_v1/"
    USER_AUTH_TOKEN_ENDPOINT = "user/auth_token/"
    FASTQ_UPLOAD_ENDPOINT = "fq_file_upload/"
    FQ_DATASET_ENDPOINT = "fq_dataset/token/"
    FQ_FILE_ENDPOINT = "fq_file/token/"
    FQ_ATTACHMENT_ENDPOINT = "fq_attachment/token/"
    PROJECT_ENDPOINT = "project/token/"
    PROJECT_ATTACHMENT_ENDPOINT = "project_attachment/token/"
    UPLOAD_CHUNK_SIZE_MB = 100

    def __init__(
        self, username: str, token: str, endpoint_url: str, output_format: str
    ):
        """Constructor
        
        Initialize a new RSClient object
        
        Args:
            username: ReadStore username
            token: ReadStore user token
            endpoint_url: The endpoint URL for the ReadStore API
            output_format: The default output format for the client

        Raises:
            rsexceptions.ReadStoreError:
                Server Connection to API Failed
            rsexceptions.ReadStoreError:
                User Authentication Failed
        """

        self.username = username
        self.token = token
        self.endpoint = f"{endpoint_url}/{self.REST_API_VERSION}"
        self.output_format = output_format

        if not self._test_server_connection():
            raise rsexceptions.ReadStoreError(
                f"Server Connection Failed\nEndpoint URL: {self.endpoint}"
            )

        if not self._auth_user_token():
            raise rsexceptions.ReadStoreError(
                f"User Authentication Failed\nUsername: {self.username}"
            )

    def _test_server_connection(self) -> bool:
        """
        Validate server URL

        Returns:
            True if server can be reached else False
        """

        parsed_url = urlparse(self.endpoint)

        if parsed_url.scheme not in ["http", "https"]:
            return False
        else:
            try:
                response = requests.head(self.endpoint)

                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.exceptions.ConnectionError:
                return False

    def _auth_user_token(self) -> bool:
        """
        Validate user and token

        Returns:
            True if user token is valid else False
        """

        try:
            auth_endpoint = os.path.join(self.endpoint, self.USER_AUTH_TOKEN_ENDPOINT)

            payload = {"username": self.username, "token": self.token}

            res = requests.post(auth_endpoint, json=payload)

            if res.status_code != 200:
                return False
            else:
                return True

        except requests.exceptions.ConnectionError:
            return False

    def get_output_format(self) -> str:
        """
        Get Output Format set for client

        Return:
            str output format
        """

        return self.output_format

    def upload_fastq(self, fastq_files: List[str] | str):
        """Upload Fastq Files
        
        Upload Fastq files to ReadStore.
        Check if file exists and has read permissions.
        
        Args:
            fastq_files: List of Fastq files to upload
            
        Raises:
            rsexceptions.ReadStoreError: If file not found
            rsexceptions.ReadStoreError: If no read permissions
            rsexceptions.ReadStoreError: If upload URL request failed
        """

        if isinstance(fastq_files, str):
            fastq_files = [fastq_files]

        fq_upload_endpoint = os.path.join(self.endpoint, self.FASTQ_UPLOAD_ENDPOINT)

        # Run parallel uploads of fastq files
        for fq_file in fastq_files:

            fq_file = os.path.abspath(fq_file)

            # Make sure file exists and
            if not os.path.exists(fq_file):
                raise rsexceptions.ReadStoreError(f"File Not Found: {fq_file}")
            elif not os.access(fq_file, os.R_OK):
                raise rsexceptions.ReadStoreError(f"No read permissions: {fq_file}")

            payload = {
                "username": self.username,
                "token": self.token,
                "fq_file_path": fq_file,
            }

            res = requests.post(fq_upload_endpoint, json=payload)

            if res.status_code not in [200, 204]:
                res_message = res.json().get("message", "No Message")
                raise rsexceptions.ReadStoreError(
                    f"Upload URL Request Failed: {res_message}"
                )

    def get_fq_file(self, fq_file_id: int) -> Dict:
        """Get Fastq File

        Return Fastq file data by fq_file ID
        
        Args:
            fq_file_id: ID (pk) of fq_file

        Returns:
            dict with fq file data
        """

        fq_file_endpoint = os.path.join(self.endpoint, self.FQ_FILE_ENDPOINT)

        # Define json for post request
        json = {
            "username": self.username,
            "token": self.token,
            "fq_file_id": fq_file_id,
        }

        res = requests.post(fq_file_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("get_fq_file Failed")
        else:
            return res.json()[0]

    def get_fq_file_upload_path(self, fq_file_id: int) -> str:
        """Get FASTQ file upload path

        Get upload path for FASTQ file by fq_file ID

        Args:
            fq_file_id: ID (pk) of FASTQ file

        Raises:
            rsexceptions.ReadStoreError: If upload_path is not found

        Returns:
            str: Upload path
        """

        fq_file = self.get_fq_file(fq_file_id)

        if "upload_path" not in fq_file:
            raise rsexceptions.ReadStoreError("upload_path Not Found in FqFile entry")

        upload_path = fq_file.get("upload_path")

        return upload_path

    def list_fastq_datasets(
        self,
        project_name: str | None = None,
        project_id: int | None = None,
        role: str | None = None,
    ) -> List[dict]:
        """
        List FASTQ Datasets

        List FASTQ datasets and filter by project_name, project_id or role.
        Role can be owner, collaborator or creator.

        Args:
            project_name: Filter fq_datasets by project name
            project_id: Filter fq_datasets by project ID
            role: Filter fq_datasets by owner role (owner, collaborator, creator)

        Raises:
            rsexceptions.ReadStoreError if role is not valid
            rsexceptions.ReadStoreError request failed

        Returns:
            List[Dict]: FASTQ datasets in JSON format
        """

        fq_dataset_endpoint = os.path.join(self.endpoint, self.FQ_DATASET_ENDPOINT)

        # Define json for post request
        json = {
            "username": self.username,
            "token": self.token,
        }

        if role:
            if role.lower() in ["owner", "collaborator", "creator"]:
                json["role"] = role
            else:
                raise rsexceptions.ReadStoreError("Invalid Role")

        if project_name:
            json["project_name"] = project_name
        if project_id:
            json["project_id"] = project_id

        res = requests.post(fq_dataset_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("list_fastq_datasets Failed")
        else:
            return res.json()

    def get_fastq_dataset(
        self,
        dataset_id: int | None = None,
        dataset_name: str | None = None
    ) -> Dict:
        """Get FASTQ dataset

        Get FASTQ dataset by provided dataset_id or dataset_name
        If dataset_name is not unique an error is printed

        Args:
            dataset_id: fq_dataset ID (or pk) to select
            dataset_name: fq_dataset Name to select

        Raises:
            rsexceptions.ReadStoreError: If backend request failed
            rsexceptions.ReadStoreError:
                If multiple datasets found with same name.
                This can occur if datasets with identical name were shared with you.

        Returns:
            Dict: Json Detail response
        """

        fq_dataset_endpoint = os.path.join(self.endpoint, self.FQ_DATASET_ENDPOINT)

        # Define json for post request
        json = {"username": self.username, "token": self.token}
        if dataset_id:
            json["dataset_id"] = dataset_id
        if dataset_name:
            json["dataset_name"] = dataset_name

        res = requests.post(fq_dataset_endpoint, json=json)

        # Remove entries not requested
        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("get_fastq_dataset Failed")
        else:
            # If no dataset found, return empty dict
            if len(res.json()) == 0:
                return {}
            # If several datasets found, return error
            elif len(res.json()) > 1:
                raise rsexceptions.ReadStoreError(
                    """Multiple Datasets Found.\n
                    This can happen if datasets with identical name were
                    shared with you.\nUse dataset_id to get the correct dataset."""
                )
            else:
                return res.json()[0]

    def list_projects(self, role: str | None = None) -> List[Dict]:
        """List Projects

        List projects and optionally filter by role

        Args:
            role: Owner role to filter (owner, collaborator, creator)

        Raises:
            rsexceptions.ReadStoreError: If role is not valid
            rsexceptions.ReadStoreError: If request failed

        Returns:
            List[Dict]: List of projects
        """

        project_endpoint = os.path.join(self.endpoint, self.PROJECT_ENDPOINT)

        # Define json for post request
        json = {"username": self.username, "token": self.token}

        if role:
            if role.lower() in ["owner", "collaborator", "creator"]:
                json["role"] = role
            else:
                raise rsexceptions.ReadStoreError("Invalid Role")

        res = requests.post(project_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("list_projects Failed")
        else:
            return res.json()

    def get_project(
        self,
        project_id: int | None = None,
        project_name: str | None = None
    ) -> Dict:
        """Get Individual Project
        
        Return project details by project_id or project_name
        If name is duplicated, print error message

        Args:
            project_id: Project ID
            project_name: Project Name

        Raise
            rsexceptions.ReadStoreError: If request failed
            rsexceptions.ReadStoreError: If duplicate names are found

        Returns:
            project detail response
        """

        assert project_id or project_name, "project_id or project_name Required"

        project_endpoint = os.path.join(self.endpoint, self.PROJECT_ENDPOINT)

        # Define json for post request
        json = {"username": self.username, "token": self.token}

        if project_id:
            json["project_id"] = project_id
        if project_name:
            json["project_name"] = project_name

        res = requests.post(project_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("get_project Failed")
        else:
            if len(res.json()) == 0:
                return {}
            # If several datasets found, return error
            elif len(res.json()) > 1:
                raise rsexceptions.ReadStoreError(
                    """Multiple Projects Found.\n
                This can happen if Projects with identical name were shared with you.\n
                Use unique Project ID to access the correct dataset."""
                )
            else:
                return res.json()[0]

    def download_project_attachment(
        self,
        attachment_name: str,
        outpath: str,
        project_id: int | None = None,
        project_name: str | None = None,
    ):
        """Download Project Attachments

        Download Project Attachment Files to local path

        Args:
            attachment_name: Attachment name
            outpath: Path to write to
            project_id: Id of project
            project_name: Project name.

        Raises:
            rsexceptions.ReadStoreError: Request failed
            rsexceptions.ReadStoreError: Attachment not Found
            rsexceptions.ReadStoreError: Multiple Attachments Found for Project.
        """

        project_attachment_endpoint = os.path.join(
            self.endpoint, self.PROJECT_ATTACHMENT_ENDPOINT
        )

        assert project_id or project_name, \
            "Either project_id or project_name required"

        # Define json for post request
        json = {
            "username": self.username,
            "token": self.token,
            "attachment_name": attachment_name,
        }

        if project_id:
            json["project_id"] = project_id
        if project_name:
            json["project_name"] = project_name

        res = requests.post(project_attachment_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("download_project_attachment failed")
        elif len(res.json()) == 0:
            raise rsexceptions.ReadStoreError("Attachment Not Found")
        elif len(res.json()) > 1:
            raise rsexceptions.ReadStoreError(
                """Multiple Attachments Found For Project.
                This can happen if Projects with identical name were shared with you.\n
                Use unique Project ID to access the correct attachment."""
            )
        else:
            attachment = res.json()[0]
            with open(outpath, "wb") as fh:
                fh.write(base64.b64decode(attachment["body"]))

    def download_fq_dataset_attachment(
        self,
        attachment_name: str,
        outpath: str,
        dataset_id: int | None = None,
        dataset_name: str | None = None,
    ):
        """Fastq Attachments

        Download Fastq Attachments

        Args:
            attachment_name: Attachment name
            outpath: Path to write to
            dataset_id: Id of project
            dataset_name: Project name.

        Raises:
            rsexceptions.ReadStoreError: Request failed
            rsexceptions.ReadStoreError: Attachment not Found
            rsexceptions.ReadStoreError: Multiple Attachments Found for Project.
        """

        fq_dataset_endpoint = os.path.join(self.endpoint, self.FQ_ATTACHMENT_ENDPOINT)

        assert dataset_id or dataset_name, "dataset_id or dataset_name required"

        # Define json for post request
        json = {
            "username": self.username,
            "token": self.token,
            "attachment_name": attachment_name,
        }

        if dataset_id:
            json["dataset_id"] = dataset_id
        if dataset_name:
            json["dataset_name"] = dataset_name

        res = requests.post(fq_dataset_endpoint, json=json)

        if res.status_code not in [200, 204]:
            raise rsexceptions.ReadStoreError("download_fq_dataset_attachment failed")
        elif len(res.json()) == 0:
            raise rsexceptions.ReadStoreError("Attachment Not Found")
        elif len(res.json()) > 1:
            raise rsexceptions.ReadStoreError(
                """Multiple Attachments Found For Dataset.
                This can happen if Datasets with identical name were shared with you.\n
                Use unique Dataset ID to access the correct attachment."""
            )
        else:
            attachment = res.json()[0]
            with open(outpath, "wb") as fh:
                fh.write(base64.b64decode(attachment["body"]))
