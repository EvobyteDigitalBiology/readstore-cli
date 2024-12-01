# ReadStore CLI

This README describes the ReadStore Command Line Interface (CLI). Also available as [GitHub Page](#https://evobytedigitalbiology.github.io/readstore-cli/).

The ReadStore CLI is used to upload FASTQ files and Processed Data to the ReadStore database and access Projects, Datasets, metadata and attachment files.
The ReadStore CLI enables you to automate your bioinformatics pipelines by providing simple and standardized access to datasets.
 
Check the [ReadStore Github repository](https://github.com/EvobyteDigitalBiology/readstore) for more information how to get started.

More infos on the ReadStore website https://evo-byte.com/readstore/

**Tutorials** and Intro Videos how to get started: https://www.youtube.com/@evobytedigitalbio

Blog posts and How-Tos: https://evo-byte.com/blog/

For general questions reach out to info@evo-byte.com

Happy analysis :)

## Table of Contents
- [Description](#description)
- [Security and Permissions](#backup)
- [Installation](#installation)
- [Usage](#usage)
    - [Quickstart](#quickstart)
    - [CLI Configuration](#cliconfig)
    - [FASTQ Upload](#upload)
    - [Access Projects](#projectaccess)
    - [Access Datasets](#datasetaccess)
    - [Access Processed Data](#prodata)
- [Contributing](#contributing)
- [License](#license)
- [Credits and Acknowledgments](#acknowledgments)


## The Lean Solution for Managing NGS and Omics Data

ReadStore is a platform for storing, managing, and integrating genomic data. It accelerates analysis and offers an easy way to manage and share FASTQ file, NGS datasets and processed datasets. 
With built-in project and metadata management, ReadStore structures your workflows, and its collaborative user interface enhances teamwork — so you can focus on generating insights.

The integrated Webservice (API) enables your to directly retrieve data from ReadStore via the terminal [Command-Line-Interface (CLI)](https://github.com/EvobyteDigitalBiology/readstore-cli) or [Python](https://github.com/EvobyteDigitalBiology/pyreadstore) / [R](https://github.com/EvobyteDigitalBiology/r-readstore) SDKs. 

The ReadStore Basic version provides a local web server with simple user management. For organization-wide deployment, advanced user and group management, or cloud integration, please check out the ReadStore Advanced versions and contact us at info@evo-byte.com.

## Description

The ReadStore Command-Line Interface (CLI) is a powerful tool for uploading and managing your omics data. With the ReadStore CLI, you can upload FASTQ files and **Pro**cessed **Data** directly to the ReadStore database, as well as access and manage Projects, Datasets, metadata, and attachment files with ease.

The CLI can be run from your shell or terminal and is designed for seamless integration into data pipelines and scripts, enabling efficient automation of data management tasks. This flexibility allows you to integrate the ReadStore CLI within any bioinformatics application or pipeline, streamlining data uploads, access, and organization within ReadStore.

By embedding the ReadStore CLI in your bioinformatics workflows, you can improve efficiency, reduce manual tasks, and ensure your data is readily accessible for analysis and collaboration.

## Security and Permissions<a id="backup"></a>

**PLEASE READ AND FOLLOW THESE INSTRUCTIONS CAREFULLY!**

### User Accounts and Token<a id="token"></a>

Using the CLI with a ReadStore server requires an active User Account and a Token. You should **never enter your user account password** when working with the CLI.

To retrieve your token:

1. Login to the ReadStore web app via your browser
2. Navigate to `Settings` page and click on `Token`
3. If needed you can regenerate your token (`Reset`). This will invalidate the previous token

For uploading FASTQ files or **Pro**cessed **Data** your User Account needs to have `Staging Permission`. If you can check this in the `Settings` page of your account. If you not have `Staging Permission`, ask the ReadStore server Admin to grant you permission.

### CLI Configuration

After running the `readstore configure` the first time, a configuration file is created in your home directory (`~/.readstore/config`) to store your credentials and CLI configuration.

The config file is created with user-excklusive read-/write permissions (`chmod 600`), please make sure to keep the file permissions restricted.

You find more information on the [configuration file](#cliconfig) below.

## Installation

`pip3 install readstore-cli`

You can perform the install in a conda or venv virtual environment to simplify package management.

A local install is also possible

`pip3 install --user readstore-cli`

Make sure that `~/.local/bin` is on your `$PATH` in case you encounter problems when starting the server.

Validate the install by running

`readstore -v`

This should print the ReadStore CLI version

## Usage

Detailed tutorials, videos and explanations are found on [YouTube](https://www.youtube.com/playlist?list=PLk-WMGySW9ySUfZU25NyA5YgzmHQ7yquv) or on the [**EVO**BYTE blog](https://evo-byte.com/blog).

### Quickstart<a id="quickstart"></a>

Let's upload some FASTQ files.

#### 1. Configure CLI

Make sure you have the ReadStore CLI installed and a running ReadStore server with your user registered.

1. Run `readstore configure`

2. Enter your username and [token](#token)
3. Select the default output of your CLI requests. You can choose between `text` outputs, comma-separated `csv` or `json`.
4. Run `readstore configure list` and check if your credentials are correct. 

#### 2. Upload Files

For uploading FASTQ files your User Account needs to have `Staging Permission`. If you can check this in the `Settings` page of your account. If you not have `Staging Permission`, ask the ReadStore Server Admin to grant you permission.

Move to a folder that contains some FASTQ files

`readstore upload myfile_r1.fastq`

This will upload the file and run the QC check. You can select multiple files at once using the `*` wildcard.
The fastq files need to have the default file endings `.fastq, .fastq.gz, .fq, .fq.gz`.

You can also upload multiple FASTQ files from a template `.csv` file using the `import fastq` function. More information below.

#### 3. Stage Files

Login to the web app on your browser and move to the `Staging` page. Here you find a list of all FASTQ files that you just uploaded. For larger files, the QC step can take a while to complete.

FASTQ files are grouped into Datasets which you can `Check In`. Checked In Datasets appear in the `Datasets` page and can be accessed by the CLI.

Check the `Batch Check In` button to import several Dataset at once.

#### 4. Access Datasets via the CLI

The ReadStore CLI enables programmatic access to Datasets and FASTQ files. Some examples are:

`readstore list`  List all FASTQ files

`readstore get --id 25`  Get detailed view on Dataset 25

`readstore get --id 25 --read1-path`  Get path for Read1 FASTQ file

`readstore get --id 25 --meta`  Get metadata for Dataset 25

`readstore project get --name cohort1 --attachment`  Get attachment files for Project "cohort1"

You can find a full list of CLI commands below.


#### 5. Managing **Pro**cessed **Data**<a id="manage_pro_data"></a>

**Pro**cessed **Data** refer to files generated through processing of raw sequencing data.
Depending on the omics technology and assay used, this could be for instance transcript count files, variant files or gene count matrices. 

`readstore pro-data upload -d test_dataset_1 -n test_dataset_count_matrix -t count_matrix test_count_matrix.h5`  
Upload count matrix test_count_matrix.h5 with name "test_dataset_count_matrix" for dataset with name "test_dataset_1"

`readstore pro-data list` List Processed Data for all Datasets and Projects

`readstore pro-data get -d test_dataset_1 -n test_dataset_count_matrix` Get ProData details for Dataset "test_dataset_1" with the name "test_dataset_count_matrix"

`readstore pro-data delete -d test_dataset_1 -n test_dataset_count_matrix` Delete ProData for dataset "test_dataset_1" with the name "test_dataset_count_matrix"

The delete operation does not remove the file from the file system, only from the database. A user needs `Staging Permission` to create or remove datasets.


### CLI Configuration<a id="cliconfig"></a>

`readstore configure` manages the CLI configuration. To setup the configuration:

1. Run `readstore configure`

2. Enter your username and [token](#token)
3. Select the default output of your CLI requests. You can choose between `text` outputs, comma-separated `csv` or `json`.
4. Run `readstore configure list` and check if your credentials are correct. 

If you already have a configuration in place, the CLI will ask whether you want to overwrite the existing credentials. Select `y` if yes.

After running the `readstore configure` the first time, a configuration file is created in your home directory (`~/.readstore/config`).
The config file is created with user-excklusive read-/write permissions (`chmod 600`), please make sure to keep the file permissions restricted.

```
[general]
endpoint_url = http://localhost:8000
fastq_extensions = ['.fastq', '.fastq.gz', '.fq', '.fq.gz']
output = csv

[credentials]
username = myusername
token = myrandomtoken
``` 

You can further edit the configuration of the CLI client from this configuration file. In case your ReadStore Django server is not run at the default port 8000, you need to update the `endpoint_url`. If you need to process FASTQ files with file endings other than those listed in `fastq_extensions`, you can modify the list.

### Upload FASTQ Files<a id="upload"></a>

For uploading FASTQ files your User Account needs to have `Staging Permission`. You can check this in the `Settings` page of your account. If you do not have `Staging Permission`, ask the ReadStore Server Admin to grant you permission.

`readstore upload myfile_r1.fastq myfile_r2.fastq ...`

This will upload the files and run the QC check. You can select several files at once using the `*` wildcard. It can take some time before FASTQ files are available in your `Staging` page depending on how large file are and how long the QC step takes.

```
usage: readstore upload [options]

Upload FASTQ Files

positional arguments:
  fastq_files  FASTQ Files to Upload
```

### Import FASTQ files from .csv Template<a id="import_template"></a>

Import FASTQ files from template .csv file.

A `.csv` file can be downloaded from the ReadStore App in the `Staging` Page or from this repository, 
or is available in this repository under assets/readstore_template.csv

The template .csv file must contain the columns `FASTQFileName`,`ReadType` &	`UploadPath`.

- **FASTQFileName** Name for the FASTQ File in ReadStore DB
- **ReadType** FASTQ Read Type: R1 (Read 1), R2 (Read 2), I1 (Index 1) or I2 (Index 2)
- **Upload Path** File path to FASTQ file. Must be accessible from ReadStore server

```
usage: readstore import fastq [options]

Import FASTQ Files

positional arguments:
  fastq_template  FASTQ Template .csv File
```

### Access Projects<a id="projectaccess"></a>

There are 3 commands for accessing projects, `readstore project list`, `readstore project get` and `readstore project download`.

- `list` provides an overview of project, metadata and attachments
- `get` provides detailed information on individual projects and to its metadata and attachments
- `download` lets you download attachment files of a project from the ReadStore database

####  readstore project list

```
usage: readstore project ls [options]

List Projects

options:
  -h, --help            show this help message and exit
  -m, --meta            Get Metadata
  -a, --attachment      Get Attachment
  --output {json,text,csv}
                        Format of command output (see config for default)
```

Show project id and name.

The `-m/--meta` include metadata for projects as json string in output.

The `-a/--attachment` include attachment names as list in output.

Adapt the output format of the command using the `--output` options.


####  readstore project get

```
usage: readstore project get [options]

Get Project

options:
  -h, --help            show this help message and exit
  -id , --id            Get Project by ID
  -n , --name           Get Project by name
  -m, --meta            Get only Metadata
  -a, --attachment      Get only Attachment
  --output {json,text,csv}
                        Format of command output (see config for default)
```

Show project details for a project selected either by `--id` or the `--name` argument.
The project details include description, date of creation, attachments and metadata

The `-m/--meta` shows **only** the metadata with keys in header.

The `-a/--attachment` shows **only** the attachments.

Adapt the output format of the command using the `--output` options.

Example: `readstore project get --id 2`

####  readstore project download

```
usage: readstore project download [options]

Download Project Attachments

options:
  -h, --help          show this help message and exit
  -id , --id          Select Project by ID
  -n , --name         Select Project by name
  -a , --attachment   Set Attachment Name to download
  -o , --outpath      Download path or directory (default . )
```

Download attachment files for a project. Select a project selected either by `--id` or the `--name` argument.

With the `--attachment` argument you specify the name of the attachment file to download.

Use the `--outpath` to set a directory to download files to.

Example `readstore project download --id 2 -a ProjectQC.pptx -o ~/downloads`


### Access Datasets and FASTQ Files<a id="datasetaccess"></a>

There are 3 commands for accessing dataset, `readstore list`, `readstore get` and `readstore download`.

- `list` provides an overview of datasets, metadata and attachments
- `get` provides detailed information on an individual dataset and to its metadata and attachments and individual FASTQ read files and statistics.
- `download` lets you download attachment files of a dataset

####  readstore list

```
usage: readstore ls [options]

List FASTQ Datasets

options:
  -h, --help            show this help message and exit
  -p , --project-name   Subset by Project Name
  -pid , --project-id   Subset by Project ID
  -m, --meta            Get Metadata
  -a, --attachment      Get Attachment
  --output {json,text,csv}
                        Format of command output (see config for default)
```

Show dataset id, name, description, qc_passed, paired_end, index_read, project_ids and project_names

`-p/--project-name` subset dataset from a specified project

`-pid/--project-id` subset dataset from a specified project

`-m/--meta` include metadata for datasets

`-a/--attachment` include attachment names as list for datasets

Adapt the output format of the command using the `--output` options.

####  readstore get

```
usage: readstore get [options]

Get FASTQ Datasets and Files

options:
  -h, --help            show this help message and exit
  -id , --id            Get Dataset by ID
  -n , --name           Get Dataset by name
  -m, --meta            Get only Metadata
  -a, --attachment      Get only Attchments
  -r1, --read1          Get Read 1 Data
  -r2, --read2          Get Read 2 Data
  -r1p, --read1-path    Get Read 1 FASTQ Path
  -r2p, --read2-path    Get Read 2 FASTQ Path
  -i1, --index1         Get Index 1 Data
  -i2, --index2         Get Index 2 Data
  -i1p, --index1-path   Get Index 1 FASTQ Path
  -i2p, --index2-path   Get Index 2 FASTQ Path
  --output {json,text,csv}
                        Format of command output (see config for default)

```

Show details for a dataset selected either by `--id` or the `--name` argument.

`-m/--meta` shows **only** the metadata with keys in header.

`-a/--attachment` shows **only** the attachments.

`-r1/--read1` shows details for dataset Read 1 data (same for `--read2`, `--index1`, `--index2`)

`-r1p/--read1-path` returns path for dataset Read 1 (same for `--read2-path`, `--index1-path`, `--index2-path`)

Adapt the output format of the command using the `--output` options.

Example: `readstore get --id 2`

Example: `readstore get --id 2 --read1-path`


####  readstore download

```
usage: readstore download [options]

Download Dataset attachments

options:
  -h, --help          show this help message and exit
  -id , --id          Select Dataset by ID
  -n , --name         Select Dataset by name
  -a , --attachment   Set Attachment Name to download
  -o , --outpath      Download path or directory (default . )
```

Download attachment files for a dataset. Select dataset either by `--id` or the `--name` argument.

With the `--attachment` argument you specify the name of the attachment file to download.

Use the `--outpath` to set a directory to download files to.

Example `readstore download --id 2 -a myAttachment.csv -o ~/downloads`

### Access **Pro**cessed **Data**<a id="prodata"></a>

#### readstore pro-data upload

```
usage: readstore pro-data upload [options]

Upload Processed Data

positional arguments:
  pro_data_file         Path to Processed Data File to Upload

options:
  -h, --help            show this help message and exit
  -did , --dataset-id   Set associated Dataset by ID
  -d , --dataset-name   Set associated Dataset by Name
  -n , --name           Set Processed Data Name (required)
  -t , --type           Set Type of Processed Data (e.g. gene_counts) (required)
  --description         Set Description
  -m META, --meta META  Set metadata as JSON string (e.g '{"key": "value"}')
```

Upload **Pro**cessed **Data** to ReadStore database and connect with an existing dataset.

**Pro**cessed **Data** can be any file type and tyically represent datasets for downstream omics analysis, for instance gene count matrices or variant files.

Your ReadStore user account is required to have `Staging Permissions` to upload or delete Processed Data.

You need to specify a `--dataset-id` or `--dataset-name` to select the dataset to attach files to.

`-n/--name` defines the name to set for the processed data in the ReadStore DB

`-t/--type` defines the data type of the processed dataset. The type is free to choose, for instance `gene_counts` or `count_matrix`

`-m/--meta` enables to set metadata for the processed data (optional). This attribute must be a json-formatted string, e.g. `'{"key": "value"}'`

`--description` set a optional description for the dataset (optional).

Example: `readstore pro-data upload -d test_dataset_1 -n test_dataset_count_matrix -t count_matrix -m '{"key":"value"}' test_count_matrix.h5`

#### readstore pro-data list

```
usage: readstore pro-data list [options]

List Processed Data

options:
  -h, --help            show this help message and exit
  -pid , --project-id   Subset by Project ID
  -p , --project-name   Subset by Project Name
  -did , --dataset-id   Subset by Dataset ID
  -d , --dataset-name   Subset by Dataset Name
  -n , --name           Subset by ProData Name
  -t , --type           Subset by Data Type
  -m, --meta            Get Metadata
  -a, --archived        Include Archived ProData
  --output {json,text,csv}
                        Format of command output (see config for default)
```

List **Pro**cessed **Data** stored in the ReadStore database.

You can subset the list by Projects (`-pid/-p`), Datasets (`-did/-d`) and/or by the specific Name (`-n`) of the **Pro**cessed **Data** stored.

`-m/--meta` Also show metadata

`-a/--archived` Show archived **Pro**cessed **Data**.

**Pro**cessed **Data** are archived when a new file with the same name attribute is uploaded. This invalidates a previous version of the **Pro**cessed **Data**

Example: `readstore pro-data list -p TestProject`

#### readstore pro-data get

```
usage: readstore pro-data get [options]

Get Processed Data

options:
  -h, --help            show this help message and exit
  -id , --id            Get ProData by ID
  -did , --dataset-id   Get ProData by Dataset ID
  -d , --dataset-name   Get ProData by Dataset Name
  -n , --name           Get ProData by Name
  -m, --meta            Get only Metadata
  -p, --upload-path     Get only Upload Path
  -v , --version        Get ProData Version (default: latest)
  --output {json,text,csv}
                        Format of command output (see config for default)
```

Get single **Pro**cessed **Data** by their `-id` or the associated `--dataset-id/--dataset-name` plus `--name` argument.

`-m/--meta` Return only metadata

`-p/--upload-path` Return only upload path

`-v/--version` Select ProData by specific version (Optional). Default: latest version.

Example: `readstore pro-data get -d test_dataset_1 -n test_dataset_count_matrix`

#### readstore pro-data delete

```
usage: readstore pro-data delete [options]

Delete Processed Data

options:
  -h, --help            show this help message and exit
  -id , --id            Delete ProData by ID
  -did , --dataset-id   Delete ProData by Dataset ID
  -d , --dataset-name   Delete ProData by Dataset Name
  -n , --name           Delete ProData by Name
  -v , --version        Delete ProData Version (default: latest)
```

Delete **Pro**cessed **Data** by their `-id` or the associated `--dataset-id / --dataset-name` plus `--name` argument.

`-v/--version` Delete ProData by specific version (Optional). Default: latest version.

Example: `readstore pro-data delete -d test_dataset_1 -n test_dataset_count_matrix`


## Contributing

Contributions make this project better! Whether you want to report a bug, improve documentation, or add new features, any help is welcomed!

### How You Can Help
- Report Bugs
- Suggest Features
- Improve Documentation
- Code Contributions

### Contribution Workflow
1. Fork the repository and create a new branch for each contribution.
2. Write clear, concise commit messages.
3. Submit a pull request and wait for review.

Thank you for helping make this project better!

## License

The ReadStore CLI is licensed under an Apache 2.0 Open Source License.
See the LICENSE file for more information.

## Credits and Acknowledgments<a id="acknowledgments"></a>

ReadStore CLI is built upon the following open-source python packages and would like to thank all contributing authors, developers and partners.

- Python (https://www.python.org/)
- Requests (https://requests.readthedocs.io/en/latest/)
