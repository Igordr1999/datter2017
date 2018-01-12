from django.shortcuts import render, get_list_or_404, get_object_or_404
from currency.models import ValutaValue, Valuta
from currency.forms import ConverterForm

# Create your views here.
def currency_home(request):
    all_valuta = Valuta.objects.all()
    popular_valuta = Valuta.objects.filter(popular=True)
    unpopular_valuta = Valuta.objects.filter(popular=False)
    all_last_values = []
    for i in all_valuta:
        code = i.char_code
        value = ValutaValue.objects.filter(valuta__char_code=code).first()
        all_last_values.append(value)
    context = dict(pairs=zip(all_valuta, all_last_values))
    return render(request, 'currency/currency_home.html', {"context": context,
                                                           "popular_valuta": popular_valuta,
                                                           "unpopular_valuta": unpopular_valuta,
                                                           "all_valuta": all_valuta})


def currency_values(request, code):
    valuta = get_object_or_404(Valuta, char_code=code)
    values = get_list_or_404(ValutaValue, valuta=Valuta.objects.get(char_code=code))

    values = values[::-1]  # по возрастанию дат. Требование поставщика графика
    last_values = values[::-1][:10]  # для оптимизации запросов снова переворачиваем и выделяем 10 крайних

    all_valuta = Valuta.objects.all()
    popular_valuta = Valuta.objects.filter(popular=True)
    unpopular_valuta = Valuta.objects.filter(popular=False)
    return render(request, 'currency/currency_values.html', {'values': values,
                                                             'valuta': valuta,
                                                             'last_values': last_values,
                                                            "popular_valuta": popular_valuta,
                                                           "unpopular_valuta": unpopular_valuta,
                                                           "all_valuta": all_valuta})


def currency_valuta_info(request, code):
    valuta = get_object_or_404(Valuta, char_code=code)

    all_valuta = Valuta.objects.all()
    popular_valuta = Valuta.objects.filter(popular=True)
    unpopular_valuta = Valuta.objects.filter(popular=False)
    return render(request, 'currency/currency_info.html', {'valuta': valuta,
                                                           "popular_valuta": popular_valuta,
                                                           "unpopular_valuta": unpopular_valuta,
                                                           "all_valuta": all_valuta})


def currency_converter(request):
    all_valuta = Valuta.objects.all()
    popular_valuta = Valuta.objects.filter(popular=True)
    unpopular_valuta = Valuta.objects.filter(popular=False)
    if request.method == "POST":
        form = ConverterForm(request.POST)
        if form.is_valid():
            valuta_from = form.cleaned_data['valuta_from']
            valuta_to = form.cleaned_data['valuta_to']
            value_from = form.cleaned_data['value_from']
            cur_from = ValutaValue.objects.filter(valuta__name_ru=valuta_from).first().value
            cur_to = ValutaValue.objects.filter(valuta__name_ru=valuta_to).first().value
            answer = round(cur_from/cur_to * value_from, 2)
            return render(request, 'currency/currency_converter.html', {'form': form,
                                                                        "answer": answer,
                                                           "popular_valuta": popular_valuta,
                                                           "unpopular_valuta": unpopular_valuta,
                                                           "all_valuta": all_valuta})
        else:
            return render(request, 'currency/currency_converter.html', {'form': form, "too": "Форма некорректна"})
    else:
        form = ConverterForm()
        return render(request, 'currency/currency_converter.html', {'form': form,
                                                                    "popular_valuta": popular_valuta,
                                                                    "unpopular_valuta": unpopular_valuta,
                                                                    "all_valuta": all_valuta})
