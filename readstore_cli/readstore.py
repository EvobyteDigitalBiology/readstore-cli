#!/usr/bin/env python3


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
Provides readstore command line interface

Functions:
    - configure_list: List configuration settings
    - configure: Configure ReadStore CLI
    - upload: Upload FASTQ Files
    - list_fq_datasets: List FASTQ Datasets
    - list_projects: List Projects
    - get_fastq_dataset: Get FASTQ Dataset
    - get_project: Get Project
    - download_fq_dataset_attachment: Download FASTQ Dataset Attachment
    - download_project_attachment: Download Project Attachment
    - main: Main function for ReadStore CLI

"""

import argparse
from pathlib import Path
import os
from typing import List
import sys

# Check case if readstore is installed as package or run from source
try:
    from readstore_cli.__version__ import __version__
    from readstore_cli import rsconfig
    from readstore_cli import rsexceptions
    from readstore_cli import rsclient
    
except ModuleNotFoundError:
    from __version__ import __version__
    import rsconfig
    import rsexceptions
    import rsclient
    
# GLOBALS
DEFAULT_ENDPOINT_URL = 'http://localhost:8000'
DEFAULT_FASTQ_EXTENSIONS = '.fastq,.fastq.gz,.fq,.fq.gz'.split(',')
DEFAULT_OUTPUT = 'text'
OUTPUT_FORMATS = ['json', 'text', 'csv']

HOME = str(Path.home())
READSTORE_CONFIG_FILE = os.path.join(HOME, '.readstore', 'config')

# region PARSERS

# Base Parser
parser = argparse.ArgumentParser(
    prog='readstore',
    usage='%(prog)s <command> [options]',
    description="ReadStore Command Line Interface",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')

parser.add_argument('-v',
                    '--version', action='store_true', help='Show ReadStore CLI Version')

subparsers = parser.add_subparsers(title="Commands")

# Configure Parser
config_parser = subparsers.add_parser("configure",
                                      help='Set Credentials and Configuration',
                                      add_help=True)

config_subparser_list = config_parser.add_subparsers()

config_parser_list = config_subparser_list.add_parser(
    "ls",
    aliases=['list'],
    prog='readstore configure ls',
    usage='%(prog)s [options]',
    description="List Credentials and Configuration",
    help='List Credentials and Configuration')


# List FASTQ Datasets Parser
list_fq_parser = subparsers.add_parser(
    "ls",
    aliases=['list'],
    help='List FASTQ Datasets',
    prog='readstore ls',
    usage='%(prog)s [options]',
    description="List FASTQ Datasets",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')

list_fq_parser.add_argument('-p',
                            '--project-name',
                            type=str,
                            help='Subset by Project Name',
                            metavar='')
list_fq_parser.add_argument('-pid',
                            '--project-id',
                            type=int,
                            help='Subset by Project ID',
                            metavar='')
list_fq_parser.add_argument('-m',
                            '--meta',
                            action='store_true',
                            help='Get Metadata')
list_fq_parser.add_argument('-a',
                            '--attachment',
                            action='store_true',
                            help='Get Attachment')
list_fq_parser.add_argument('--output',
                            type=str,
                            help='Format of command output (see config for default)',
                            choices=OUTPUT_FORMATS)

# Get FASTQ Datasets Parser
get_fq_parser = subparsers.add_parser(
    "get",
    help='Get FASTQ Datasets',
    prog='readstore get',
    usage='%(prog)s [options]',
    description="Get FASTQ Datasets and Files",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')

get_fq_parser.add_argument('-id',
                           '--id',
                           type=int,
                           help='Get Dataset by ID',
                           metavar='')
get_fq_parser.add_argument('-n',
                           '--name',
                           type=str,
                           help='Get Dataset by name',
                           metavar='')
get_fq_parser.add_argument('-m',
                           '--meta',
                           action='store_true',
                           help='Get only Metadata')
get_fq_parser.add_argument('-a',
                           '--attachment',
                           action='store_true',
                           help='Get only Attachments')

get_fq_parser.add_argument('-r1',
                           '--read1',
                           action='store_true',
                           help='Get Read 1 Data')
get_fq_parser.add_argument('-r2',
                           '--read2',
                           action='store_true',
                           help='Get Read 2 Data')
get_fq_parser.add_argument('-r1p',
                           '--read1-path',
                           action='store_true',
                           help='Get Read 1 FASTQ Path')
get_fq_parser.add_argument('-r2p',
                           '--read2-path',
                           action='store_true',
                           help='Get Read 2 FASTQ Path')

# Index Reads, could be removed
get_fq_parser.add_argument('-i1',
                           '--index1',
                           action='store_true',
                           help='Get Index 1 Data')
get_fq_parser.add_argument('-i2',
                           '--index2',
                           action='store_true',
                           help='Get Index 2 Data')

get_fq_parser.add_argument('-i1p',
                           '--index1-path',
                           action='store_true',
                           help='Get Index 1 FASTQ Path')
get_fq_parser.add_argument('-i2p',
                           '--index2-path',
                           action='store_true',
                           help='Get Index 2 FASTQ Path')
# Access attachments
get_fq_parser.add_argument('--output',
                           type=str,
                           help='Format of command output (see config for default)',
                           choices=['json', 'text', 'csv'])

# Project Parser

project_parser = subparsers.add_parser("project",
                                       help='Access Projects')

project_subparser = project_parser.add_subparsers()
list_project_parser = project_subparser.add_parser(
    "ls",
    aliases=['list'],
    help='List Projects',
    prog='readstore project ls',
    usage='%(prog)s [options]',
    description="List Projects",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')

list_project_parser.add_argument('-m',
                                 '--meta',
                                 action='store_true',
                                 help='Get Metadata')
list_project_parser.add_argument('-a',
                                 '--attachment',
                                 action='store_true',
                                 help='Get Attachment')
list_project_parser.add_argument('--output',
                                 type=str,
                                 help='Format of command output (see config for default)',
                                 choices=['json', 'text', 'csv'])

get_project_parser = project_subparser.add_parser(
    "get",
    help='Get Project',
    prog='readstore project get',
    usage='%(prog)s [options]',
    description="Get Project",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')

get_project_parser.add_argument('-id',
                                '--id',
                                type=int,
                                help='Get Project by ID',
                                metavar='')
get_project_parser.add_argument('-n',
                                '--name',
                                type=str,
                                help='Get Project by name',
                                metavar='')
get_project_parser.add_argument('-m',
                                '--meta',
                                action='store_true',
                                help='Get only Metadata')
get_project_parser.add_argument('-a',
                                '--attachment',
                                action='store_true',
                                help='Get only Attachment')
get_project_parser.add_argument('--output',
                                type=str,
                                help='Format of command output (see config for default)',
                                choices=['json', 'text', 'csv'])

download_project_parser = project_subparser.add_parser(
    "download",
    help='Download Project Attachments',
    prog='readstore project download',
    usage='%(prog)s [options]',
    description="Download Project Attachments",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')
                                                         
download_project_parser.add_argument('-id',
                                     '--id',
                                     type=int,
                                     help='Select Project by ID',
                                     metavar='')
download_project_parser.add_argument('-n',
                                     '--name',
                                     type=str,
                                     help='Select Project by name',
                                     metavar='')
download_project_parser.add_argument('-a',
                                     '--attachment',
                                     type=str,
                                     help='Set Attachment Name to download',
                                     metavar='',
                                     required=True)
download_project_parser.add_argument('-o',
                                     '--outpath',
                                     type=str,
                                     help='Download path or directory (default . )',
                                     default='.',
                                     metavar='')

# Upload Parser
upload_parser = subparsers.add_parser("upload",
                                      help='Upload FASTQ Files')
upload_parser.add_argument('fastq_files',
                           type=str,
                           nargs='+',
                           help='FASTQ Files to Upload')

download_fq_parser = subparsers.add_parser(
    "download",
    help='Download Dataset attachments',
    prog='readstore download',
    usage='%(prog)s [options]',
    description="Download Dataset attachments",
    epilog='For help on a specific command, type "readstore <command> <subcommand> -h"')
                                                         
download_fq_parser.add_argument('-id',
                                '--id',
                                type=int,
                                help='Select Dataset by ID',
                                metavar='')
download_fq_parser.add_argument('-n',
                                '--name',
                                type=str,
                                help='Select Dataset by name',
                                metavar='')
download_fq_parser.add_argument('-a',
                                '--attachment',
                                type=str,
                                help='Set Attachment Name to download',
                                metavar='',
                                required=True)
download_fq_parser.add_argument('-o',
                                '--outpath',
                                type=str,
                                help='Download path or directory (default . )',
                                default='.',
                                metavar='')

# Help Parser
# Set Defaults in order to run the correct function based on subparser
config_parser.set_defaults(config_run=True)
config_parser_list.set_defaults(config_list=True)

upload_parser.set_defaults(upload_run=True)

# Set role argument none for basic version
list_fq_parser.set_defaults(list_fq_run=True, role=None)
get_fq_parser.set_defaults(get_fq_run=True)
download_fq_parser.set_defaults(download_run=True)

project_parser.set_defaults(project_run=True)
list_project_parser.set_defaults(list_project_run=True, role=None)
get_project_parser.set_defaults(get_project_run=True)
download_project_parser.set_defaults(download_project_run=True)


# TODO: option for custom config file path
def _get_readstore_client() -> rsclient.RSClient:
    """Get ReadStore RSClient

    Load readstore configuration and generate client
    Requires READSTORE_CONFIG_FILE global
    Requires DEFAULT_ENDPOINT_URL
    Requires DEFAULT_FASTQ_EXTENSIONS
    Requires DEFAULT_OUTPUT
    
    Raises:
        rsexceptions.ReadStoreError:
            If no config is found in config file or ENV variables

    Returns:
        rsclient.RSClient
    """
    
    if os.path.isfile(READSTORE_CONFIG_FILE):
        config_params = rsconfig.load_rs_config(filename=READSTORE_CONFIG_FILE)
    else:
        try:
            # Try to load default configuration and environment variables
            config_params = rsconfig.load_rs_config(
                default_endpoint_url=DEFAULT_ENDPOINT_URL,
                default_fastq_extensions=DEFAULT_FASTQ_EXTENSIONS,
                default_output=DEFAULT_OUTPUT)
            
        except rsexceptions.ReadStoreError as e:
            raise rsexceptions.ReadStoreError(
                e.message + '\n No Configuration File and No ENV Variables Found')
    
    username, token, endpoint_url, fastq_extensions, output = config_params
    
    client = rsclient.RSClient(username, token, endpoint_url, output)

    return client


def _validate_read_path(fq_file_path: str) -> bool:
    """Check fq_file path
    
    Check if fastq file exists and can be read
    
    Args:
        fq_file_path: File to check

    Returns:
        bool: True if path is valid else False
    """
    
    # Check if file exists
    if not os.path.isfile(fq_file_path):
        sys.stderr.write(
            f'ReadStore Warning: Upload Path of this FASTQ File could not be found: {fq_file_path}\n')
        return False
    # Check for read permission
    elif not os.access(fq_file_path, os.R_OK):
        sys.stderr.write(f'ReadStore Warning: No Read Permission: {fq_file_path}\n')
        return False
    else:
        return True


def configure_list():
    """List config settings
    
    List user and general client configuration
    Print in console
    
    

    Raises: rsexceptions.ReadStoreError
    """
    
    print('Listing ReadStore Configuration and Credentials')
    
    if os.path.isfile(READSTORE_CONFIG_FILE):
        try:
            config_params = rsconfig.load_rs_config(READSTORE_CONFIG_FILE)
            username, token, endpoint_url, fastq_extensions, output = config_params
            
            # For token make last 4 characters visible
            token_hidden = '*' * (len(token) - 4) + token[-4:]
            
            print(f'Configuration File Found at {READSTORE_CONFIG_FILE}')
            
            print("[USER]")
            print(f'Username: {username}')
            print(f'Token: {token_hidden}')
            
            print("[GENERAL]")
            print(f'Endpoint URL: {endpoint_url}')
            print(f"""FASTQ Extensions: {fastq_extensions}""")
            print(f"""Default Output: {output}""")
            
        except rsexceptions.ReadStoreError as e:
            # If config file is invalid, overwrite anyway
            sys.stderr.write(e.message + '\n') 
            sys.stderr.write("""Configuration Found, But Corrupted.\n
                             Reset Configuration with "readstore configure"\n""")
    else:
        sys.stderr.write("""No Configuration Found.\n
                        Set Configuration with "readstore configure"\n""")
    
    
def configure():
    """Configure CLI

    Write config file for ReadStore CLI
    
    Requires: READSTORE_CONFIG_FILE
    
    Write config file to READSTORE_CONFIG_FILE
        
    """
    
    print('Configuring ReadStore CLI')
    
    readstore_config_dir = os.path.dirname(READSTORE_CONFIG_FILE)
    
    os.makedirs(readstore_config_dir,
                exist_ok=True)

    username = input('ReadStore Username: ')
    token = input('ReadStore Token: ')
    output = input('Default Output Format (json, text, csv): ')
    
    if output not in OUTPUT_FORMATS:
        sys.stderr.write('ReadStore Error: Invalid Output Format.\n')
        return
    
    endpoint_url = DEFAULT_ENDPOINT_URL
    fastq_extensions = DEFAULT_FASTQ_EXTENSIONS
    write_config = True
    
    # Check if config exists, if so, ask to overwrite
    if os.path.isfile(READSTORE_CONFIG_FILE):
        
        try:
            config = rsconfig.load_rs_config(READSTORE_CONFIG_FILE)
            username_old, token_old, endpoint_url_old, fastq_extensions_old, output_format_old = config
            write_config = False
            print(f'Config file found at {READSTORE_CONFIG_FILE}')
            overwrite = input('Overwrite? (y/n): ')
            
            # If not overwrite, don't write config
            if overwrite.lower().strip() == 'y':
               
                endpoint_url = endpoint_url_old
                fastq_extensions = fastq_extensions_old
                rsconfig.write_rs_config(READSTORE_CONFIG_FILE,
                                         username,
                                         token,
                                         endpoint_url,
                                         fastq_extensions,
                                         output)
                print('Configuration File Updated')
            else:
                print('Abort Configuration')
                     
        except rsexceptions.ReadStoreError:
            # If config file is invalid, overwrite anyway
            sys.stderr.write("Error Setting Configuration\n")
    
    if write_config:
        
        rsconfig.write_rs_config(READSTORE_CONFIG_FILE,
                                 username,
                                 token,
                                 endpoint_url,
                                 fastq_extensions,
                                 output)
        print(f'Created New Configuration File at {READSTORE_CONFIG_FILE}')


def upload(fastq_files: List[str]):
    """Upload fastq files
    
    Upload provided files
    
    Check files by extension
    
    Args:
        fastq_files: Fastq files to upload
    """
    
    # Get ReadStore Client and Validate Connection    
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    for fq in fastq_files:
        
        print(f'ReadStore Upload: Start {fq}')
        
        if not os.path.isfile(fq):
            sys.stderr.write(f'\nReadStore Upload: File Not Found: {fq}\n')
            continue
        elif not fq.endswith(tuple(DEFAULT_FASTQ_EXTENSIONS)):
            sys.stderr.write(f'\nReadStore Upload: Invalid FASTQ Extension: {fq}\n')
        else:
            client.upload_fastq(fq)
    

def list_fq_datasets(project_name: str | None = None,
                     project_id: int | None = None,
                     role: str | None = None,
                     meta: bool = False,
                     attachment: bool = False,
                     output: str | None = None):
    """List Fastq Datasets

    List all Fastq Datasets and Filter by Project
    Options to show only meta and attachments
    
    Args:
        project_name: Filter by Project Name
        project_id: Filter by Project Id
        role: Filter by Owner Role
        meta: Show metadata
        attachment: Show attachments
        output: Set output format. If none use default from config file
    """
    
    # Get ReadStore Client and Validate Connection    
    try:
        client = _get_readstore_client()
                
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    if output is None:
        output = client.get_output_format()
    
    try:
        fq_datasets = client.list_fastq_datasets(
            project_name,
            project_id,
            role)
        
        for fq in fq_datasets:
            if not meta:
                fq.pop('metadata', None)
            if not attachment:
                fq.pop('attachments', None)
        
        if output == 'json':
            print(fq_datasets)
        elif output == 'text':
            if len(fq_datasets) > 0:
                header = list(fq_datasets[0].keys())
                header_str = ' | '.join(header)
                print(header_str)
                
                for fq in fq_datasets:
                    values = [str(fq[key]) for key in header]
                    values_str = ' | '.join(values)
                    print(values_str)
        elif output == 'csv':
            if len(fq_datasets) > 0:
                header = list(fq_datasets[0].keys())
                header_str = ','.join(header)
                print(header_str)
                
                for fq in fq_datasets:
                    values = [str(fq[key]) for key in header]
                    values_str = ','.join(values)
                    print(values_str)
        else:
            sys.stderr.write('Output Format Not Supported\n')
            return
        
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return


def list_projects(role: str | None = None,
                  meta: bool = False,
                  attachment: bool = False,
                  output: str | None = None):
    """List Projects

    List all Fastq Projects.
    Options to add metadata and attachments
    
    Role must be in owner, collaborator, creator
    
    Args:
        role: Filter by Owner Role
        meta: Show metadata
        attachment: Show attachments
        output: Set output format. If none use default from config file
    """
    
    # Get ReadStore Client and Validate Connection 
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return

    if output is None:
        output = client.get_output_format()
    try:
        projects = client.list_projects(role)
        
        for p in projects:
            if not meta:
                p.pop('metadata', None)
            if not attachment:
                p.pop('attachments', None)
        
        if output == 'json':
            print(projects)
        elif output == 'text':
            header = list(projects[0].keys())
            header_str = ' | '.join(header)
            print(header_str)
            
            for p in projects:
                values = [str(p[key]) for key in header]
                values_str = ' | '.join(values)
                print(values_str)
        elif output == 'csv':
            header = list(projects[0].keys())
            header_str = ','.join(header)
            print(header_str)
            
            for p in projects:
                values = [str(p[key]) for key in header]
                values_str = ','.join(values)
                print(values_str)
        else:
            sys.stderr.write('Output Format Not Supported\n')
            return
        
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return


def get_fastq_dataset(dataset_id: int | None = None,
                      dataset_name: str | None = None,
                      meta: bool = False,
                      attachment: bool = False,
                      read1: bool = False,
                      read2: bool = False,
                      index1: bool = False,
                      index2: bool = False,
                      read1_path: bool = False,
                      read2_path: bool = False,
                      index1_path: bool = False,
                      index2_path: bool = False,
                      output: str | None = None):
    """Get individual FASTQ dataset

    Use arguments to filter and return specific data
    such as individual reads, metadata or read paths
    
    Args:
        dataset_id: Filter by Dataset Id. Defaults to None.
        dataset_name: Filter by Dataset Name. Defaults to None.
        meta: Show only metadata.
        attachment: Show only attachments
        read1: Show Read 1 data.
        read2: Show Read 2 data.
        index1: Show Index 1 data
        index2: Show Index 2 data
        read1_path: Show Read 1 Path
        read2_path: Show Read 2 Path
        index1_path: Show Index 1 Path
        index2_path: Show Index 2 Path
        output: Set output format. If none use default from config file
    """
    
    if not dataset_id and not dataset_name:
        sys.stderr.write(
            'ReadStore Error: Must Provide Dataset ID (--id) or Name (--name)\n')
        sys.stderr.write(
            'ReadStore Error: Run readstore get -h for help\n')
        return
    
    # Get ReadStore Client and Validate Connection
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    if output is None:
        output = client.get_output_format()
    
    try:
        fq_dataset = client.get_fastq_dataset(dataset_id,
                                              dataset_name)
        
        path = False
        
        if meta:
            out_data = fq_dataset.pop('metadata', {})
        elif attachment:
            out_data = fq_dataset.pop('attachments', {})
            out_data = {'name': out_data}
        # Return individual read files
        elif read1:
            if fq_dataset['fq_file_r1']:
                out_data = client.get_fq_file(fq_dataset['fq_file_r1'])
            else:
                out_data = {}
        elif read2:
            if fq_dataset['fq_file_r2']:
                out_data = client.get_fq_file(fq_dataset['fq_file_r2'])
            else:
                out_data = {}
        elif index1:
            if fq_dataset['fq_file_i1']:
                out_data = client.get_fq_file(fq_dataset['fq_file_i1'])
            else:
                out_data = {}
        elif index2:
            if fq_dataset['fq_file_i2']:
                out_data = client.get_fq_file(fq_dataset['fq_file_i2'])
            else:
                out_data = {}
        elif read1_path:
            path = True
            if fq_dataset['fq_file_r1']:
                out_data = client.get_fq_file_upload_path(fq_dataset['fq_file_r1'])
                _ = _validate_read_path(out_data)
            else:
                out_data = ''
        elif read2_path:
            path = True
            if fq_dataset['fq_file_r2']:
                out_data = client.get_fq_file_upload_path(fq_dataset['fq_file_r2'])
                _ = _validate_read_path(out_data)
            else:
                out_data = ''
        elif index1_path:
            path = True
            if fq_dataset['fq_file_i1']:
                out_data = client.get_fq_file_upload_path(fq_dataset['fq_file_i1'])
                _ = _validate_read_path(out_data)
            else:
                out_data = ''
        elif index2_path:
            path = True
            if fq_dataset['fq_file_i2']:
                out_data = client.get_fq_file_upload_path(fq_dataset['fq_file_i2'])
                _ = _validate_read_path(out_data)
            else:
                out_data = ''
        # Return individual read files
        else:
            # Reformat so that all data is in one dict
            out_data = fq_dataset
        
        if output == 'json':
            print(out_data)
        elif output == 'text':
            if path:
                print(out_data)
            else:
                header = list(out_data.keys())
                header_str = ' | '.join(header)
                print(header_str)
                
                if attachment:
                    values_str = '\n'.join(out_data['name'])
                else:
                    values = [str(out_data[key]) for key in header]
                    values_str = ' | '.join(values)
                print(values_str)
        elif output == 'csv':
            if path:
                print(out_data)
            else:
                header = list(out_data.keys())
                header_str = ','.join(header)
                print(header_str)
                
                if attachment:
                    values_str = '\n'.join(out_data['name'])
                else:
                    values = [str(out_data[key]) for key in header]
                    values_str = ','.join(values)
                print(values_str)
        else:
            sys.stderr.write('Output Format Not Supported\n')
            return
          
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return


def get_project(project_id: int | None = None,
                project_name: str | None = None,
                meta: bool = False,
                attachment: bool = False,
                output: str | None = None):
    """Get individual Project

    Must define project id or name
    Options to show only meta and attachments
    
    Args:
        project_id: Set Project ID
        project_name: Set Project Name
        meta: Show only meta data
        attachment: Show only attachments
        output: Set output format. If none use default from config file
    """
    
    if not project_id and not project_name:
        sys.stderr.write(
            'ReadStore Error: Must Provide Project ID (--id) or Name (--name)\n')
        sys.stderr.write(
            'ReadStore Error: Run readstore project get -h for help\n')
        return
    
    # Get ReadStore Client and Validate Connection    
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return

    if output is None:
        output = client.get_output_format()
    
    try:
        project = client.get_project(project_id,
                                     project_name)
        
        if meta:
            out_data = project.pop('metadata', {})
        elif attachment:
            out_data = project.pop('attachments', {})
            out_data = {'name': out_data}
        else:
            out_data = project
        
        if output == 'json':
            print(out_data)
        elif output == 'text':
            header = list(out_data.keys())
            header_str = ' | '.join(header)
            print(header_str)
            
            if attachment:
                values_str = '\n'.join(out_data['name'])
            else:
                values = [str(out_data[key]) for key in header]
                values_str = ' | '.join(values)
            
            print(values_str)
        elif output == 'csv':
            header = list(out_data.keys())
            header_str = ','.join(header)
            print(header_str)
            
            if attachment:
                values_str = '\n'.join(out_data['name'])
            else:
                values = [str(out_data[key]) for key in header]
                values_str = ','.join(values)
            print(values_str)
        else:
            sys.stderr.write('Output Format Not Supported\n')
            return
        
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return


def download_fq_dataset_attachment(attachment_name: str,
                                   outpath: str,
                                   dataset_id: int | None = None,
                                   dataset_name: str | None = None):
    """Download Fastq Dataset Attachment

    Args:
        attachment_name: Choose attachment to download
        outpath: Set outpath to write file to.
        dataset_id: Set dataset id
        dataset_name: Set dataset name
    """
    
    if not dataset_id and not dataset_name:
        sys.stderr.write(
            'ReadStore Error: Must Provide Dataset ID (--id) or Name (--name)\n')
        sys.stderr.write(
            'ReadStore Error: Run readstore download -h for help\n')
        return

    # Get ReadStore Client and Validate Connection
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    outpath = os.path.abspath(outpath)
    out_dirname = os.path.dirname(outpath)
    
    # case directory path (e.g. '.' or /home/user/)
    if os.path.isdir(outpath):
        download_path = os.path.join(outpath, attachment_name)
    # case full path is provided, e.g. test.png or /home/user/test.png
    elif os.path.isdir(out_dirname):
        download_path = outpath
    else:
        sys.stderr.write(
            f'ReadStore Error: Output Directory Path Not Found: {outpath}\n')
        return
    
    try:
        client.download_fq_dataset_attachment(
            attachment_name=attachment_name,
            outpath=download_path,
            dataset_id=dataset_id,
            dataset_name=dataset_name)
        
        print(f'ReadStore Download: {attachment_name}\nDownloaded to {outpath}')
        
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    
def download_project_attachment(attachment_name: str,
                                outpath: str,
                                project_id: int | None = None,
                                project_name: str | None = None):
    """Download Project Attachment

    Download attachment file from project defined by project id
    or project name and download attachment_name
    
    Either project_id and project_name are required
    
    Args:
        attachment_name: Choose attachment to download
        outpath: Set outpath to write file to.
        project_id: Set project id
        project_name: Set project name
    """
    
    if not project_id and not project_name:
        sys.stderr.write(
            'ReadStore Error: Must Provide Project ID (--id) or Name (--name)\n')
        sys.stderr.write(
            'ReadStore Error: Run readstore project download -h for help\n')
        return
    
    # Get ReadStore Client and Validate Connection
    try:
        client = _get_readstore_client()
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return
    
    outpath = os.path.abspath(outpath)
    out_dirname = os.path.dirname(outpath)
    
    # case directory path (e.g. '.' or /home/user/)
    if os.path.isdir(outpath):
        download_path = os.path.join(outpath, attachment_name)
    # case full path is provided, e.g. test.png or /home/user/test.png
    elif os.path.isdir(out_dirname):
        download_path = outpath
    else:
        sys.stderr.write(
            f'ReadStore Error: Output Directory Path Not Found: {outpath}\n')
        return
    
    try:
        client.download_project_attachment(
            attachment_name=attachment_name,
            outpath=download_path,
            project_id=project_id,
            project_name=project_name)
        
        print(f'ReadStore Download: {attachment_name}\nDownloaded to {outpath}')
        
    except rsexceptions.ReadStoreError as e:
        sys.stderr.write(f'ReadStore Error: {e.message}\n')
        return


def main():
    """
    Main function for ReadStore CLI
    
    """
    
    args = parser.parse_args()
    
    if args.version:
        print(f'ReadStore CLI Version: {__version__}')
        sys.exit(0)
    
    # Keep hierarchy of commands. First check for subparsers.
    elif 'config_list' in args:
        configure_list()
    
    elif 'config_run' in args:
        configure()

    elif 'upload_run' in args:
        upload(fastq_files=args.fastq_files)
        
    elif 'list_fq_run' in args:
        list_fq_datasets(project_name=args.project_name,
                         project_id=args.project_id,
                         role=args.role,
                         meta=args.meta,
                         attachment=args.attachment,
                         output=args.output)
    
    elif 'get_fq_run' in args:
        read1 = args.read1
        read2 = args.read2
        index1 = args.index1
        index2 = args.index2
        read1_path = args.read1_path
        read2_path = args.read2_path
        index1_path = args.index1_path
        index2_path = args.index2_path
        
        meta = args.meta
        attachment = args.attachment
        
        if sum([read1,
                read2,
                index1,
                index2,
                read1_path,
                read2_path,
                index1_path,
                index2_path,
                meta,
                attachment]) > 1:
            sys.stderr.write("""ReadStore Error: Only One Flag Allowed for -r1, -r2,
                             -i1, -i2, -m, -r1p, -r2p, -i1p, -i2p, -m, -a\n\n""")
            get_fq_parser.print_help()
        else:
            get_fastq_dataset(dataset_id=args.id,
                              dataset_name=args.name,
                              meta=meta,
                              attachment=attachment,
                              read1=read1,
                              read2=read2,
                              index1=index1,
                              index2=index2,
                              read1_path=read1_path,
                              read2_path=read2_path,
                              index1_path=index1_path,
                              index2_path=index2_path,
                              output=args.output)
        
    elif 'download_run' in args:
        download_fq_dataset_attachment(attachment_name=args.attachment,
                                       outpath=args.outpath,
                                       dataset_id=args.id,
                                       dataset_name=args.name)
    
    elif 'list_project_run' in args:
        list_projects(role=args.role,
                      meta=args.meta,
                      attachment=args.attachment,
                      output=args.output)
    
    elif 'get_project_run' in args:
        get_project(project_id=args.id,
                    project_name=args.name,
                    meta=args.meta,
                    attachment=args.attachment,
                    output=args.output)
    
    elif 'download_project_run' in args:
        download_project_attachment(attachment_name=args.attachment,
                                    outpath=args.outpath,
                                    project_id=args.id,
                                    project_name=args.name)
        
    elif 'project_run' in args:
        project_parser.print_help()
    
    else:
        parser.print_help()
    

if __name__ == '__main__':
    main()
