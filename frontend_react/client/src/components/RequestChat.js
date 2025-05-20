/* Helper for calling the FastAPI `/chat_stream/` endpoint via
   Server-Sent Events (text/event-stream).

   Usage example in a React component:
   for await (const ev of chatStream("Hello world", null)) {
       console.log(ev);    // { type: "...", ... }
   }
*/

const API_URL = process.env.REACT_APP_API_URL ?? "http://127.0.0.1:8000";

/**
 * Async generator that yields parsed JSON events coming from
 * the backend `/chat_stream/` endpoint.
 *
 * @param {string} message        – User message
 * @param {string|null} checkpointId – (Optional) checkpoint_id
 * @returns {AsyncGenerator<object>}
 */

export async function* chatStream(message, checkpointId = null) {
  const params = new URLSearchParams({ message });
  
  if (checkpointId) params.append("checkpoint_id", checkpointId);

  const response = await fetch(`${API_URL}/chat_stream/?${params.toString()}`, {
    method: "GET",
    headers: { Accept: "text/event-stream" },
  });

  if (!response.ok) {
    throw new Error(`Chat stream failed: ${response.status} ${response.statusText}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Split on double-newline (event delimiter in SSE)
    let idx;
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      const rawChunk = buffer.slice(0, idx).trim();
      buffer = buffer.slice(idx + 2);         // consume this event

      if (rawChunk.startsWith("data:")) {
        const payload = rawChunk.slice(5).trim();
        if (payload) {
          try {
            yield JSON.parse(payload);
          } catch (e) {
            console.error("Invalid SSE JSON:", payload, e);
          }
        }
      }
    }
  }
}
