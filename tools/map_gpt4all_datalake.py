import pyarrow.parquet as pq
import os


def stream_gpt4all_datalake(datalake_dump_path: str):

    for root, dirs, files in os.walk(datalake_dump_path):
        for filename in files:
            table = pq.read_table(os.path.join(root, filename))
            chat = table.to_pylist()

            datalake_item = {
                'chat': chat,
                **dict(table.schema.metadata)
            }
            yield datalake_item

if __name__ == "__main__":
    path = 'datalake_dump'

    parquet_files = stream_gpt4all_datalake(datalake_dump_path=path)



