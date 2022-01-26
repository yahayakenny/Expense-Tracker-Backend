from core.helpers import AuthenticateUser
from category.models import Category


class categoryModelTest(AuthenticateUser):
    def test_category(self):
        user = self.authenticate_user()
        test_category_one = Category.objects.create(
            name="new category",
        )
        test_category_two = Category.objects.create(
            name="new category 2",
        )
        test_category_three = Category.objects.create(
            name="new category 3",
        )
        category_count = Category.objects.all().count()
        self.assertEqual(category_count, 8)
    

