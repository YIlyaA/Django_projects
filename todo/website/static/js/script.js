
var originalDescription = {};

// Enter edit mode
function editItem(itemId) {
    // Save the current description before editing
    originalDescription[itemId] = document.getElementById('description-input-' + itemId).value;

    // Hide description and show input field
    document.getElementById('description-text-' + itemId).style.display = 'none';
    document.getElementById('description-input-' + itemId).style.display = 'block';
    document.getElementById('description-input-' + itemId).style.fontFamily = 'inherit'; // Keep the same font

    // Hide edit button and show save/cancel buttons
    document.getElementById('edit-button-' + itemId).style.display = 'none';
    document.getElementById('save-button-' + itemId).style.display = 'inline';
    document.getElementById('back-button-' + itemId).style.display = 'inline';

    // Hide delete button during editing
    document.getElementById('delete-button-' + itemId).style.display = 'none';
}

function saveItem(itemId) {
    const newDescription = document.getElementById(`description-input-${itemId}`).value;

    fetch(`/main/update/${itemId}/`, {  // Verify this URL is correct
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({ description: newDescription }).toString()
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network or server error');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                document.getElementById(`description-text-${itemId}`).innerText = newDescription;
                document.getElementById(`description-text-${itemId}`).style.display = 'block';
                document.getElementById(`description-input-${itemId}`).style.display = 'none';
                document.getElementById(`edit-button-${itemId}`).style.display = 'inline';
                document.getElementById(`save-button-${itemId}`).style.display = 'none';
                document.getElementById(`back-button-${itemId}`).style.display = 'none';
                document.getElementById(`delete-button-${itemId}`).style.display = 'inline';
            } else {
                alert('Error updating item');
            }
        })
        .catch(error => {
            alert('Failed to save item');
        });
}



// Cancel the edit and revert to the original description
function cancelEdit(itemId) {
    // Revert the description input to its original value
    document.getElementById('description-input-' + itemId).value = originalDescription[itemId];

    // Hide input field and show description text
    document.getElementById('description-text-' + itemId).style.display = 'block';   // elemnt that display text, visible
    document.getElementById('description-input-' + itemId).style.display = 'none';   // elemnt used in edit mode, invisible

    // Switch buttons back to original state
    document.getElementById('edit-button-' + itemId).style.display = 'inline';
    document.getElementById('save-button-' + itemId).style.display = 'none';     // button 'save' invisible
    document.getElementById('back-button-' + itemId).style.display = 'none';     // button 'back' invisible

    // Show delete button again
    document.getElementById('delete-button-' + itemId).style.display = 'inline';
}

function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this item?")) {    // confirmation of deletion
        event.preventDefault();
    }
}

function confirmLogout(event) {
    // Show the confirmation dialog
    if (!confirm("Are you sure you want to logout?")) {
        // If the user clicks "Cancel," prevent the form submission
        event.preventDefault();
    } else {
        // Otherwise, submit the form if they clicked "OK"
        document.getElementById('logout-form').submit();
    }
}


function toggleComplete(itemId) {
    const checkbox = document.querySelector(`#item-${itemId} .completed-checkbox`);
    const status = checkbox.checked;

    // Toggle UI immediately
    const itemElement = document.getElementById(`item-${itemId}`);
    if (status) {
        itemElement.classList.add("completed");
        document.getElementById(`edit-button-${itemId}`).style.display = "none";
    } else {
        itemElement.classList.remove("completed");
        document.getElementById(`edit-button-${itemId}`).style.display = "inline-block";
    }

    // Send the status update to the server
    fetch(`/main/update-status/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ 'status': status })        
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert('Failed to update status');
            checkbox.checked = !status; // Revert checkbox if update failed
        }
    })
    .catch(error => console.error('Error updating status:', error));
}


