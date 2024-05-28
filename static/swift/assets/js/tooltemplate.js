document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('toolTemplateForm');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert(data.message);
                // Optionally, you can redirect or update the page content here
            } else {
                // Handle validation errors
                const formErrors = data.form_errors;
                const inpFormErrors = data.inp_form_errors;
                
                // Clear existing error messages
                const errorElements = document.querySelectorAll('.errorlist');
                errorElements.forEach(el => el.remove());
                
                // Display new error messages
                for (const [field, errors] of Object.entries(formErrors)) {
                    const fieldElement = document.querySelector(`[name=${field}]`);
                    if (fieldElement) {
                        const errorList = document.createElement('ul');
                        errorList.classList.add('errorlist');
                        errors.forEach(error => {
                            const errorItem = document.createElement('li');
                            errorItem.textContent = error;
                            errorList.appendChild(errorItem);
                        });
                        fieldElement.parentElement.appendChild(errorList);
                    }
                }
                
                for (const [field, errors] of Object.entries(inpFormErrors)) {
                    const fieldElement = document.querySelector(`[name=${field}]`);
                    if (fieldElement) {
                        const errorList = document.createElement('ul');
                        errorList.classList.add('errorlist');
                        errors.forEach(error => {
                            const errorItem = document.createElement('li');
                            errorItem.textContent = error;
                            errorList.appendChild(errorItem);
                        });
                        fieldElement.parentElement.appendChild(errorList);
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});