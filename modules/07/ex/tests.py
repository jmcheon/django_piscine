from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article, UserFavouriteArticle


class BlogViewsTestCase(TestCase):
    # 1. Tell the test case to load your fixture file
    fixtures = ["data.json"]

    def setUp(self):
        """
        Fetch objects from the database that were loaded by the fixture.
        """
        # 2. Fetch the users and articles 
        #    NOTE: Check your 'data.json' file to make sure the 'pk' (primary key)
        #    values are correct. I am assuming 1 and 2 for users, and 1 for the article.
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.article1 = Article.objects.get(pk=1)

        # 3. Set the passwords manually for the test login.
        #    Fixtures store hashed passwords, but self.client.login needs a plain password.
        self.user1.set_password("passwORd123")
        self.user1.save()
        self.user2.set_password("passwORd123")
        self.user2.save()

        # Create an article authored by user1
        self.article1 = Article.objects.create(
            title="Article by User1",
            author=self.user1,
            synopsis="Test synopsis",
            content="Test content.",
        )

    def test_protected_views_redirect_anonymous_users(self):
        """
        Tests that views requiring login redirect anonymous users to the login page.
        """
        protected_urls = [
            reverse("favourites"),
            reverse("publications"),
            reverse("publish"),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            # Check that the server responds with a redirect (status code 200)
            # and that it redirects to the login URL.
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_register_page_redirects_logged_in_user(self):
        """
        Tests that the registration page redirects an already authenticated user.
        """
        # We capture the return value of the login method
        login_successful = self.client.login(
            username=self.user1, password="passwORd123"
        )

        # This new assertion will fail immediately if the login is unsuccessful,
        # telling us the exact source of the problem.
        self.assertTrue(
            login_successful,
            "Login failed in the test. Check username/password in setUp vs the test.",
        )

        # The rest of the test remains the same
        response = self.client.get(reverse("register"))
        self.assertRedirects(response, reverse("articles"))

    def test_user_cannot_add_duplicate_favourite(self):
        """
        Tests that adding a duplicate favourite does not create a new object.
        """
        # Log the user in
        self.client.login(username="user1", password="passwORd123")

        # Create one favourite entry manually
        UserFavouriteArticle.objects.create(user=self.user1, article=self.article1)

        # Check that this specific user has exactly 1 favourite
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user1).count(), 1
        )

        # Try to add the same article again via the view
        self.client.post(reverse("add_favourite", kwargs={"pk": self.article1.pk}))

        # Assert that the count for this specific user is STILL 1
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user1).count(), 1
        )
