let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert-close");

if (alertWrapper) {
    alertClose.addEventListener(
        "click",
        () => (alertWrapper.style.visibility = "hidden")
    );
}


let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()
            let page = this.dataset.page
            searchForm.innerHTML += `<input value=${page} name="page" hidden />`
            searchForm.submit()
        })
    }
}