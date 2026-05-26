document.addEventListener('DOMContentLoaded', function() {
    const amountInput = document.querySelector('input[name="amount"]');
    const incomeInput = document.querySelector('input[name="monthly_income"]');
    const expenseInput = document.querySelector('input[name="monthly_expense"]');
    
    if (amountInput && incomeInput) {
        function calculateRatios() {
            const amount = parseFloat(amountInput.value) || 0;
            const income = parseFloat(incomeInput.value) || 0;
            const expense = parseFloat(expenseInput.value) || 0;
            
            if (income > 0) {
                const dti = (expense / income * 100).toFixed(1);
                const lti = (amount / (income * 12) * 100).toFixed(1);
                
                let dtiDisplay = document.getElementById('dti-display');
                let ltiDisplay = document.getElementById('lti-display');
                
                if (dtiDisplay) dtiDisplay.textContent = dti + '%';
                if (ltiDisplay) ltiDisplay.textContent = lti + '%';
            }
        }
        
        if (amountInput) amountInput.addEventListener('input', calculateRatios);
        if (incomeInput) incomeInput.addEventListener('input', calculateRatios);
        if (expenseInput) expenseInput.addEventListener('input', calculateRatios);
    }
    
    const statusSelect = document.querySelector('select[name="status"]');
    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            const rejectionReason = document.getElementById('rejection-reason');
            if (rejectionReason) {
                rejectionReason.style.display = this.value === 'rejected' ? 'block' : 'none';
            }
        });
    }
    
    const forms = document.querySelectorAll('form[method="post"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });
    
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                const fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
                const nextSibling = this.nextElementSibling;
                if (nextSibling && nextSibling.classList.contains('text-muted')) {
                    nextSibling.textContent = fileName + ' (' + fileSize + ' MB)';
                }
            }
        });
    });
});