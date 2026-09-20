document.addEventListener("DOMContentLoaded", function () {
    
    const seatsInput = document.querySelector("input[name='seats']");
    const showSelect = document.querySelector("select[name='show_id']");
    const totalDisplay = document.querySelector("#estimated_total");

    function updateTotal() {
        const seats = parseInt(seatsInput.value) || 0;

        // Get selected option
        const selectedOption = showSelect.options[showSelect.selectedIndex];

        // Get ticket price from data attribute
        const price = parseFloat(selectedOption.getAttribute("data-price")) || 0;

        const total = seats * price;

        totalDisplay.innerText = "₹ " + total.toFixed(2);
    }

    // Trigger on change
    seatsInput.addEventListener("input", updateTotal);
    showSelect.addEventListener("change", updateTotal);
});