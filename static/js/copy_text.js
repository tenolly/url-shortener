function copyText() {
    let text = document.getElementById("new_link");
    text.select()
    document.execCommand("copy");
    text.value += ''
}
