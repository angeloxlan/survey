document.addEventListener('alpine:init', () => {
    Alpine.data('actions', () => ({
        createSurveySubmit() {
            const form = document.getElementById('create-survey-form');
            form.submit();
        },
    }));
});
