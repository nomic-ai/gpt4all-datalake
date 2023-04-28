import pyarrow.parquet as pq
import os
from nomic import atlas


def stream_gpt4all_datalake(datalake_dump_path: str):

    for root, dirs, files in os.walk(datalake_dump_path):
        for filename in files:
            table = pq.read_table(os.path.join(root, filename))
            conversation = table.to_pylist()

            datalake_item = {
                'conversation': conversation,
                **dict({key.decode('utf8'): value.decode('utf8') for key, value in dict(table.schema.metadata).items()})
            }
            yield datalake_item


def map_prompt_response():

    path = 'datalake_dump'

    chats = stream_gpt4all_datalake(datalake_dump_path=path)

    chats_to_map = []

    chats = [chat for chat in chats]
    for chat in chats:
        for i in range(0, len(chat['conversation']), 2):
            user_prompt = chat['conversation'][i]['content']
            model_response = chat['conversation'][i+1]['content']
            chat_copy = chat.copy()
            chat_copy['conversation'] = f"User:\n{user_prompt}\nModel:\n{model_response}"
            chats_to_map.append(chat_copy)

    project = atlas.map_text(data=chats_to_map,
                             indexed_field='conversation',
                             name='GPT4All Datalake Prompt Responses',
                             )


def map_entire_conversation(chats):
    chats_to_map = []

    chats = [chat for chat in chats]
    for chat in chats:

        conversation = ""
        for idx, item in enumerate(chat['conversation']):
            conversation += f"Turn {idx}:\n{item['content']}\n"

        chat['conversation'] = conversation
        chats_to_map.append(chat)

    project = atlas.map_text(data=chats_to_map,
                             indexed_field='conversation',
                             name='GPT4All Datalake Conversations',
                             )

if __name__ == "__main__":

    path = 'datalake_dump'

    chats = stream_gpt4all_datalake(datalake_dump_path=path)

    map_entire_conversation(chats)


