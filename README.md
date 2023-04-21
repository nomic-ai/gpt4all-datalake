# gpt4all-datalake
An open-source datalake to ingest, organize and efficiently store all data contributions made to the gpt4all projects.


### Architecture
The core datalake architecture is a simple HTTP API (written in FastAPI) that ingests JSON in a fixed schema, performs some integrity checking and stores it. This JSON is transformed into storage efficient Arrow/Parquet files and stored in a target filesystem. A light-weight index of the entire parquet filesystem is maintained with DuckDB.

#### Data formats
- Data is stored on disk in parquet files in subdirectories organized by day. These parquet files have a standardized schema allowing for easy manipulation in any programming language.
- 

### Open sourcing the data.
Nomic AI will provide automatic snapshots of this raw parquet data.
You will be able to interact with the snapshots:
- In automatic [Atlas](https://atlas.nomic.ai/) maps over its raw, cleaned and curated form.
- Through highly-processed downloads where the data has been curated, de-duplicated and cleaned for LLM training/finetuning.


### Data Privacy


### Where does the gpt4all-datalake run?
While the source code is open-sourced under an Apache-2 License, this datalake run on infrastructure managed and paid for by Nomic AI. 
