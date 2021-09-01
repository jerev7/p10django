from django.test import TestCase
from django.urls import reverse
from .models import Category, Products, Product_saved
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui


# Create your tests here.

testproduct = ""
testproduct2 = ""


def setting_up_db():
    testcategory = Category.objects.create(name="testcategory")
    testproduct = Products.objects.create(name="testproduct",
                                          nutriscore=4,
                                          image_url="/",
                                          url_offacts="/",
                                          energy_value=24.2,
                                          energy_unit="kcal",
                                          sugars_100g=12.1,
                                          fat_100g=2,
                                          saturated_fat_100g=1.2,
                                          proteins=4,
                                          nutriscore_complete_url="myapp/assets\
                                          /img/nutriscore/nutricomplet_e.png",
                                          nutriscore_letter_url="myapp/assets\
                                          /img/nutriscore/nutrilettre_e.png")
    testproduct2 = Products.objects.create(name="testproduct2",
                                           nutriscore=3,
                                           image_url="/",
                                           url_offacts="/",
                                           energy_value=24.2,
                                           energy_unit="kcal",
                                           sugars_100g=12.1,
                                           fat_100g=2,
                                           saturated_fat_100g=1.2,
                                           proteins=4,
                                           nutriscore_complete_url="myapp\
                                           /assets/img/nutriscore\
                                           /nutricomplet_d.png",
                                           nutriscore_letter_url="myapp/assets\
                                           /img/nutriscore/nutrilettre_d.png")
    testproduct.categories.add(testcategory)
    testproduct2.categories.add(testcategory)
    User.objects.create(username="Bob",
                        email="bob@gmail.com",
                        password="bobby")


# Index page
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# Legal notices
class LegalPageTestCase(TestCase):
    def test_legal_page(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)


# Search page
class SearchPageTestCase(TestCase):
    def setUp(self):  # create data before tests start
        setting_up_db()

    def test_search_page_product_found(self):
        response = self.client.get(reverse('search'), {'query': 'testproduct'})
        self.assertEqual(response.status_code, 200)

    def test_search_page_product_not_found(self):
        response = self.client.get(reverse('search'), {'query': 'huhuhuhu'})
        self.assertEqual(response.status_code, 404)


# Result page
class ResultPageTestCase(TestCase):
    def setUp(self):  # create data before tests start
        setting_up_db()

    def test_result_page_product_found(self):
        myproduct = Products.objects.get(name="testproduct")
        product_id = myproduct.id
        response = self.client.get(reverse('results', args=(product_id,)))
        self.assertEqual(response.status_code, 200)


# Product detail
class DetailPageTestCase(TestCase):
    def setUp(self):  # create data before tests start
        setting_up_db()

    def test_detail_page_product_found(self):
        myproduct = Products.objects.get(name="testproduct")
        product_id = myproduct.id
        response = self.client.get(reverse('product_detail',
                                           args=(product_id,)))
        self.assertEqual(response.status_code, 200)


# Save and delete a product
class SaveProductPageTestCase(TestCase):
    def setUp(self):  # create data before tests start
        setting_up_db()

    def test_saveanddelete_product_page(self):
        self.client.force_login(user=User.objects.get(username='Bob'))
        saved_products = Product_saved.objects.all()
        products_number_before = len(saved_products)
        prod_to_save_selected = Products.objects.get(name="testproduct")
        prod_to_save_sel_id = Products.objects.get(name="testproduct").id
        prod_to_save_subst = Products.objects.get(name="testproduct2")
        prod_save_subst_id = Products.objects.get(name="testproduct2").id
        # Saving new product
        res = (self.client
               .get(reverse('save_product',
                            kwargs={'product_selected_id': prod_to_save_sel_id,
                                    'substitution_id': prod_save_subst_id})))
        self.assertEqual(res.status_code, 302)

        saved_products_after = Product_saved.objects.all()
        products_number_after = len(saved_products_after)
        self.assertEqual(products_number_after, (products_number_before + 1))

        # Deleting new product
        new_product_saved = (Product_saved.objects
                             .get(product_selected=prod_to_save_selected,
                                  substitution_product=prod_to_save_subst,
                                  user=User.objects.get(username='Bob')))
        response2 = self.client.get(reverse('delete_product',
                                            args=(new_product_saved.id,)))
        self.assertEqual(response2.status_code, 302)
        products_number_finally = len(Product_saved.objects.all())
        self.assertEqual(products_number_finally, products_number_before)


# ------------------- Selenium tests ------------------------#
class PlayerFormTest(LiveServerTestCase):

    def setUp(self):
        """
        Setting up selenium server
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://p8django.herokuapp.com/")
        self.wait = ui.WebDriverWait(self.driver, 3000)

    # def tearDown(self):
    #     """
    #     Closing the server
    #     """
    #     self.driver.quit()
    def test_search_page(self):
        # find the elements you need to submit form
        search_test = "nutella"
        form = self.driver.find_element_by_id('searchForm')
        form.send_keys(search_test)
        form.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(100)
        ui.WebDriverWait(self.driver, 3000)

        # testing search : nutella
        product_searched = (self.driver
                            .find_element_by_id('product_searched').text)
        self.assertEqual(product_searched, "Produit recherché : nutella")
        url = self.driver.current_url
        self.assertEqual(url, "https://p8django.herokuapp.com"
                              "/myapp/search/?query=nutella")

        # selecting the first product
        self.driver.find_element_by_partial_link_text("Nutella").click()
        url = self.driver.current_url
        self.assertEqual(url, "https://p8django.herokuapp.com/myapp/2/")

        # see first product detail
        self.driver.find_element_by_partial_link_text("Pâte").click()
        url = self.driver.current_url
        self.assertEqual(url, "https://p8django.herokuapp.com"
                              "/myapp/product_detail/3/")
