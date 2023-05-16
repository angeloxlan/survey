document.addEventListener('alpine:init', () => {
    Alpine.data('actions', () => ({
        submitFilters() {
            const form = document.getElementById('form-filters');
            form.submit();
        },
    }));
});
