async function receiveShortLink() {
    let response = await fetch(window.location.href + "/new", {
        method: "POST",
        headers: { "Content-Type": "application/json;charset=utf-8" },
        body: JSON.stringify({ "link": document.getElementById("user_link").value })
    });

    let result = await response.json();
    if (result.success) {
        document.getElementById("new_link").value = result.link
    } else {
        document.getElementById("new_link").value = result.error
    }
}
