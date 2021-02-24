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

function copyText() {
    let text = document.getElementById("new_link");
    text.select();
    document.execCommand("copy");
    text.value += ' ';
    text.value = text.value.slice(0, -1);
    swapTextAndIcon()
}

function swapTextAndIcon() {
    const icon = document.getElementById("copy_button").innerHTML
    document.getElementById("copy_button_icon").remove()
    document.getElementById("copy_button").insertAdjacentHTML(
        "afterbegin", '<span class="copy_button_text" id="copy_button_text">Copied</span>'
    )
    setTimeout(() => {
        document.getElementById("copy_button_text").remove()
        document.getElementById("copy_button").insertAdjacentHTML("afterbegin", icon)
    }, 1500)
}

const shorten_button = document.getElementById("short_url_button")
shorten_button.addEventListener("mouseover", () => shorten_button.classList.add("white_icon"), true)
shorten_button.addEventListener("mouseout", () => shorten_button.classList.remove('white_icon'), true)

const copy_button = document.getElementById("copy_button")
copy_button.addEventListener("mouseover", () => copy_button.classList.add("white_icon"), true)
copy_button.addEventListener("mouseout", () => copy_button.classList.remove("white_icon"), true)
