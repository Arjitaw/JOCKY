const API_BASE_URL =
  import.meta.env["VITE_API_BASE_URL"] ||
  "http://127.0.0.1:5000";;


export async function checkHealth() {
  const response = await fetch(
    `${API_BASE_URL}/health`
  );

  if (!response.ok) {
    throw new Error("API is unavailable");
  }

  return response.json();
}


export async function executeCommand(command: string) {
  const response = await fetch(
    `${API_BASE_URL}/command`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        command: command,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Command failed"
    );
  }

  return data;
}