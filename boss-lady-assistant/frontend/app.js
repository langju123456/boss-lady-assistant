async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

function show(id, data) {
  document.getElementById(id).textContent = JSON.stringify(data, null, 2);
}

document.getElementById("recordButton").addEventListener("click", async () => {
  const text = document.getElementById("recordText").value;
  show("recordResult", await request("/api/record", {
    method: "POST",
    body: JSON.stringify({ text }),
  }));
});

document.getElementById("reportButton").addEventListener("click", async () => {
  const period = document.getElementById("period").value;
  show("reportResult", await request(`/api/reports/${period}`));
});

document.getElementById("contentButton").addEventListener("click", async () => {
  const topic = document.getElementById("contentTopic").value;
  show("contentResult", await request("/api/content", {
    method: "POST",
    body: JSON.stringify({ topic }),
  }));
});

document.getElementById("adviceButton").addEventListener("click", async () => {
  const question = document.getElementById("adviceQuestion").value;
  show("adviceResult", await request("/api/advice", {
    method: "POST",
    body: JSON.stringify({ question }),
  }));
});

