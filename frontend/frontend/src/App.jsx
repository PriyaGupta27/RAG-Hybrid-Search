import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";
import { streamRAG } from "./services/api";

function App() {
  const [question, setQuestion] = useState("");
  const [topK, setTopK] = useState(5);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
  
    const currentQuestion = question.trim();
  
    if (!currentQuestion || loading) {
      return;
    }
  
    setQuestion("");
    setLoading(true);
  
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: currentQuestion,
      },
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);
  
    try {
      await streamRAG(
        currentQuestion,
        topK,
        (chunk) => {
          setMessages((previous) => {
            const updated = [...previous];
  
            const lastIndex =
              updated.length - 1;
  
            updated[lastIndex] = {
              ...updated[lastIndex],
              content:
                updated[lastIndex].content +
                chunk,
            };
  
            return updated;
          });
        }
      );
    } catch (error) {
      setMessages((previous) => {
        const updated = [...previous];
  
        const lastIndex =
          updated.length - 1;
  
        updated[lastIndex] = {
          ...updated[lastIndex],
          content:
            "Sorry, I couldn't process your request. Please try again.",
        };
  
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (question.trim() && !loading) {
        event.currentTarget.form.requestSubmit();
      }
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div className="brand">
          <div className="brand-icon">R</div>

          <div>
            <h1>Hybrid RAG</h1>
            <span>Document Assistant</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>


      <main className="chat-container">

        {messages.length === 0 && (
          <div className="welcome">

            <h2>How can I help you?</h2>

            <p>
              Ask questions about your documents.
            </p>

          </div>
        )}


        <div className="messages">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`message-row ${message.role}`}
            >

              <div
                className={`message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                {message.role === "assistant" ? (
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  message.content
                )}

              </div>


              {message.role === "assistant" &&
                message.sources?.length > 0 && (

                  <details className="sources">

                    <summary>
                      Sources
                    </summary>

                    <div className="source-list">

                      {message.sources.map(
                        (source, sourceIndex) => (

                          <div
                            className="source"
                            key={
                              source.chunk_id ||
                              sourceIndex
                            }
                          >
                            <span>
                              {sourceIndex + 1}.
                            </span>

                            <div>
                              <strong>
                                {source.source
                                  ?.split("\\")
                                  .pop()}
                              </strong>

                              <small>
                                Page {source.page}
                              </small>
                            </div>

                          </div>

                        )
                      )}

                    </div>

                  </details>
                )}

            </div>

          ))}


          {loading && (

            <div className="message-row assistant">

              <div className="message assistant-message loading">

                <span></span>
                <span></span>
                <span></span>

              </div>

            </div>

          )}

        </div>

      </main>


      <form
        className="input-container"
        onSubmit={handleSubmit}
      >

        <div className="input-box">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask a question"
            rows={1}
            disabled={loading}
          />

          <button
            type="submit"
            disabled={
              loading ||
              !question.trim()
            }
            className="send-button"
          >
            ↑
          </button>

        </div>


        <div className="input-footer">

          <span>
            Hybrid search · Reranking · Ollama
          </span>

          <label>
            Top K

            <select
              value={topK}
              onChange={(event) =>
                setTopK(
                  Number(event.target.value)
                )
              }
            >
              <option value={3}>3</option>
              <option value={5}>5</option>
              <option value={8}>8</option>
              <option value={10}>10</option>
            </select>

          </label>

        </div>

      </form>

    </div>
  );
}

export default App;