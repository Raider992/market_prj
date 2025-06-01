from django.urls import path, include

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns= [
    path('', mainapp.accommodations, name='index'),
    path('accomodation_details/<int:pk>/', mainapp.accommodation, name='accommodation'),
]
