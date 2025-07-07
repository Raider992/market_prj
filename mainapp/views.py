from django.shortcuts import render, get_object_or_404
from .models import Accommodation

def main(request):
    return render(request, 'mainapp/index.html')

def accommodations(request):
    title = 'отели'

    list_of_accommodations = Accommodation.objects.filter(is_active=True)

    context = {
        'title':title,
        'list_of_accommodations':list_of_accommodations
    }

    return render(request, 'mainapp/accommodations.html', context)


def accommodation(request, pk):
    title = 'отель'

    context = {
        'title':title,
        'accommodation': get_object_or_404(Accommodation, pk=pk),
    }

    return render(request, 'mainapp/accommodation_details.html', context)
