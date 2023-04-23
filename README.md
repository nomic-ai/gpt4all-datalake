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
By sending data to the GPT4All-Datalake you agree to the following.

Data sent to this datalake will be used to train open-source large language models and released to the public.
There is no expectation of privacy to any data entering this datalake. You can, however, expect attribution. If you attach a unique identifier
that associates you as the data contributor, Nomic will retain that identifier in any LLM trains that it conducts.
You will receive credit and public attribution if Nomic releases any model trained on your submitted data.
You can also submit data anonymously.


### Where does the gpt4all-datalake run?`
While open-sourced under an Apache-2 License, this datalake runs on infrastructure managed and paid for by Nomic AI.
You are welcome to run this datalake under your own infrastructure! We just ask you also release the underlying data
that gets sent into it under the same attribution terms.


### Development
1. Clone down the repository.
2. Run `make testenv` to build all docker images and launch the HTTP server.
3. Go to 'http://localhost/docs' to view the API documentation.
4. You can run the unit tests with `make test`. Any edits made to the FastAPI app will hot reload.