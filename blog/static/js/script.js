function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this item?")) {    // confirmation of deletion
        event.preventDefault();
    }
}

function confirmLogout(event) {
    if (!confirm("Are you sure you want to logout?")) {    // confirmation of deletion
        event.preventDefault();
    }
}

function confirmUpdateProfile(event) {
    if (!confirm("Are you sure you want to update profile?")) {    // confirmation of deletion
        event.preventDefault();
    }
}