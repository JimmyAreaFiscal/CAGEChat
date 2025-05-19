/**
 * Unit test for chatStream() using Jest.
 * Mocks the fetch() call with a minimal in-memory ReadableStream.
 */

import { chatStream } from "./client/src/request_chat.js";

function mockFetchWithStream(chunks) {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      statusText: "OK",
      body: new ReadableStream({
        start(controller) {
          const enc = new TextEncoder();
          chunks.forEach(txt => controller.enqueue(enc.encode(txt)));
          controller.close();
        },
      }),
    })
  );
}

describe("chatStream()", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it("parses events and yields them in order", async () => {
    mockFetchWithStream([
      'data:{"type":"checkpoint","checkpoint_id":"abc"} \n\n',
      'data: {"type":"end"} \n\n',
    ]);

    const events = [];
    for await (const ev of chatStream("Hello world")) {
      events.push(ev);
    }

    expect(events).toEqual([
      { type: "checkpoint", checkpoint_id: "abc" },
      { type: "end" },
    ]);

    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
