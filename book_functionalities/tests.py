from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from book import settings
from book_functionalities.models import Author, Book, BookGenre, BookReview
from user_profile.models import ExtendedUser, UserProfile


class testBook(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(full_name="Author1",
                                             birth_date="1980-01-01",
                                             biography="biography of author1"
                                             )
        self.author2 = Author.objects.create(full_name="Author2",
                                             birth_date="1980-01-01",
                                             biography="biography of author2"
                                             )

        # --------------------------------------------------------------------
        self.user1 = ExtendedUser.objects.create(username="user1",
                                                 email="mail@mail.com",
                                                 password="passworduser1",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user1 = UserProfile.objects.create(user=self.user1,
                                                        first_name="user1 first name",
                                                        last_name="user1 last name",
                                                        )
        self.user2 = ExtendedUser.objects.create(username="user2",
                                                 email="mail2@mail2.com",
                                                 password="passworduser2",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user2 = UserProfile.objects.create(user=self.user2,
                                                        first_name="user2 first name",
                                                        last_name="user2 last name",
                                                        )
        self.user3 = ExtendedUser.objects.create(username="user3",
                                                 email="mail3@mail3.com",
                                                 password="passworduser3",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user3 = UserProfile.objects.create(user=self.user3,
                                                        first_name="user3 first name",
                                                        last_name="user3 last name",
                                                        )
        # ----------------------------------------------------------------------------
        self.book_genre = BookGenre.objects.create(name="genre1")

    def test_book_avg_score(self):
        book = Book.objects.create(title="book title",
                                   author=self.author1,
                                   release_date=timezone.now(),
                                   synopsis="text",
                                   )
        book.genres.add(self.book_genre)

        review1 = BookReview.objects.create(user_profile=self.profile_user1,
                                            book=book,
                                            content="content text",
                                            rating=10
                                            )

        self.assertNotEqual(book.avg_rating,
                            None,
                            "The average rating for a book with more than zero reviews is 'None'")

        review2 = BookReview.objects.create(user_profile=self.profile_user2,
                                            book=book,
                                            content="content text",
                                            rating=5
                                            )

        self.assertEqual(book.avg_rating, 7.5, "The average rating is not correct")

        review3 = BookReview.objects.create(user_profile=self.profile_user3,
                                            book=book,
                                            content="content text",
                                            rating=5
                                            )

        self.assertEqual(book.avg_rating, 6.67, "The average rating is not rounded properly")

        other_book = Book.objects.create(title="book title2",
                                         author=self.author2,
                                         release_date=timezone.now(),
                                         synopsis="text",
                                         )
        other_book.genres.add(self.book_genre)

        review_other_book = BookReview.objects.create(user_profile=self.profile_user3,
                                                      book=other_book,
                                                      content="content text",
                                                      rating=5
                                                      )

        self.assertEqual(book.avg_rating, 6.67, "The average takes into consideration the ratings of other books")
        self.assertEqual(other_book.avg_rating, 5.0, "The average takes into consideration the ratings of other books")

        other_book.delete()
        review_other_book.delete()
        review1.delete()
        review2.delete()
        review3.delete()

        self.assertEqual(book.avg_rating, None, "The average rating for a book without reviews is not 'None'")

        book.delete()

    def tearDown(self):
        self.author1.delete()
        self.author2.delete()

        self.user1.delete()
        self.profile_user1.delete()
        self.user2.delete()
        self.profile_user2.delete()
        self.user3.delete()
        self.profile_user3.delete()

        self.book_genre.delete()


# ----------------------------View Testing--------------------------------

def create_book(author, *genre_list):
    book = Book.objects.create(title="book title",
                               author=author,
                               release_date=timezone.now(),
                               synopsis="text",
                               )
    for genre in genre_list:
        book.genres.add(genre)

    return book


def create_review(book, user_profile, rating):
    return BookReview.objects.create(user_profile=user_profile,
                                     book=book,
                                     content="content text",
                                     rating=rating
                                     )


class testTopList(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(full_name="Author1",
                                             birth_date="1980-01-01",
                                             biography="biography of author1"
                                             )
        self.author2 = Author.objects.create(full_name="Author2",
                                             birth_date="1980-01-01",
                                             biography="biography of author2"
                                             )
        self.author3 = Author.objects.create(full_name="Author3",
                                             birth_date="1980-01-01",
                                             biography="biography of author3"
                                             )

        # --------------------------------------------------------------------
        self.user1 = ExtendedUser.objects.create(username="user1",
                                                 email="mail@mail.com",
                                                 password="passworduser1",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user1 = UserProfile.objects.create(user=self.user1,
                                                        first_name="user1 first name",
                                                        last_name="user1 last name",
                                                        )
        self.user2 = ExtendedUser.objects.create(username="user2",
                                                 email="mail2@mail2.com",
                                                 password="passworduser2",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user2 = UserProfile.objects.create(user=self.user2,
                                                        first_name="user2 first name",
                                                        last_name="user2 last name",
                                                        )
        self.user3 = ExtendedUser.objects.create(username="user3",
                                                 email="mail3@mail3.com",
                                                 password="passworduser3",
                                                 terms_of_service_acceptance=True
                                                 )
        self.profile_user3 = UserProfile.objects.create(user=self.user3,
                                                        first_name="user3 first name",
                                                        last_name="user3 last name",
                                                        )
        # ----------------------------------------------------------------------------
        self.book_genre1 = BookGenre.objects.create(name="genre1")
        self.book_genre2 = BookGenre.objects.create(name="genre2")
        self.book_genre3 = BookGenre.objects.create(name="genre3")

    def check_no_results(self, response):
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['results_list'], [])
        self.assertContains(response, "No results found")

    def test_no_results(self):
        # No results check with no books
        response = self.client.get(reverse("book_functionalities:book-top-list"))
        self.check_no_results(response)

        # No results check with only books without reviews
        book_without_reviews1 = create_book(self.author1, self.book_genre1)
        book_without_reviews2 = create_book(self.author2, self.book_genre2)

        self.check_no_results(response)
        # No results check with reviewed books of the wrong genre
        reviewed_book1 = book_without_reviews1
        review1 = create_review(reviewed_book1, self.profile_user1, 8)

        response = self.client.get(reverse("book_functionalities:book-top-list"), {'genre': self.book_genre3.id})
        self.check_no_results(response)
        # No results check with reviewed books having the wrong author
        response = self.client.get(reverse("book_functionalities:book-top-list"), {'author': self.author3.full_name})
        self.check_no_results(response)

        # No results check with reviewed books of the wrong genre and the wrong author
        response = self.client.get(reverse("book_functionalities:book-top-list"), {
            'author': self.author3.full_name,
            'genre': self.book_genre3.id,
        })
        self.check_no_results(response)

        reviewed_book1.delete()
        book_without_reviews2.delete()
        review1.delete()

    def test_no_results_incorrect_data(self):
        book1 = create_book(self.author1, self.book_genre1)
        book2 = create_book(self.author1, self.book_genre2)
        book3 = create_book(self.author2, self.book_genre1)
        book4 = create_book(self.author2, self.book_genre2)

        book1_review1 = create_review(book1, self.profile_user1, 10)
        book1_review2 = create_review(book1, self.profile_user2, 10)

        book2_review1 = create_review(book2, self.profile_user1, 10)
        book2_review2 = create_review(book2, self.profile_user2, 9)

        book3_review1 = create_review(book3, self.profile_user1, 9)
        book3_review2 = create_review(book3, self.profile_user2, 9)

        book4_review1 = create_review(book4, self.profile_user1, 9)
        book4_review2 = create_review(book4, self.profile_user2, 8)

        # No results check with non existent genre id
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': self.book_genre3.id+self.book_genre2.id+self.book_genre1.id})
        self.check_no_results(response)

        # No results check with genre id of wrong type (not convertible to an existing id)
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': "a string"})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': 1.5})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': object()})
        self.check_no_results(response)

        # No results check with non existent author
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': self.author1.full_name+"abcd"*5})
        self.check_no_results(response)

        # No results check with author of wrong type (not convertible to an existing author name nor contained in one)
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 17})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 1.5})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': object()})
        self.check_no_results(response)

        # No results check with mixed correct and wrong parameters
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 17, 'genre': self.book_genre1.id})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 1.5, 'genre': self.book_genre1.id})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': object(), 'genre': self.book_genre1.id})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': self.author3.full_name, 'genre': self.book_genre1.id})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': "a string", 'author': self.author1.full_name})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': 1.5, 'author': self.author1.full_name})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': self.book_genre3.id, 'author': self.author1.full_name})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': object(), 'author': self.author1.full_name})
        self.check_no_results(response)

        # No results check with wrong parameters only
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 17, 'genre': "a string"})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': 1.5, 'genre': 1.5})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': object(), 'genre': object()})
        self.check_no_results(response)

        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'author': self.author3.full_name, 'genre': self.book_genre3.id})
        self.check_no_results(response)

        book1.delete()
        book2.delete()
        book3.delete()
        book4.delete()

        book1_review1.delete()
        book1_review2.delete()

        book2_review1.delete()
        book2_review2.delete()

        book3_review1.delete()
        book3_review2.delete()

        book4_review1.delete()
        book4_review2.delete()

    def test_results_with_filtering(self):
        book1 = create_book(self.author1, self.book_genre1)
        book2 = create_book(self.author1, self.book_genre2)
        book3 = create_book(self.author2, self.book_genre1)
        book4 = create_book(self.author2, self.book_genre2)
        book5 = create_book(self.author1, self.book_genre1)
        book6 = create_book(self.author2, self.book_genre2)

        book1_review1 = create_review(book1, self.profile_user1, 10)
        book1_review2 = create_review(book1, self.profile_user2, 10)

        book2_review1 = create_review(book2, self.profile_user1, 10)
        book2_review2 = create_review(book2, self.profile_user2, 9)

        book3_review1 = create_review(book3, self.profile_user1, 9)
        book3_review2 = create_review(book3, self.profile_user2, 9)

        book4_review1 = create_review(book4, self.profile_user1, 9)
        book4_review2 = create_review(book4, self.profile_user2, 8)

        book5_review1 = create_review(book5, self.profile_user1, 8)
        book5_review2 = create_review(book5, self.profile_user2, 8)

        book6_review1 = create_review(book6, self.profile_user1, 8)
        book6_review2 = create_review(book6, self.profile_user2, 7)

        # results with no filtering
        old_value = settings.MIN_AMOUNT_REVIEWS_TOPLIST
        settings.MIN_AMOUNT_REVIEWS_TOPLIST = 1
        response = self.client.get(reverse("book_functionalities:book-top-list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'], [book1, book2, book3, book4, book5, book6])

        # results with filters set on default values
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {"author": "", "genre": '0'}
                                   )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'], [book1, book2, book3, book4, book5, book6])

        # results with filtering on genre
        response = self.client.get(reverse("book_functionalities:book-top-list"), {'genre': self.book_genre1.id})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'], [book1, book3, book5])

        # results with filtering on author
        response = self.client.get(reverse("book_functionalities:book-top-list"), {'author': self.author1.full_name})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'], [book1, book2, book5])

        # results with filtering on author and genre
        response = self.client.get(reverse("book_functionalities:book-top-list"),
                                   {'genre': self.book_genre1.id, 'author': self.author1.full_name},
                                   )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'], [book1, book5])

        # results with filtering on list length (the view should return 10 results at most)
        book7 = create_book(self.author1, self.book_genre1.id)
        book8 = create_book(self.author1, self.book_genre1.id)
        book9 = create_book(self.author1, self.book_genre1.id)
        book10 = create_book(self.author1, self.book_genre1.id)
        book11 = create_book(self.author1, self.book_genre1.id)
        book12 = create_book(self.author1, self.book_genre1.id)

        book7_review = create_review(book7, self.profile_user1, 7)
        book8_review = create_review(book8, self.profile_user1, 6)
        book9_review = create_review(book9, self.profile_user1, 5)
        book10_review = create_review(book10, self.profile_user1, 4)
        book11_review = create_review(book11, self.profile_user1, 3)
        book12_review = create_review(book12, self.profile_user1, 2)

        response = self.client.get(reverse("book_functionalities:book-top-list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'],
                         [book1, book2, book3, book4, book5, book6, book7, book8, book9, book10]
                         )

        # results with minimum amount of reviews to be included in the evaluation > 1
        settings.MIN_AMOUNT_REVIEWS_TOPLIST = 2

        response = self.client.get(reverse("book_functionalities:book-top-list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertNotEqual(response.context['results_list'], [])
        self.assertEqual(response.context['results_list'],
                         [book1, book2, book3, book4, book5, book6]
                         )

        settings.MIN_AMOUNT_REVIEWS_TOPLIST = old_value
        # deletion of the data
        book1.delete()
        book2.delete()
        book3.delete()
        book4.delete()
        book5.delete()
        book6.delete()
        book7.delete()
        book8.delete()
        book9.delete()
        book10.delete()
        book11.delete()
        book12.delete()

        book1_review1.delete()
        book1_review2.delete()

        book2_review1.delete()
        book2_review2.delete()

        book3_review1.delete()
        book3_review2.delete()

        book4_review1.delete()
        book4_review2.delete()

        book5_review1.delete()
        book5_review2.delete()

        book6_review1.delete()
        book6_review2.delete()

        book7_review.delete()
        book8_review.delete()
        book9_review.delete()
        book10_review.delete()
        book11_review.delete()
        book12_review.delete()

    def tearDown(self):
        self.author1.delete()
        self.author2.delete()
        self.author3.delete()

        self.user1.delete()
        self.profile_user1.delete()
        self.user2.delete()
        self.profile_user2.delete()
        self.user3.delete()
        self.profile_user3.delete()

        self.book_genre1.delete()
        self.book_genre2.delete()
        self.book_genre3.delete()



