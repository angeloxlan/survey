document.addEventListener('alpine:init', () => {
    Alpine.data('actions', () => ({
        editSurveySubmit() {
            const form = document.getElementById('edit-survey-form');
            form.submit();
        },
    }));
});
