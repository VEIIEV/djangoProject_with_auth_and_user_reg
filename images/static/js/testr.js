const url = '{% url "user_follow" %}';
var options = {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
}
document.querySelector('a.follow')
    .addEventListener('click', function (e) {
        e.preventDefault();
        var followButton = this;
        // добавить тело запроса
        var formData = new FormData();
        formData.append('id', followButton.dataset.id);
        formData.append('action', followButton.dataset.action);
        options['body'] = formData;
        // отправить HTTP-запрос
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if (data['status'] === 'ok') {
                    var previousAction = followButton.dataset.action;
                    // переключить текст кнопки и data-action
                    var action = previousAction === 'follow' ? 'unfollow' : 'follow';
                    followButton.dataset.action = action;
                    followButton.innerHTML = action;
                    // обновить количество подписчиков
                    var followerCount = document.querySelector('span.count .total');
                    var totalFollowers = parseInt(followerCount.innerHTML);
                    followerCount.innerHTML = previousAction === 'follow' ? totalFollowers + 1 : totalFollowers - 1;
                }
            })
    });