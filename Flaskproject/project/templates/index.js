function showContent(contentId) {
    // Hide all content sections
    var contentSections = document.getElementsByClassName('content-section');
    for (var i = 0; i < contentSections.length; i++) {
        contentSections[i].style.display = 'none';
    }

    // Show the selected content section
    document.getElementById(contentId).style.display = 'block';
}

function toggleDropdown(dropdownId) {
    var dropdownContent = document.getElementById(dropdownId + 'Dropdown');
    dropdownContent.classList.toggle('show');
}
function showContent(contentId) {
    // Hide all content sections
    var contentSections = document.getElementsByClassName('content-section');
    for (var i = 0; i < contentSections.length; i++) {
        contentSections[i].style.display = 'none';
    }

    // Show the selected content section
    document.getElementById(contentId).style.display = 'block';
}

function toggleDropdown(dropdownId) {
    var dropdownContent = document.getElementById(dropdownId + 'Dropdown');
    dropdownContent.classList.toggle('show');
}