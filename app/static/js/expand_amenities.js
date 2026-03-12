function toggleAmenities() {
    const chips = document.querySelectorAll('.amenity-chip');
    const btn = document.getElementById('amenities-toggle');
    const totalAmenities = chips.length;

    // Ensure initial state is defined
    if (!btn.dataset.expanded) {
        btn.dataset.expanded = 'false';
    }

    const isExpanded = btn.dataset.expanded === 'true';

    chips.forEach((chip, index) => {
        if (index >= 5) {
            chip.classList.toggle('hidden', isExpanded);
        }
    });

    btn.dataset.expanded = isExpanded ? 'false' : 'true';
    btn.textContent = isExpanded
        ? `+${totalAmenities - 5} more`
        : 'Show less';
}