from fastapi.testclient import TestClient


example_conversation = [{'content': 'Hello, how can I assist you today?',
                          'role': 'assistant',
                          'rating': 'negative',
                          'edited_content': 'Hello, how may I assist you today?'},
                         {'content': 'Write me python code to contribute data to the GPT4All Datalake!', 'role': 'user'}]

barebones_conversation = [{'content': 'Hello, how can I assist you today?',},
                         {'content': 'Write me python code to contribute data to the GPT4All Datalake!'}]

def test_chat_history_upload(client):
    response = client.post(
        "/v1/ingest/chat",
        json={
            'source': 'unittest',
            'submitter_id': 'unittest',
            'agent_id': 'test_agent',
            'conversation': example_conversation

        }
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/ingest/chat",
        json={
            'source': 'unittest',
            'submitter_id': 'unittest',
            'agent_id': 'test_agent',
            'conversation': barebones_conversation

        }
    )
    assert response.status_code == 200

    return True