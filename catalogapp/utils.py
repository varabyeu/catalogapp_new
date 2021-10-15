from django.db import models


def recalc_selection(selection):
    """Recalculating fiunction.

    This functions recalculate selected count of items
    in Selecion and gives current total sum
    """
    selection_data = selection.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if selection_data.get('final_price__sum'):
        selection.final_price = selection_data['final_price__sum']
    else:
        selection.final_price = 0
    selection.total_products = selection_data['id__count']
    selection.save()
