import { useState } from "react";
import { postJson } from "../lib/api";

export function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "ai", text: "Ask about password resets, onboarding, or VPN access." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    const value = input.trim();
    if (!value || loading) return;

    const nextMessages = [...messages, { role: "user", text: value }];
    setMessages(nextMessages);
    setInput("");
    setLoading(true);

    try {
      const data = await postJson("/api/ai/chat", { messages: nextMessages });
      setMessages((current) => [...current, { role: "ai", text: data.response }]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        { role: "ai", text: error.message || "Failed to get a response." }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={`chat${open ? " open" : ""}`}>
      <button className="chat-toggle" onClick={() => setOpen((value) => !value)}>
        {open ? "Close Assistant" : "Open Assistant"}
      </button>
      {open && (
        <section className="chat-panel">
          <div className="chat-messages">
            {messages.map((message, index) => (
              <article key={`${message.role}-${index}`} className={`bubble ${message.role}`}>
                {message.text}
              </article>
            ))}
          </div>
          <div className="chat-input-row">
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => event.key === "Enter" && sendMessage()}
              placeholder="Type a support question"
            />
            <button onClick={sendMessage} disabled={loading}>
              {loading ? "..." : "Send"}
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
