from django.urls import reverse

from rest_framework import status

from movie_service.models import Review

from . import AbstractApiModelTests, TitleTestsMixin


class ApiReviewTests(TitleTestsMixin, AbstractApiModelTests):
    rev_urls = {
        'list': 'review-list',
        'detail': 'review-detail',
        'accept': 'review-accept',
        'reject': 'review-reject',
    }
    data = {
        'review_01': {
            'body': 'Lorem ipsum dolor sit amet',
            'rating': 8,
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.title = cls._create_title_with_m2m()

    @classmethod
    def _create_review(cls):
        review_data = cls.data['review_01']
        data = review_data.copy()
        data['user'] = cls.user
        data['title'] = cls.title
        return Review.objects.create(**data)

    def test_accept_title_review(self):
        self.client.force_authenticate(self.root)
        review = self._create_review()

        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': review.pk}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Review accept should have OK status'
        )
        review.refresh_from_db()
        self.assertTrue(
            review.is_accepted,
            msg='The review should be accepted'
        )

    def test_accept_title_review_fail(self):
        self.client.force_authenticate(self.root)
        review = self._create_review()
        review.is_accepted = True
        review.save()

        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': review.pk}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=f'The review is already accepted so review accept should fail'
        )

        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
            msg=f'The review does not exist so review accept should fail'
        )

    def test_reject_title_review(self):
        self.client.force_authenticate(self.root)
        review = self._create_review()

        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': review.pk}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Review reject should have OK status'
        )
        review = Review.objects.filter(pk=review.pk).first()
        self.assertIsNone(
            review,
            msg='Rejected review should be deleted'
        )

    def test_reject_title_review_fail(self):
        self.client.force_authenticate(self.root)
        review = self._create_review()
        review.is_accepted = True
        review.save()

        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': review.pk}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=f'The review is already accepted so review reject should fail'
        )

        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
            msg=f'The review does not exist so review reject should fail'
        )
