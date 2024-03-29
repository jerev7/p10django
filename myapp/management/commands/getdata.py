from myapp.models import Category, Products
import requests
from django.core.management.base import BaseCommand, CommandError


"""
code working for this url :
url = https://fr.openfoodfacts.org/categorie/pates-a-tartiner-aux-noisettes/1.json
"""
def get_product(category, url):

    final_list = []

    nutrition_grade_list = ["a", "b", "c", "d", "e"]
    nutriscore_letter_url = [
        "myapp/assets/img/nutriscore/nutrilettre_a.png",
        "myapp/assets/img/nutriscore/nutrilettre_b.png",
        "myapp/assets/img/nutriscore/nutrilettre_c.png",
        "myapp/assets/img/nutriscore/nutrilettre_d.png",
        "myapp/assets/img/nutriscore/nutrilettre_e.png"
    ]
    nutriscore_complete_url = [
        "myapp/assets/img/nutriscore/nutricomplet_a.png",
        "myapp/assets/img/nutriscore/nutricomplet_b.png",
        "myapp/assets/img/nutriscore/nutricomplet_c.png",
        "myapp/assets/img/nutriscore/nutricomplet_d.png",
        "myapp/assets/img/nutriscore/nutricomplet_e.png"
    ]
    response = requests.get(url)
    my_products = response.json()["products"]
    # i = 0
    for product in my_products:
        if 'product_name_fr' in product and product["product_name_fr"] != "" and "image_front_url" in product:
            new_entry = {}
            new_entry["name"] = product["product_name_fr"]
            new_entry["category"] = category
            new_entry["url_offacts"] = product["url"]
            try:
                new_entry["energy_value"] = str(product["nutriments"]["energy_value"])
            except:
                new_entry["energy_value"] = "not found"
            try:
                new_entry["energy_unit"] = product["nutriments"]["energy_unit"]
            except:
                new_entry["energy_unit"] = "not found"
            try:    
                new_entry["sugars_100g"] = str(product["nutriments"]["sugars_100g"])
            except:
                new_entry["sugars_100g"] = "not found"
            try:
                new_entry["fat_100g"] = str(product["nutriments"]["fat_100g"])
            except:
                new_entry["fat_100g"] = "not found"
            try:
                new_entry["saturated_fat_100g"] = str(product["nutriments"]["saturated-fat_100g"])
            except:
                new_entry["saturated_fat_100g"] = "not found"
            try:
                new_entry["proteins"] = str(product["nutriments"]["proteins"])
            except:
                new_entry["proteins"] = "not found"
            if "nutrition_grades" in product:
                new_entry["nutriscore"] = nutrition_grade_list.index(product["nutrition_grades"])
            else:
                new_entry["nutriscore"] = 4
            new_entry["nutriscore_letter_url"] = nutriscore_letter_url[new_entry["nutriscore"]]
            new_entry["nutriscore_complete_url"] = nutriscore_complete_url[new_entry["nutriscore"]]
            new_entry["image_url"] = product["image_front_url"]
            # mettre chaine vide et mettre le lien dans le front
            # i += 1
            # new_entry["compte"] = i
            final_list.append(new_entry)
    return final_list



# print(get_product("pates-a-tartiner-aux-noisettes", "https://fr.openfoodfacts.org/categorie/pates-a-tartiner-aux-noisettes/1.json"))


def add_products_to_db(product_list):
    for element in product_list:
        if Products.objects.filter(name=element["name"]).exists():
            pass
        else:
            new_product = Products.objects.create(
                name=element["name"],
                nutriscore=element["nutriscore"],
                image_url=element["image_url"],
                url_offacts=element["url_offacts"],
                energy_value=element["energy_value"],
                energy_unit=element["energy_unit"],
                sugars_100g=element["sugars_100g"],
                fat_100g=element["fat_100g"],
                saturated_fat_100g=element["saturated_fat_100g"],
                proteins=element["proteins"],
                nutriscore_letter_url=element["nutriscore_letter_url"],
                nutriscore_complete_url=element["nutriscore_complete_url"]
            )
            category_check = Category.objects.filter(name=element["category"])
            if not category_check.exists():
                category = Category.objects.create(name=element["category"])
            else:
                category = category_check[0]
            new_product.categories.add(category)

class Command(BaseCommand):

    help = "Get the data to fill database"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        add_products_to_db(get_product("pates-a-tartiner-aux-noisettes", "https://fr.openfoodfacts.org/categorie/pates-a-tartiner-aux-noisettes/1.json"))
        add_products_to_db(get_product("pizzas-tartes-salees-et-quiches","https://fr.openfoodfacts.org/categorie/pizzas-tartes-salees-et-quiches/1.json"))
        add_products_to_db(get_product("saucissons-secs", "https://fr.openfoodfacts.org/categorie/saucissons-secs/1.json"))
        add_products_to_db(get_product("poulets", "https://fr.openfoodfacts.org/categorie/poulets/1.json"))
        add_products_to_db(get_product("fromages", "https://fr.openfoodfacts.org/categorie/fromages/1.json"))

        self.stdout.write(self.style.SUCCESS('Data successfully inserted in database'))