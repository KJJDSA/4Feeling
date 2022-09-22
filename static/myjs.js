function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
        //parseInt는 파라미터 안을 정수로 바꿔주는 파이썬 함수같은 거구나.
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}
function listing(username) {

    if (username==undefined) {
        username=""
        //유저네임이 없으면 유저네임을 공란으로
    }
    $("#cards-box").empty()
    $.ajax({
        type:'GET',
        url:`/sad_get?username_give=${username}`,
        data: {},
        success:function(response) {
            console.log(response)
            let rows = response['posts']
            for (let i = 0; i < rows.length; i++){
                let post = rows[i]
                let time_post = new Date(post["date"])

                let url = rows[i]['url'].split('watch?v=')[1]
                let title = rows[i]['title']
                let feeling = rows[i]['feeling']
                let comment = rows[i]['comment']
                let time_before = time2str(time_post)
                let temp_html = `<div class="col">
                                    <div class="card">
                                            <a class="image is-48x48" href="/user/${post['username']}">
                                                <img class="is-rounded" src="{{ url_for('static', filename=user_info.profile_pic_real) }}"
                                                     alt="Image">
                                            </a>
                                        </div>
                                        <div class="media-content">
                                            <div class="content">
                                            <p><strong>${post['profile_name']}</strong> <small>${time_before}</small></p>
                                        </div>
                                        <div class="ratio ratio-16x9">
                                          <iframe src="https://www.youtube.com/embed/${url}" title="YouTube video" allowfullscreen></iframe>
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title">${feeling}</h5>
                                            <p class="card-text">${comment}</p>
                                            <p class="card-text"><small class="text-muted">${title}</small></p>
                                        </div>
                                        
                                    </div>
                                </div>`;

                $('#cards-box').prepend(temp_html)
            }
        }
    });

}


function posting() {

    let url = $('#url').val()
    let feeling = $('#inputGroupSelect01').val()
    let comment = $('#floatingTextarea2').val()
    let today = new Date().toISOString()
    if (url == "") {
        return alert('url을 입력해주세요')
    }
    if (feeling == "-- 선택하기 --") {
        return alert('기분을 선택해주세요.')
    }
    if (comment == "") {
        return alert('코멘트를 입력해주세요.')
    }
    else {
        $.ajax({
        type: 'POST',
        url: '/posting',
        data: {
            'url_give': url,
            'feeling_give': feeling,
            'comment_give': comment,
            'date_give': today
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload() //새로고침
        }
    });
    }


}

function open_box() {
    $('#post-box').show()
}

function close_box() {
    $('#post-box').hide()
}