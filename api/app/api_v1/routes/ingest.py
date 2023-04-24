import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import pyarrow as pa
import pyarrow.parquet as pq
import uuid
import os
from datetime import datetime, date

from api_v1.models import ChatIngestRequest, ChatIngestResponse, SuccessResponse
from api_v1.settings import settings


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["Ingest"])


async def chat_ingest_request_to_arrow_table(request: ChatIngestRequest):
    '''Converts a ChatIngestRequest to an arrow table for efficient storage.'''

    print(request.conversation)
    if request.ingest_id is None:
        ingest_id = str(uuid.uuid4())
    else:
        ingest_id = str(request.ingest_id)

    arrow_conversation_schema = pa.schema([

        pa.field('turn', pa.int32()),
        pa.field('content', pa.string()),
        pa.field('role', pa.string()),
        pa.field('rating', pa.string()),
        pa.field('stopped', pa.bool_()),
        pa.field('edited_content', pa.string()),
    ],
        metadata={"ingest_id": ingest_id,
                  'submitter_id': request.submitter_id,
                  'agent_id': request.agent_id})

    conversation = pa.Table.from_pylist([{**item.dict(), 'turn': idx} for idx, item in enumerate(request.conversation)], schema=arrow_conversation_schema)

    return conversation, ingest_id


@router.post("/chat")
async def ingest_chat(request: ChatIngestRequest):

    arrow_table, ingest_id = await chat_ingest_request_to_arrow_table(request=request)
    ingest_save_path = os.path.join(settings.root_filesystem_path, 'data', "{:%Y_%m_%d}".format(datetime.now()), 'chats')

    if not os.path.exists(ingest_save_path):
        os.makedirs(ingest_save_path, exist_ok=True)

    ingest_save_path = os.path.join(ingest_save_path, f"{ingest_id}.parquet")

    pq.write_table(arrow_table, ingest_save_path, compression=None)

    return ChatIngestResponse(ingest_id=ingest_id)
