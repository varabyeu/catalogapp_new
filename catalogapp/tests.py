from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Boilers, Selection, SelectedProduct, UserClass
from .views import recalc_selection

User = get_user_model()


class CatalogTestCases(TestCase):

    def SetUp(self):
        self.user_for_test = User.objects.create(username='test_user', password='test')
        self.category = Category.objects.create(name='Boilers', slug='boilers')
        image = SimpleUploadedFile(name='boiler_image.jpg', content=b'', content_type='image/jpg')
        self.boiler = Boilers.objects.create(
            category=self.category,
            name='Test Boiler',
            image=image,
            manufacturer='Manufacturer',
            fuel_type1=True,
            fuel_type2=False,
            fuel_type3=True,
            gas_passes_count=2,
            heat_output=70,
            heat_input=74,
            water_press_loss=Decimal(6.0),
            flue_gas_press_loss=Decimal(0.001),
            max_pressure=6,
            weight=236,
            outlet_diameter='65',
            inlet_diameter='65',
            price=Decimal(50000.00)
        )
        self.user = UserClass.objects.create(user=self.user_for_test)
        self.sel = Selection.objects.create(owner=self.user)
        self.selection_product = SelectedProduct.objects.create(
            user=self.user,
            selection=self.sel,
            content_object=self.boiler
        )


    def test_add(self):

        self.sel.products.add(self.selection_product)
        recalc_selection(self.sel)
        self.assertIn(self.selection_product, self.sel.products.all())
        self.assertEqual(self.sel.products.count(), 1)
        self.assertEqual(self.sel.final_price, Decimal(50000.00))
