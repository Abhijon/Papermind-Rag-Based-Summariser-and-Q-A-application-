// Q&A Functionality
document.addEventListener('DOMContentLoaded', () => {
    const askQuestionBtn = document.getElementById('askQuestionBtn');
    const questionInput = document.getElementById('questionInput');
    const answerResult = document.getElementById('answerResult');
    const qaProcessing = document.getElementById('qaProcessing');

    if (askQuestionBtn) {
        askQuestionBtn.addEventListener('click', async function () {
            const question = questionInput.value.trim();

            if (!question) {
                alert('Please enter a question');
                return;
            }

            // Show processing animation
            qaProcessing.classList.remove('hidden');
            askQuestionBtn.disabled = true;
            answerResult.innerHTML = 'Processing...';

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();

                if (data.success) {
                    let answerHTML = `<p>${data.answer}</p>`;

                    // Add sources if available
                    if (data.sources && data.sources.length > 0) {
                        answerHTML += '<div class="sources"><h4>Relevant Context:</h4>';
                        data.sources.forEach((source, index) => {
                            answerHTML += `<div class="source-item"><strong>Source ${index + 1}:</strong> ${source.substring(0, 200)}...</div>`;
                        });
                        answerHTML += '</div>';
                    }

                    answerResult.innerHTML = answerHTML;
                } else {
                    answerResult.innerHTML = `<p style="color: #ff4444;">${data.answer}</p>`;
                }
            } catch (error) {
                console.error('Error:', error);
                answerResult.innerHTML = `<p style="color: #ff4444;">Error: ${error.message}</p>`;
            } finally {
                qaProcessing.classList.add('hidden');
                askQuestionBtn.disabled = false;
            }
        });

        // Allow Enter key to submit question
        questionInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                askQuestionBtn.click();
            }
        });
    }
});

// Show Q&A section after PDF summary
window.showQASection = function () {
    document.getElementById('qaSection').style.display = 'block';
};
