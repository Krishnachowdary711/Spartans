// Confirm before deleting an account, transaction, or category
document.querySelectorAll('.btn-danger').forEach(button => {
    button.addEventListener('click', function (event) {
        if (!confirm('Are you sure you want to delete this transaction?')) {
            event.preventDefault();
        }
    });
});

// Show alerts for success messages (optional)
setTimeout(() => {
    const alertBox = document.querySelector('.alert');
    if (alertBox) {
        alertBox.remove();
    }
}, 3000);

document.querySelectorAll('.btn-danger').forEach(button => {
    button.addEventListener('click', function (event) {
        if (!confirm('Are you sure you want to delete this account?')) {
            event.preventDefault();
        }
    });
});