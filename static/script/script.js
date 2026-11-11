
// Sweet search functionality

const sweetSearch = document.getElementById("sweetSearch");

if (sweetSearch) {

    sweetSearch.addEventListener("input", function () {

        const searchValue = this.value.toLowerCase();

        const sweetItems = document.querySelectorAll(".sweet-item");

        let found = 0;

        sweetItems.forEach(function (item) {

            const sweetName = item.textContent.toLowerCase();

            if (sweetName.includes(searchValue)) {
                item.style.display = "";
                found++;
            } else {
                item.style.display = "none";
            }

        });

        const noResults = document.getElementById("noResults");

        noResults.hidden = found !== 0;

    });

}
