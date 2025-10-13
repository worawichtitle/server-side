// Filter functionality
const filterRadios = document.querySelectorAll('input[name="a_filter"]');
const searchInput = document.getElementById('search');

function updateURL() {
    const selectedFilter = document.querySelector('input[name="a_filter"]:checked').value;
    const searchValue = searchInput ? searchInput.value : '';
    
    const params = new URLSearchParams();
    if (searchValue) params.set('search', searchValue);
    if (selectedFilter && selectedFilter !== 'datetime') params.set('filter', selectedFilter);
    
    const newURL = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.location.href = newURL;
}

filterRadios.forEach(radio => {
    radio.addEventListener('change', updateURL);
});

if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            updateURL();
        }
    });
}
