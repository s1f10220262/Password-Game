document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-game-button');

    startButton.addEventListener('click', async () => {
        const selectedQuizFile = document.querySelector('input[name="quiz-option"]:checked').value;

        try {
            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quiz_file: selectedQuizFile })
            });

            const result = await response.json();

            alert(result.message);
        } catch (error) {
            console.error('Error:', error);
            alert('ゲームの起動中にエラーが発生しました。');
        }
    });
});
