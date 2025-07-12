const feedback = document.getElementById('feedback')
const form = document.getElementById('form')
const textarea = document.getElementById('message-input')
const lengthFeedback = document.getElementById('message-length-feedback');
const maxLength = textarea.getAttribute('maxlength');

function updateLengthFeedback() {
    const currentLength = textarea.value.length;
    lengthFeedback.textContent = `${currentLength}/${maxLength}`;
}

function clearErrors() {
    feedback.removeAttribute('class');
}

function hideFeedback() {
    feedback.classList.add('hidden')
    feedback.classList.remove('visible')
}

function showFeedback() {
    feedback.classList.remove('hidden')
    feedback.classList.add('visible')
}

function setup() {
    updateLengthFeedback()
}

form.addEventListener('input', () => {
    clearErrors()
    hideFeedback()
})

form.addEventListener('submit', function (event) {
    event.preventDefault()

    const form = event.target;
    const formData = new FormData(form);

    clearErrors()

    fetch(form.action, {
        method: form.method,
        body: formData
    })
        .then(response => {
            if (response.ok) {
                form.reset();
                feedback.classList.add('feedback-success')
                feedback.innerText = "Success!"
            } else {
                feedback.classList.add('feedback-error')
                feedback.innerText = "Failed to submit form!"
            }
        })
        .catch(error => {
            feedback.classList.add('feedback-error')
            feedback.textContent = "Network error."
        }).finally(() => {
            showFeedback()
        })
})

textarea.addEventListener('input', () => {
    updateLengthFeedback()
})

setup()