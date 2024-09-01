document.addEventListener("DOMContentLoaded", function() {
    const messageElement = document.getElementById("message");

    // Функция для получения значения куки по имени
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    }

    // Функция для удаления куки
    function deleteCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    }

    // Получаем значение куков
    const messageContent = getCookie('message');
    const messageType = getCookie('message_type');

    if (messageContent) {
        console.log(`Message: ${messageContent}`)
        messageElement.innerText = messageContent; // Декодированное значение уже
        messageElement.classList.add("alert");

        if (messageType === "success") {
            messageElement.classList.add("alert-success");
        } else if (messageType === "error") {
            messageElement.classList.add("alert-danger");
        }

        messageElement.style.display = 'block';

        // Удаляем куки после отображения сообщения
        deleteCookie('message');
        deleteCookie('message_type');
    }
});
