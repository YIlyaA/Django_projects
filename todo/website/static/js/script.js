
// Function to enter the editing mode
function editItem(itemId) {
// Hide the current description and show the input field
document.getElementById('description-text-' + itemId).style.display = 'none';
document.getElementById('description-input-' + itemId).style.display = 'block';


// Hide the delete button during editing
document.getElementById('delete-form-' + itemId).style.display = 'none';
document.getElementById('update-form-' + itemId).style.display = 'none';
}

// Function to save the edited item
function saveItem(itemId) {
// Get the new description from the input field
var newDescription = document.getElementById('description-input-' + itemId).value;

// Send an AJAX request to update the item
fetch(`/main/update/${itemId}/`, {
    method: 'POST',
    headers: {
    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    'Content-Type': 'application/json'
    },
    body: JSON.stringify({
    'description': newDescription
    })
}).then(response => response.json())
    .then(data => {
    if (data.success) {
        // Update the displayed description and hide the input field
        document.getElementById('description-text-' + itemId).innerText = newDescription;
        document.getElementById('description-input-' + itemId).style.display = 'none';
        document.getElementById('description-text-' + itemId).style.display = 'block';

        // Show the edit button and hide the save button
        document.getElementById('edit-button-' + itemId).style.display = 'inline';
        document.getElementById('save-button-' + itemId).style.display = 'none';

        // Show the delete button again
        document.getElementById('delete-form-' + itemId).style.display = 'inline';
    }
    });
}

