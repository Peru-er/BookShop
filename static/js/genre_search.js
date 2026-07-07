
document.getElementById('genre-search').addEventListener('input', function() {
    let filter = this.value.toLowerCase();
    let items = document.querySelectorAll('#genres-list .genre-item');

    items.forEach(function(item) {
        let genreName = item.querySelector('.genre-name').textContent.toLowerCase();
        if (genreName.includes(filter)) {
            item.style.setProperty('display', 'block', 'important');
        } else {
            item.style.setProperty('display', 'none', 'important');
        }
    });
});
