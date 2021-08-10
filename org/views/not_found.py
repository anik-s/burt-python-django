from django.shortcuts import render


def not_found(request, exception):
    return render(request, 'common/404.html', {'page': '404'})