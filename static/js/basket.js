window.onload = function () {
    $('.col-lg-5').on('click', 'input[type="number"]', function () {
        var t_href = event.target;
        var name = t_href.name          // item.id
        var value = t_href.value;       // item.quantity
        $.ajax({
            url: '/basket/edit/' + name + '/' + value + '/',
            success: function (data) {
                $('.col-lg-5').html(data.result);        // отрисовка страницы с полученными данными
            }
        });
        event.preventDefault();
    })
}
