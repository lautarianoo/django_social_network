let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
$('.add-friend').click(function () {

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        }
    });

    $(this).text('Request Sent');

    let url = $(this).data('url');

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        success: function (res) {
            if (res.status === false) {
            }
            if (res.status === true) {
                // $('.add-friend').text('Request Sent');
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
});

function accept(li) {
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        }
    });

    let friend = $(li).data('friend');

    let url = `/accept-request/${friend}`;

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        success: function (res) {
            if (res.status === false) {
            }
            if (res.status === true) {

            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}

let friendRequestNotificationSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host +
    '/ws/friend-request-notification/');

friendRequestNotificationSocket.onopen = function (e) {
    fetchFriendRequests();
};

function fetchFriendRequests() {
    friendRequestNotificationSocket.send(JSON.stringify({'command': 'fetch_notifications'}));
}

function createNotification(notification) {
    let single = ``;
    $('#friend-menu').prepend(single);
}

friendRequestNotificationSocket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    if (data['command'] === 'notifications') {
        let notifications = JSON.parse(data['notifications']);
        $('#total-friend-notifications').text(notifications.length);
        for (let i = 0; i < notifications.length; i++) {
            createNotification(notifications[i]);
        }
    } else if (data['command'] === 'new_notification') {
        let notification = $('#total-friend-notifications');
        notification.text(parseInt(notification.text() + 1));
        createNotification(JSON.parse(data['notification']));
    }
};


// like and comment notification
let newCommentNotificationSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host +
    '/ws/new-comment-notification/');


function fetchNotifications() {
    newCommentNotificationSocket.send(JSON.stringify({'command': 'fetch_notifications'}));
}

function createNewCommentNotification(notification) {
    let single = ``;
    $('#new-comment-menu').prepend(single);
}

newCommentNotificationSocket.onopen = function (e) {
    fetchNotifications();
};

newCommentNotificationSocket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    if (data['command'] === 'notifications') {
        let notifications = JSON.parse(data['notifications']);
        $('#total-new-comment-notifications').text(notifications.length);
        for (let i = 0; i < notifications.length; i++) {
            createNewCommentNotification(notifications[i]);
        }
    } else if (data['command'] === 'new_comment_notification') {
        let notification = $('#total-new-comment-notifications');
        notification.text(parseInt(notification.text()) + 1);
        createNewCommentNotification(JSON.parse(data['notification']));
    }
};

$('#mark-new-comment-notifications-as-read').click(function () {

    let url = $(this).data('url');

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        }
    });

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        success: function (res) {
            console.log(res);
            if (res.status === false) {
            }
            if (res.status === true) {}

        },
        error: function (err) {
            console.log(err);
        }
    });
});