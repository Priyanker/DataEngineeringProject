// Function to open a modal dialog
function openModal(movieId) {
    var modal = document.getElementById('modal-' + movieId);
    modal.style.display = "block";
}

// Function to close the modal dialog
function closeModal(movieId) {
    var modal = document.getElementById('modal-' + movieId);
    modal.style.display = "none";
}

// Close modal when clicking anywhere outside of the modal
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}

function scrollToGenre(genreId) {
    const element = document.getElementById(genreId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}