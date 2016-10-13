from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic

from utils import verify_input, return_within_limit, get_address
from .models import FieldOffice, Item

class OfficeView(generic.ListView):
    template_name = 'tasks/office_list.html'
    model = FieldOffice

class NearbyOfficeView(generic.ListView):
    template_name = 'tasks/nearby_office_list.html'
    model = FieldOffice

    def get_context_data(self, **kwargs):
        context = super(NearbyOfficeView, self).get_context_data(**kwargs)
        lat = self.kwargs.get('lat', None)
        lon = self.kwargs.get('lon', None)
        limit = self.kwargs.get('limit', 25)
        if lat and lon:
            your_location = get_address(lat, lon)
            context['nearby_office_list'] = return_within_limit(lat, lon, limit)
            if context['nearby_office_list'] == []:
                context['message_string'] = "There are no field offices within " + str(limit) + " miles of " + your_location + "."
            else:
                context['message_string'] = "Field offices within " + str(limit) + " miles of " +  your_location + "."
        return context

class SingleOfficeView(generic.DetailView):
    template_name = 'tasks/single_office.html'
    model = FieldOffice

class ItemView(generic.ListView):
    template_name = 'tasks/item_list.html'

    def get_queryset(self):
        return Item.objects.all().order_by('-quantity')

def SearchFieldOfficeView(request):
    location = request.GET.get('location')
    limit = request.GET.get('limit')
    resp = verify_input(location, limit)
    if resp:
        url = reverse('nearby', kwargs={'lat': resp['lat'], 'lon': resp['lon'], 'limit': resp['limit']})
        return JsonResponse({'status': 'success', 'url': url})
    else:
        return JsonResponse({'status': 'error', 'message':"I'm sorry, that address/zip code/city was not recognized."})
