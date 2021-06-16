window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;
        var name = t_href.name          // item.id
        var value = t_href.value;       // item.quantity
        $.ajax({
            url: '/basket/edit/' + name + '/' + value + '/',
            success: function (data) {
                $('.basket_list').html(data.result);        // отрисовка страницы с полученными данными
            }
        });
        event.preventDefault();
    })
}
