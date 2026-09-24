const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function streamRAG(question, topK = 5, onChunk) {
  const response = await fetch(`${API_BASE_URL}/query/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        top_k: topK,
      }),
    }
  );

  if (!response.ok) {
    let errorMessage =
      "Failed to connect to RAG backend.";

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {

    }
    throw new Error(errorMessage);
  }

  if (!response.body) {
    throw new Error(
      "Streaming is not supported by this response."
    );
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(
          value,
          { stream: true }
        );

      if (chunk) {
        onChunk(chunk);
      }
    }
  } finally {
    reader.releaseLock();
  }
}
