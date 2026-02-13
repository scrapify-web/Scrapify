async function start() {
  const url = document.getElementById("url").value;
  const status = document.getElementById("status");

  if (!url.startsWith("http")) {
    status.innerText = "Status: Invalid URL";
    return;
  }

  status.innerText = "Status: Extracting...";

  try {
    const response = await fetch("http://127.0.0.1:8000/scrape", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: url,
        depth: 1,
        use_js: true
      })
    });

    const data = await response.json();

    if (data.pages && data.pages.length > 0) {
      status.innerText = `Status: Extracted ${data.pages.length} page(s) ✔`;
    } else {
      status.innerText = "Status: No data found";
    }

  } catch (err) {
    status.innerText = "Status: Backend not running ❌";
    console.error(err);
  }
}
