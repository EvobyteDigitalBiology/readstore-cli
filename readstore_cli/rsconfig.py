# readstore-cli/readstore_cli/rsconfig.py

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
Provides methods for reading and writing configuration files.

Functions:
    - load_rs_config: Load configuration from file or ENV variables
    - write_rs_config: Write configuration to file

"""

import os
import configparser
from typing import List, Tuple

try:
    from readstore_cli import rsexceptions
except ModuleNotFoundError:
    import rsexceptions


def load_rs_config(
    filename: str | None = None,
    default_endpoint_url: str | None = None,
    default_fastq_extensions: List[str] | None = None,
    default_output: str | None = None,
) -> Tuple[str, str, str, List[str], str]:
    """Load configuration

    Load configuration from config file or ENV variables and return as tuple.
    If default API endpoint, fastq extensions or output format is provided,
    it will be used if not found in config.

    ENV variables precede over config file.

    Args:
        filename: config file to load
        default_endpoint_url:
            Default API endpoint to select if no config was found. Default None.
        default_fastq_extensions:
            Default API fastq extensions if no config was found. Default None.
        default_output:
            Default output fastq extensions if no config was found. Default None.

    Raises:
        rsexceptions.ReadStoreError: If no username was found
        rsexceptions.ReadStoreError: If no token was found
        rsexceptions.ReadStoreError: If no endpoint URL was found
        rsexceptions.ReadStoreError: If no fastq extensions were found
        rsexceptions.ReadStoreError: If no output format was found

    Returns:
        Tuple[str, str, str, List[str], str]:
        Tuple of username, token, endpoint URL, fastq extensions and output format
    """

    # If filename is provided, check if file exists
    # Then load configuration
    # If not provided, check if ENV variable are set and override config

    if filename and os.path.isfile(filename):

        rs_config = configparser.ConfigParser()
        rs_config.read(filename)

        username = rs_config.get("credentials", "username", fallback=None)
        token = rs_config.get("credentials", "token", fallback=None)
        endpoint_url = rs_config.get("general", "endpoint_url", fallback=None)
        fastq_extensions = rs_config.get("general", "fastq_extensions", fallback=None)
        output = rs_config.get("general", "output", fallback=None)
    # If file is not found, init empty variables
    else:
        username = None
        token = None
        endpoint_url = None
        fastq_extensions = None
        output = None

    # Check if ENV variables are set
    # Overwrite config if found
    if "READSTORE_USERNAME" in os.environ:
        username = os.environ["READSTORE_USERNAME"]
    if "READSTORE_TOKEN" in os.environ:
        token = os.environ["READSTORE_TOKEN"]
    if "READSTORE_ENDPOINT_URL" in os.environ:
        endpoint_url = os.environ["READSTORE_ENDPOINT_URL"]
    if "READSTORE_FASTQ_EXTENSIONS" in os.environ:
        fastq_extensions = os.environ["READSTORE_FASTQ_EXTENSIONS"]
        fastq_extensions = fastq_extensions.split(",")
    if "READSTORE_DEFAULT_OUTPUT" in os.environ:
        output = os.environ["READSTORE_DEFAULT_OUTPUT"]

    # If config parameters are not found in file or ENV,
    # try to use defaukt arguments if provided.
    if not username:
        raise rsexceptions.ReadStoreError("Username Not Found")
    if not token:
        raise rsexceptions.ReadStoreError("Token Not Found")
    if not endpoint_url:
        # Check if default is provided
        if default_endpoint_url:
            endpoint_url = default_endpoint_url
        else:
            raise rsexceptions.ReadStoreError("Config: Endpoint URL Not Found")
    if not fastq_extensions:
        if default_fastq_extensions:
            fastq_extensions = default_fastq_extensions
        else:
            raise rsexceptions.ReadStoreError("Config: Fastq Extensions Not Found")
    if not output:
        if default_output:
            output = default_output
        else:
            raise rsexceptions.ReadStoreError("Config: Output Format Not Found")

    return (username, token, endpoint_url, fastq_extensions, output)


def write_rs_config(
    filename: str,
    username: str,
    token: str,
    endpoint_url: str,
    fastq_extensions: List[str],
    output: str,
):
    """Write configuration file

    Write configuration file containing
    username, token, endpoint URL, fastq extensions and output format.

    Args:
        filename: Path to write configuration file
        username: Username
        token: Token
        endpoint_url: URL of the ReadStore API
        fastq_extensions (List[str]): List of fastq extensions
        output: Default output format
    """

    assert os.path.isdir(os.path.dirname(filename)), "Directory Not Found"

    # TODO Validate Server URL

    config = configparser.ConfigParser()

    config["general"] = {
        "endpoint_url": endpoint_url,
        "fastq_extensions": fastq_extensions,
        "output": output,
    }

    config["credentials"] = {"username": username, "token": token}

    with open(filename, "w") as f:
        config.write(f)
        os.chmod(filename, 0o600)
