/**
 * Creates a tag with specified details and appends it to a designated container.
 * This function also clears related search fields and suggestion elements.
 * 
 * @param {string} containerId - The ID of the container where the tag will be appended.
 * @param {string} searchFieldId - The ID of the search input field to be cleared after adding the tag.
 * @param {string} suggestionsId - The ID of the suggestions list to be cleared.
 * @param {string} name - The display name for the tag.
 * @param {string} id - The identifier associated with the tag, used for form submissions.
 * @param {string} inputName - The name attribute for the hidden input field to handle form submissions.
 */
function createTag(containerId, searchFieldId, suggestionsId, name, id, inputName) {
    const container = document.getElementById(containerId);
    const tag = document.createElement('span');
    tag.className = 'badge bg-primary me-2';
    tag.textContent = name + ' ';

    const removeIcon = document.createElement('i');
    removeIcon.className = 'fas fa-times';
    removeIcon.style.cursor = 'pointer';
    removeIcon.onclick = () => container.removeChild(tag);
    tag.appendChild(removeIcon);

    // Create a hidden input to store the identifier for form submission
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = inputName;
    hiddenInput.value = id;
    tag.appendChild(hiddenInput);

    container.appendChild(tag);

    // Clear any existing text in the search field and remove any existing suggestions
    document.getElementById(searchFieldId).value = '';
    document.getElementById(suggestionsId).innerHTML = '';
}

/**
 * Convenience function for adding a teacher tag.
 * Wraps the createTag function specifically for teacher tags.
 *
 * @param {string} name - The name of the teacher.
 * @param {string} id - The unique identifier of the teacher.
 */
function addTeacherTag(name, id) {
    createTag('selectedTeachers', 'teacherSearch', 'teacherNameSuggestions', name, id, 'teacherIds[]');
}

/**
 * Convenience function for adding a presenter tag.
 * Wraps the createTag function specifically for presenter tags.
 *
 * @param {string} name - The name of the presenter.
 * @param {string} id - The unique identifier of the presenter.
 */
function addPresenterTag(name, id) {
    createTag('selectedPresenters', 'presenterSearch', 'presenterNameSuggestions', name, id, 'presenterIds[]');
}

/**
 * Event listener to clear suggestion lists when clicking outside of search fields.
 * This ensures that suggestion lists are hidden when they are no longer needed.
 */
document.addEventListener('click', function(event) {
    // Array of search field IDs to check against the click target
    ['teacherSearch', 'presenterSearch'].forEach(searchFieldId => {
        const searchField = document.getElementById(searchFieldId);
        if (searchField && !searchField.contains(event.target)) {
            // Determine which suggestions list to clear based on the search field
            const suggestionsId = searchFieldId === 'teacherSearch' ? 'teacherNameSuggestions' : 'presenterNameSuggestions';
            document.getElementById(suggestionsId).innerHTML = '';
        }
    });
});
