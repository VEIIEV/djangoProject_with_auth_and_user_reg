const url = '{% url "images:like" %}';
var options = {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
}
document.querySelector('a.like')
    .addEventListener('click', function (e) {
        e.preventDefault();
        var likeButton = this;

        // добавить тело запроса
        var formData = new FormData();
        formData.append('id', likeButton.dataset.id);
        formData.append('action', likeButton.dataset.action);
        options['body'] = formData;
        // отправить HTTP-запрос
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if (data['status'] === 'ok') {
                    var previousAction = likeButton.dataset.action;
                    // переключить текст кнопки и атрибут data-action
                    var action = previousAction === 'like' ? 'unlike' : 'like';
                    likeButton.dataset.action = action;
                    likeButton.innerHTML = action;
                    // обновить количество лайков
                    var likeCount = document.querySelector('span.count .total');
                    var totalLikes = parseInt(likeCount.innerHTML);
                    likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
                }
            })
    });


var page = 1;
var emptyPage = false;
var blockRequest = false;
window.addEventListener('scroll', function (e) {
    var margin = document.body.clientHeight – window.innerHeight – 200;
    if (window.pageYOffset > margin && !emptyPage && !blockRequest) {
        blockRequest = true;
        page += 1;
        fetch('?images_only=1&page=' + page)
            .then(response => response.text())
            .then(html => {
                if (html === '') {
                    emptyPage = true;
                } else {
                    var imageList = document.getElementById('image-list');
                    imageList.insertAdjacentHTML('beforeEnd', html);
                    blockRequest = false;
                }
            })
    }
});
// Запустить события прокрутки
const scrollEvent = new Event('scroll');
window.dispatchEvent(scrollEvent);