async function receiveShortLink() {
    const response = await fetch(window.location.href + "/new_link", {
        method: "POST",
        headers: { "Content-Type": "application/json;charset=utf-8" },
        body: JSON.stringify({ "link": document.getElementById("user-link").value })
    });

    const generated_link =  document.getElementById("new-generated-link");

    if (response.ok) {
        const result = await response.json();
        generated_link.value = result.success ? result.link : result.error;
    } else {
        generated_link.value = `Error ${response.status}`;
    }
}

function copyText() {
    let text = document.getElementById("new-generated-link");
    text.select();
    document.execCommand("copy");
    text.value += " ";
    text.value = text.value.slice(0, -1);
    swapTextAndIcon();
}

function swapTextAndIcon() {
    const icon = document.getElementById("button_copy-text").innerHTML;
    document.getElementById("button_copy-text__icon").remove();
    document.getElementById("button_copy-text").insertAdjacentHTML(
        "afterbegin", '<span class="button_copy-text_clicked" id="button_copy-text_clicked">Copied</span>'
    );
    setTimeout(() => {
        document.getElementById("button_copy-text_clicked").remove()
        document.getElementById("button_copy-text").insertAdjacentHTML("afterbegin", icon)
    }, 1500);
}
