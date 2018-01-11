from django.shortcuts import render, get_list_or_404, get_object_or_404
from currency.models import ValutaValue, Valuta


# Create your views here.
def currency_home(request):
    all_valuta = Valuta.objects.all()
    return render(request, 'currency/currency_home.html', {'all_valuta': all_valuta})


def currency_values(request, code):
    valuta = get_object_or_404(Valuta, char_code=code)
    values = get_list_or_404(ValutaValue, valuta=Valuta.objects.get(char_code=code))

    values = values[::-1]  # по возрастанию дат. Требование поставщика графика
    last_values = values[::-1][:10]  # для оптимизации запросов снова переворачиваем и выделяем 10 крайних
    return render(request, 'currency/currency_values.html', {'values': values,
                                                             'valuta': valuta,
                                                             'last_values': last_values})


def currency_valuta_info(request, code):
    valuta = get_object_or_404(Valuta, char_code=code)
    return render(request, 'currency/currency_info.html', {'valuta': valuta})