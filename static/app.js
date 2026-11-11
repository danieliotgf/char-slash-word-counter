const input = document.getElementById("input");
const status = document.getElementById("status");
const fields = ["words", "characters", "characters_no_spaces", "paragraphs"];

let timer = null;
let inflight = null;

function render(counts) {
  for (const key of fields) {
    document.getElementById(key).textContent = counts[key].toLocaleString();
  }
}

async function update() {
  inflight?.abort();
  inflight = new AbortController();
  try {
    const res = await fetch("/api/count", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input.value }),
      signal: inflight.signal,
    });
    if (!res.ok) throw new Error(res.status === 413 ? "Text is too large." : `Server error (${res.status}).`);
    render(await res.json());
    status.textContent = "";
    status.classList.remove("error");
  } catch (err) {
    if (err.name === "AbortError") return;
    status.textContent = err.message.startsWith("Failed to fetch") ? "Can't reach the server." : err.message;
    status.classList.add("error");
  }
}

input.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(update, 120);
});

document.getElementById("clear").addEventListener("click", () => {
  input.value = "";
  input.focus();
  update();
});
