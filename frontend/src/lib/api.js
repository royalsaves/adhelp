const defaultHeaders = {
  "Content-Type": "application/json"
};

export async function postJson(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: defaultHeaders,
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}
