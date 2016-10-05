from django.contrib import admin
from django.utils.functional import curry

from .models import FieldOffice, Person, Item

class ItemInline(admin.TabularInline):
    model = Item
    extra = 5

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if hasattr(request.user, 'person'):
            for i in range(0,self.extra):
                initial.append({'added_by': request.user.person, 'for_office': request.user.person.office })
        formset = super(ItemInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset

class FieldOfficeAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

class ItemAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('added_by',)
        return self.readonly_fields

admin.site.register(FieldOffice, FieldOfficeAdmin)
admin.site.register(Person)
admin.site.register(Item, ItemAdmin)

# Register your models here.
