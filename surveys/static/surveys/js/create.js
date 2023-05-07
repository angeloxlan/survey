document.addEventListener('alpine:init', () => {
    Alpine.data('form', () => ({
        questionsCount: 0,
        addQuestion() {
            const questionContainer = this.$refs['question-form-container'].cloneNode(true);
            const questionsContainer = this.$refs['questions-container'];
            const optionsList = questionContainer.querySelector('ul.options-list')
            questionContainer.removeAttribute('x-ref');
            questionContainer.classList.remove('placeholder');
            this.updateOptionsIds(optionsList);
            this.$refs['questions-container'].appendChild(questionContainer);
            this.updateQuestionsIds(questionsContainer);
        },
        deleteQuestion() {
            const questionContainer = this.$event.target.closest('.question-form-container');
            const questionsContainer = this.$event.target.closest('.questions-container');
            questionContainer.remove();
            this.updateQuestionsIds(questionsContainer);
        },
        updateQuestionsIds(questionsContainer) {
            const questions = questionsContainer
                .querySelectorAll('.question-form-container:not(.placeholder)');
            questions.forEach((question, index) => {
                const formtags = question.querySelectorAll('label,input');
                formtags.forEach(element => {
                    if (element.tagName.toLowerCase() == 'input') {
                        const id = element.id;
                        const name = element.name;
                        const idUpdated = id.replace(/question_set-[\d|__q_prefix__]*-/g, `question_set-${index}-`)
                        const nameUpdated = name.replace(/question_set-[\d|__q_prefix__]*-/g, `question_set-${index}-`)
                        element.id = idUpdated;
                        element.name = nameUpdated;
                    } else {
                        const label = element.getAttribute('for');
                        if (!label) return;
                        const labelUpdated = label.replace(/question_set-[\d|__q_prefix__]*-/g, `question_set-${index}-`);
                        element.setAttribute('for', labelUpdated);
                    }
                });
                // question.innerHTML = question.innerHTML
                //     .replace(/question_set-[\d|__q_prefix__]*-/g, `question_set-${index}-`);
            });
            this.updateTotalQuestionsInput(questions.length);
        },
        addOption() {
            const questionsContainer = this.$refs['questions-container'];
            const optionsList = this.$event.target.previousElementSibling;
            const optionItem = this.$refs['option-item'].cloneNode(true);
            const totalOptions = optionsList.querySelectorAll('li');
            const optionIdx = totalOptions.length;
            optionItem.removeAttribute('x-ref')
            optionItem.innerHTML = optionItem.innerHTML
                .replace(/__o_prefix__/g, optionIdx)
            optionsList.appendChild(optionItem);
            this.updateQuestionsIds(questionsContainer);
            this.updateOptionsIds(optionsList);
        },
        deleteOption() {
            const li = this.$event.target.closest('li');
            const optionsList = this.$event.target.closest('.options-list');
            li.remove();
            this.updateOptionsIds(optionsList);
        },
        updateOptionsIds(optionsList) {
            const options = optionsList.querySelectorAll('li.option-item');
            options.forEach((liOption, index) => {
                const formtags = liOption.querySelectorAll('label,input');
                formtags.forEach(element => {
                    if (element.tagName.toLowerCase() == 'input') {
                        const id = element.id;
                        const name = element.name;
                        const idUpdated = id.replace(/option_set-[\d|__o_prefix__]*-/g, `option_set-${index}-`)
                        const nameUpdated = name.replace(/option_set-[\d|__o_prefix__]*-/g, `option_set-${index}-`)
                        element.id = idUpdated;
                        element.name = nameUpdated;
                    } else {
                        const label = element.getAttribute('for');
                        const labelUpdated = label.replace(/option_set-[\d|__o_prefix__]*-/g, `option_set-${index}-`)
                        element.setAttribute('for', labelUpdated);
                    }
                });
                // liOption.innerHTML = liOption.innerHTML
                //     .replace(/option_set-[\d|__o_prefix__]*-/g, `option_set-${index}-`)
            });
            this.updateTotalOptionsInput(optionsList, options.length);
        },
        updateTotalQuestionsInput(total) {
            const inputTotalQuestions = document.getElementById('id_question_set-TOTAL_FORMS');
            inputTotalQuestions.value = total;
        },
        updateTotalOptionsInput(optionsContainer, total) {
            const inputTotalOptions = optionsContainer.querySelector('[id$="TOTAL_FORMS"]')
            if (!inputTotalOptions) return;
            inputTotalOptions.value = total;
        },
    }));
});

document.addEventListener('alpine:init', () => {
    Alpine.data('actions', () => ({
        createSurveySubmit() {
            const form = document.getElementById('create-survey-form');
            form.submit();
        },
    }));
});
