"""SSE (Server-Sent Events) utilities for FastAPI."""

import json
from collections.abc import AsyncGenerator
from typing import Any

from fastapi.responses import StreamingResponse


def create_sse_response(
    generator: AsyncGenerator[dict[str, Any], None],
) -> StreamingResponse:
    """Create a StreamingResponse for SSE events.

    Args:
        generator: Async generator that yields dict events

    Returns:
        StreamingResponse configured for SSE

    """
    return StreamingResponse(
        event_generator(generator),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


async def event_generator(
    source: AsyncGenerator[dict[str, Any], None],
) -> AsyncGenerator[str, None]:
    """Convert dict events to SSE format.

    Args:
        source: Async generator yielding dict events

    Yields:
        SSE formatted strings: "data: {...}\\n\\n"

    """
    try:
        async for event in source:
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
    except Exception as e:
        # Send error event before closing
        error_event = {"type": "error", "content": str(e)}
        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
