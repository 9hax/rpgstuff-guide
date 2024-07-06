const searchBar = document.getElementById("search-form")
const searchItems = document.querySelectorAll("[data-search]")

const updateSearch = () => {
    let needle = searchBar.value.trim().toUpperCase()

    searchItems.forEach((item) => {
        if (!needle.length) {
            item.classList.remove('hide')
        } else {
            let hay = item.getAttribute('data-search').toUpperCase()

            if (hay.includes(needle)) {
                item.classList.remove('hide')
            } else {
                item.classList.add('hide')
            }
        }
    })
}

searchBar.addEventListener('keydown', updateSearch)
searchBar.addEventListener('input', updateSearch)
searchBar.addEventListener('change', updateSearch)