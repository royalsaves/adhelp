import { useState } from "react";
import { postJson } from "../lib/api";

export function FormPage({ title, description, fields, endpoint, successLabel = "Submitted" }) {
  const initialState = Object.fromEntries(fields.map((field) => [field.name, field.defaultValue || ""]));
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult("");

    try {
      const data = await postJson(endpoint, form);
      setResult(data.message || successLabel);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card">
      <div className="section-head">
        <p className="eyebrow">Workflow</p>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>

      <form className="stack" onSubmit={onSubmit}>
        {fields.map((field) => (
          <label key={field.name} className="field">
            <span>{field.label}</span>
            {field.type === "textarea" ? (
              <textarea
                value={form[field.name]}
                onChange={(event) => setForm({ ...form, [field.name]: event.target.value })}
                rows={field.rows || 4}
                placeholder={field.placeholder}
              />
            ) : (
              <input
                type={field.type || "text"}
                value={form[field.name]}
                onChange={(event) => setForm({ ...form, [field.name]: event.target.value })}
                placeholder={field.placeholder}
              />
            )}
          </label>
        ))}

        <button className="primary" type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>

      {result && <p className="success">{result}</p>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}
