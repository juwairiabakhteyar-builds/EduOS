const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");

if (passwordInput && toggleButton) {

    toggleButton.addEventListener("click", function () {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";
            toggleButton.textContent = "Hide";

        } else {

            passwordInput.type = "password";
            toggleButton.textContent = "Show";

        }

    });

}

/* =========================================================
   EduOS keyboard search
========================================================= */
document.addEventListener("keydown", function (event) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        const search = document.querySelector(".topbar-search input");
        if (search) {
            search.focus();
            search.select();
        }
    }
});

const globalSearch = document.querySelector(".topbar-search input");

if (globalSearch) {
    globalSearch.addEventListener("input", function () {
        const term = this.value.trim().toLowerCase();
        const items = document.querySelectorAll(".sidebar-nav .nav-item");

        items.forEach(function (item) {
            const label = item.textContent.trim().toLowerCase();
            item.style.display = !term || label.includes(term) ? "" : "none";
        });
    });

    globalSearch.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            this.value = "";
            this.dispatchEvent(new Event("input"));
            this.blur();
        }
    });
}
