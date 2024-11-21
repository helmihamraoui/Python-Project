document.addEventListener('DOMContentLoaded', function () {
    const questionButtons = document.querySelectorAll('.question-btn');
    const chatBox = document.getElementById('chat-box');

    questionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const question = button.dataset.question;

            // Append user's question to the chatbox
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = question;
            chatBox.appendChild(userMessage);

            // Send the question to the backend
            fetch('/get-response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            })
            .then(response => response.json())
            .then(data => {
                // Append chatbot's response to the chatbox
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot';
                botMessage.textContent = data.response;
                chatBox.appendChild(botMessage);

                // Scroll to the bottom of the chatbox
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(() => {
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message bot';
                errorMessage.textContent = 'Error retrieving the response.';
                chatBox.appendChild(errorMessage);

                // Scroll to the bottom of the chatbox
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        });
    });
});
