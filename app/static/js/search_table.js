// static/js/search_table.js

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchbar");
  const clearButton = document.getElementById("clear-search");
  const tableRows = document.querySelectorAll("tbody tr");

  // Filter function
  const filterTable = () => {
    const query = searchInput.value.toLowerCase().trim();

    tableRows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        row.style.display = rowText.includes(query) ? "" : "none";
    });
  };

  // Event: typing in the search bar
  searchInput.addEventListener("input", filterTable);

  // Event: Clear Button
  if (clearButton) {
    clearButton.addEventListener("click", () => {
        searchInput.value = "";
        filterTable();
        searchInput.focus();
    })
  }
});
