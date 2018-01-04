$(document).ready(function() {
    $('.down').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 0 : count;
        $input.val(count);
        $input.change();

        var a1 = parseInt( document.getElementById('am1').value);
        var a2 = parseInt( document.getElementById('am2').value);
        var a3 = parseInt( document.getElementById('am3').value);
        var sum = a1 + a2 + a3;

        if(sum == 1) document.getElementById('ressum').value = sum + " пассажир" + ", " + $('input[name=status]:checked').val();
        if(sum > 1) document.getElementById('ressum').value = sum + " пассажира" + ", " + $('input[name=status]:checked').val();
        if(sum == 0 || sum > 4) document.getElementById('ressum').value = sum + " пассажиров" + ", " + $('input[name=status]:checked').val();

        return false;
    });
    $('.up').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        var count = parseInt($input.val());
        $input.change();

        var a1 = parseInt( document.getElementById('am1').value);
        var a2 = parseInt( document.getElementById('am2').value);
        var a3 = parseInt( document.getElementById('am3').value);
        var sum = a1 + a2 + a3;

        if(a1 == 1) document.getElementById('ressum').value = sum + " пассажир" + ", " + $('input[name=status]:checked').val();
        if(sum > 1 ) document.getElementById('ressum').value = sum + " пассажира" + ", " + $('input[name=status]:checked').val();
        if(sum == 0 || sum > 4) document.getElementById('ressum').value = sum + " пассажиров" + ", " + $('input[name=status]:checked').val();

        return false;
    });

    $('.down1').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 0 ? 1 : count;
        $input.val(count);
        $input.change();

        var a4 = parseInt( document.getElementById('am4').value);
        var a5 = parseInt( document.getElementById('am5').value);
        var a6 = parseInt( document.getElementById('am6').value);
        var sum = a4 + a5 + a6;

        if(sum == 1){
            document.getElementById('ressum1').value = sum + " гость";
        }
        else{
            document.getElementById('ressum1').value = sum + " гостя";
        }
        return false;
    });

    $('.up1').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        var count = parseInt($input.val());
        $input.change();

        var a4 = parseInt( document.getElementById('am4').value);
        var a5 = parseInt( document.getElementById('am5').value);
        var a6 = parseInt( document.getElementById('am6').value);
        var sum = a4 + a5 + a6;

        if(sum == 1){
            document.getElementById('ressum1').value = sum + " гость";
        }
        else{
            document.getElementById('ressum1').value = sum + " гостей";
        }
        return false;
    });
    $('#status1').click(function () {
        document.getElementById('ressum').value = document.getElementById('ressum').value.slice(0,-8) + ", " + document.getElementById('status1').value;

    });
    $('#status2').click(function () {
        document.getElementById('ressum').value = document.getElementById('ressum').value.slice(0,-8) + ", " + document.getElementById('status2').value;

    });

    $('#search').click(function () {
        if (document.getElementById('select1').value.length < 2) {
            UIkit.notification('Вы забыли ввести пункт отправления', 'danger');
        }
        if (document.getElementById('select2').value.length < 2) {
            UIkit.notification('Вы забыли ввести пункт прибытия', 'danger');
        }
        if (document.getElementById('from_date').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату отправления', 'danger');
        }
        if (document.getElementById('to_date').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату прибытия', 'danger');
        }
        if (document.getElementById('select1').value == document.getElementById('select2').value) {
            UIkit.notification('Пункт отправления равен пункту прибытия', 'danger');
            return false;
        }
        if (parseInt( document.getElementById('am1').value) +
            parseInt( document.getElementById('am2').value) +
            parseInt( document.getElementById('am3').value) == 0 ) {
            UIkit.notification('Нулевое число пассажиров. Необходим хотя бы один пассажир.', 'danger');
            return false;
        }

    });
    $('#search1').click(function () {
        if (document.getElementById('select3').value.length < 2) {
            UIkit.notification('Вы забыли ввести название города/отеля', 'danger');
        }
        if (document.getElementById('from_date1').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату заезда', 'danger');
        }
        if (document.getElementById('to_date1').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату выезда', 'danger');
        }
        var a4 = parseInt( document.getElementById('am4').value);
        var a5 = parseInt( document.getElementById('am5').value);
        var a6 = parseInt( document.getElementById('am6').value);
        var sum = a4 + a5 + a6;
        if (sum == 0 ) {
            UIkit.notification('Нулевое число гостей. Необходим хотя бы один гость.', 'danger');
            return false;
        }

    });
    $('#search2').click(function () {
        if (document.getElementById('select4').value.length < 2) {
            UIkit.notification('Вы забыли ввести место получения авто', 'danger');
        }
        if (document.getElementById('select5').value.length < 2) {
            UIkit.notification('Вы забыли ввести место возврата авто', 'danger');
        }
        if (document.getElementById('from_date2').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату получения авто', 'danger');
        }
        if (document.getElementById('to_date2').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату возврата авто', 'danger');
        }

    });

    var today = new Date();

    list_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    list_months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
     'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    list_short_months = ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль',
    'Авг', 'Сен', 'Окт', 'Нояб', 'Дек'];
    str_today = 'Сегодня';
    str_now = 'Сейчас';
    type_date = 'date';
    min_date = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    max_date = new Date(today.getFullYear(), today.getMonth(), today.getDate()+180);
    first_day = 1;
    my_text={
      days: list_days,
      months: list_months,
      monthsShort: list_short_months,
      today: str_today,
      now: str_now,
    };

    $('#rangestart').calendar({
        minDate: min_date,
        maxDate: max_date,
        type: type_date,
        endCalendar: $('#rangeend'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,

    });
    $('#rangeend').calendar({
        maxDate: max_date,
        type: type_date,
        startCalendar: $('#rangestart'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,
    });

    $('#rangestart1').calendar({
        minDate: min_date,
        maxDate: max_date,
        type: type_date,
        endCalendar: $('#rangeend1'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,

    });
    $('#rangeend1').calendar({
        maxDate: max_date,
        type: type_date,
        startCalendar: $('#rangestart1'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,
    });

    $('#rangestart2').calendar({
        minDate: min_date,
        maxDate: max_date,
        endCalendar: $('#rangeend2'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,
        ampm: false,

    });
    $('#rangeend2').calendar({
        maxDate: max_date,
        startCalendar: $('#rangestart2'),
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,
        ampm: false,
    });

    $('#date').calendar({
        type: type_date,
        maxDate: min_date,
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();
                return day + '.' + month + '.' + year;
            }
        },
        text: my_text,
        firstDayOfWeek: first_day,
    });

    $('#select1')
      .dropdown()
    ;
    $('#select2')
      .dropdown()
    ;
    $('#select3')
      .dropdown()
    ;
    $('#select4')
      .dropdown()
    ;
    $('#select5')
      .dropdown()
    ;

    $('#login_form').submit(function() {
    if (document.getElementById('login').value.length < 2 || document.getElementById('password').value.length < 2) {
        if (document.getElementById('login').value.length < 2) {
            UIkit.notification('Вы забыли ввести логин', 'danger');
        }
        if (document.getElementById('password').value.length < 2) {
            UIkit.notification('Вы забыли ввести пароль', 'danger');
        }
        return false;
    }
    });

    $('#reg_form').submit(function() {

    if ((document.getElementById('name').value.length < 2) || 
        (document.getElementById('lastname').value.length < 2) ||
        (document.getElementById('email').value.length < 2 )||
        (document.getElementById('password').value.length < 2 )||
        (document.getElementById('input_date').value.length < 2 )||
        (document.getElementById('password').value != document.getElementById('password1').value)){

        if (document.getElementById('name').value.length < 2) {
            UIkit.notification('Вы забыли ввести имя', 'danger');
        }

        if (document.getElementById('lastname').value.length < 2) {
            UIkit.notification('Вы забыли ввести фамилию', 'danger');
        }

        if (document.getElementById('email').value.length < 2) {
            UIkit.notification('Вы забыли ввести Email', 'danger');
        }

        if (document.getElementById('sex').value != 'man' || document.getElementById('sex').value != 'woman') {
            UIkit.notification('Вы забыли указать пол', 'danger');
        }

        if (document.getElementById('input_date').value.length < 2) {
            UIkit.notification('Вы забыли ввести дату рождения', 'danger');
        }

        if (document.getElementById('password').value.length < 8) {
            UIkit.notification('Количество символов в пароле должно быть более 7', 'danger');
        }

        if (document.getElementById('password').value != document.getElementById('password1').value) {
            UIkit.notification('Пароли НЕ одинаковые!', 'danger');
        }
        
        return false;
    }
    });
});
