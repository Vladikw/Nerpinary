document.addEventListener('DOMContentLoaded', function() {
    const countdownElem = document.getElementById('countdown');
    if (!countdownElem) return;

    const countdownContainer = document.getElementById('countdown-text');
    const resendUrl = countdownContainer.getAttribute('data-resend-url');

    function parseTime(timeStr) {
        const parts = timeStr.split(':').map(Number);
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
    }

    let secondsLeft = parseTime(countdownElem.textContent);

    const timer = setInterval(function() {
        if (secondsLeft <= 0) {
            clearInterval(timer);
            countdownContainer.innerHTML = `
                <p>Не получили код?</p>
                <a href="${resendUrl}" class="resend-link">
                    <i class="fas fa-redo"></i> Отправить новый код
                </a>
            `;
            return;
        }

        secondsLeft--;
        const hours = Math.floor(secondsLeft / 3600);
        const minutes = Math.floor((secondsLeft % 3600) / 60);
        const seconds = secondsLeft % 60;

        countdownElem.textContent =
            `${hours.toString().padStart(2, '0')}:` +
            `${minutes.toString().padStart(2, '0')}:` +
            `${seconds.toString().padStart(2, '0')}`;
    }, 1000);
});