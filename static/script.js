async function shortenUrl() {
    const urlInput = document.getElementById("urlInput").value;
    const resultElement = document.getElementById("shortenedUrl");

    if (!urlInput) {
        resultElement.innerHTML = "❌ אנא הכנס כתובת URL";
        return;
    }

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: urlInput }),
        });

        const data = await response.json();

        if (response.ok) {
            resultElement.innerHTML = `✅ קישור מקוצר: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
        } else {
            resultElement.innerHTML = `❌ שגיאה: ${data.error}`;
        }
    } catch (error) {
        console.error("Error:", error);
        resultElement.innerHTML = "❌ שגיאה בלתי צפויה";
    }
}