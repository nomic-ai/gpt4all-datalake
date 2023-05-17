from enum import Enum

from typing import List, Optional
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    result = 'ok'


class Rating(str, Enum):
    positive = "positive"
    negative = "negative"

class IngestMetadata(BaseModel):
    source: Optional[str] = Field(None, description='The source contributing the ingest data.', example='gpt4all-chat')
    submitter_id: str = Field(None, description='An identifier for the entity that submitted the ingest', example='EliteHacker#42')

class ChatItem(BaseModel):
    content: str = Field(..., description='The textual contents of the chat turn', example='Hello, how can I assist you today?')
    role: Optional[str] = Field(None, description='The role of the entity that generated content.', example='assistant')
    rating: Optional[Rating] = Field(None, description='A rating of the chat item', example='negative')
    stopped: bool = Field(False, description='Was the generation stopped prior to completing?', example=True)
    edited_content: Optional[str] = Field(None, description='An optional edited version of the content.', example='Hello, how may I assist you today?')


class ChatIngestRequest(IngestMetadata):
    agent_id: str = Field(..., description='An identifier for the entity in the conversation', example='gpt4all-j-v1.2-jazzy')
    ingest_id: Optional[str] = Field(None, description='An identifier for the ingest. If a chat already exists with the identifier it will be overwritten.')
    conversation: List[ChatItem] = Field(..., description='The conversation history.',
                                         example=[{'content': 'Hello, how can I assist you today?',
                                                   'role': 'assistant',
                                                   'rating': 'negative',
                                                   'edited_content': 'Hello, how may I assist you today?'},
                                                  {'content': 'Write me python code to contribute data to the GPT4All Datalake!', 'role': 'user'}])
    prompt_template: str = Field(..., description="The prompt template used in the conversation")

class ChatIngestResponse(BaseModel):
    ingest_id: str = Field(..., description='The id of the ingest', example='d920b363-abab-4d19-a5b6-89d182115f82')
