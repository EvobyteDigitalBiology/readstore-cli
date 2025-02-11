# Changelog

## [1.3.0] - 2025-02-11

**Features**

- Add create and update methods for projects and datasets into command line

**Updates**

- Improve code format

**Bugfixes**

- ProData upload ensure dataset id OR name is specified

## [1.2.0] - 2024-12-22

**Features**
- Update rsbasic client to complete CRUD methods (create, read, update, delete) for Projects, Datasets, and FASTQ files
    - create_project
    - update_project
    - delete_project
    - list_fq_files
    - create_fq_file
    - update_fq_file
    - delete_fq_file
    - create_fastq_dataset
    - update_fastq_dataset

**Updates**

- Improve Error messages

**Bugfixes**

- Fix error message when accessing read file path on non-existing datasets

## [1.1.0] - 2024-12-01

**Features**

- Add method pro-data upload
- Add method pro-data list
- Add method pro-data get
- Add method pro-data delete
- Add readstore_template.csv for uploading file

**Updates**

- upload_fastq: Add fastq_name and read_type arguments to enable definition of FASTQ names and read types
- Update backend endpoint to api_x_v1

## [1.0.2] - 2024-11-14

Feat Add import fastq function

## [1.0.1] - 2024-10-30

Update ReadMe and License

## [1.0.0] - 2024-10-30

Initial Version