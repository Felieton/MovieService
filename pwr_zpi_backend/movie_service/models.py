from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DefaultUserManager

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

from django.db.models import Q


class UserManager(DefaultUserManager):
    pass


class UserSettings(models.Model):
    email_visible = models.BooleanField(default=False)
    watchlist_visible = models.BooleanField(default=True)
    achievements_visible = models.BooleanField(default=True)


class Achievement(models.Model):
    class Meta:
        ordering = ('name',)
    name = models.CharField(max_length=150, unique=True)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        ordering = ('-id',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    settings = models.OneToOneField(
        UserSettings,
        on_delete=models.CASCADE,
        null=True
    )
    achievements = models.ManyToManyField(Achievement, blank=True)
    watchlist = models.ManyToManyField('Title', blank=True)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_removed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='users/', blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class RequestActionMixin(models.Model):
    class Meta:
        abstract = True

    ACTION_ADD = 'A'
    ACTION_EDIT = 'E'
    ACTION_REMOVE = 'R'
    ACTION_CHOICES = [
        (ACTION_ADD, 'Add'),
        (ACTION_EDIT, 'Edit'),
        (ACTION_REMOVE, 'Remove'),
    ]
    action = models.CharField(
        max_length=3,
        choices=ACTION_CHOICES
    )


class RequestStatusMixin(models.Model):
    class Meta:
        abstract = True

    STATUS_PENDING = 'P'
    STATUS_ACCEPTED = 'A'
    STATUS_REJECTED = 'R'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )


class AbstractRequest(RequestActionMixin, RequestStatusMixin):
    class Meta:
        abstract = True
        ordering = ('-created',)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    header = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)


class Genre(models.Model):
    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Lang(models.Model):
    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    class Meta:
        ordering = ('name', 'short_name')

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name


class AbstractPerson(models.Model):
    class Meta:
        abstract = True
        ordering = ('surname', 'name')

    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)
    photo = models.ImageField(upload_to='people/', blank=True)

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    def as_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'birthdate': self.birthdate,
            'details': self.details,
            'country': self.country.pk if self.country else None,
            'photo': self.photo if self.photo else None,
        }


class Person(AbstractPerson):
    pass


class PersonSubmission(AbstractPerson):
    person_request = models.OneToOneField(
        'PersonRequest',
        on_delete=models.CASCADE,
        related_name='person_submission'
    )


class PersonRequest(AbstractRequest):
    class Meta:
        permissions = [
            ("accept_personrequest", "Can accept Person Request"),
            ("reject_personrequest", "Can reject Person Request"),
        ]

    current_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Character(models.Model):
    class Meta:
        ordering = ('name',)

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)


class DurationMixin(models.Model):
    class Meta:
        abstract = True

    # in minutes
    duration = models.PositiveSmallIntegerField(null=True, blank=True)


class AbstractTitle(DurationMixin):
    class Meta:
        abstract = True
        ordering = ('-created', 'title')

    languages = models.ManyToManyField(Lang, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    cast_members = models.ManyToManyField('CastMember', blank=True)

    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1800, "Year cannot be less than 1800"),
        ],
    )
    plot = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    released = models.DateField(null=True, blank=True)
    TYPE_MOVIE = 'M'
    TYPE_SERIES = 'S'
    TYPES = [
        (TYPE_MOVIE, 'Movie'),
        (TYPE_SERIES, 'Series'),
    ]
    type = models.CharField(
        max_length=3,
        choices=TYPES,
    )
    seasons_count = models.PositiveSmallIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='titles/', blank=True)

    def __str__(self):
        if self.year is None:
            return self.title
        else:
            return "{} ({})".format(self.title, self.year)

    def as_dict(self):
        def get_ids_list(qs):
            return list(map(lambda item: item['id'], qs.values('id')))

        return {
            'duration': self.duration,
            'languages': get_ids_list(self.languages.all()),
            'countries': get_ids_list(self.countries.all()),
            'genres': get_ids_list(self.genres.all()),
            'characters': get_ids_list(self.characters.all()),
            'cast_members': get_ids_list(self.cast_members.all()),
            'title': self.title,
            'year': self.year,
            'plot': self.plot,
            'created': self.created,
            'released': self.released,
            'type': self.type,
            'seasons_count': self.seasons_count,
            'poster': self.poster if self.poster else None,
        }


class AbstractEpisode(DurationMixin):
    class Meta:
        abstract = True
        ordering = ('name',)

    characters = models.ManyToManyField(Character, blank=True)

    name = models.CharField(max_length=255)
    plot = models.TextField(blank=True)
    released = models.DateField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    season = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()

    def as_dict(self):
        def get_ids_list(qs):
            return list(map(lambda item: item['id'], qs.values('id')))

        return {
            'duration': self.duration,
            'characters': get_ids_list(self.characters.all()),
            'name': self.name,
            'plot': self.plot,
            'released': self.released,
            'created': self.created,
            'season': self.season,
            'number': self.number
        }


class CastRole(models.Model):
    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=255, unique=True)


class ScraperSites(models.Model):
    class Meta:
        ordering = ('id',)

    netloc = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True)
    director = models.CharField(max_length=255, null=True)
    genres = models.CharField(max_length=255, null=True)
    countries = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255, null=True)
    release_date = models.CharField(max_length=255, null=True)
    duration = models.CharField(max_length=255, null=True)
    plot = models.CharField(max_length=255, null=True)


class CastMember(models.Model):
    class Meta:
        ordering = ('id',)

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    roles = models.ManyToManyField(CastRole)


class ComputedRatingMixin(models.Model):
    class Meta:
        abstract = True

    # 00.0
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)


class Title(AbstractTitle, ComputedRatingMixin):
    # selecting average rating for every title
    @staticmethod
    def get_average_ratings():
        titles = Title.objects \
            .annotate(avg_rating=models.Avg('review__rating')) \
            .filter(review__is_accepted=True)
        return titles

    def update_avg_rating(self):
        review_set = Review.objects.filter(is_accepted=True, title=self.pk)
        self.rating = review_set.aggregate(models.Avg('rating'))['rating__avg']
        self.save()


class TitleSubmission(AbstractTitle):
    title_request = models.OneToOneField(
        'TitleRequest',
        on_delete=models.CASCADE,
        related_name='title_submission'
    )


class TitleRequest(AbstractRequest):
    class Meta:
        permissions = [
            ("accept_titlerequest", "Can accept Title Request"),
            ("reject_titlerequest", "Can reject Title Request"),
        ]

    current_title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Episode(AbstractEpisode, ComputedRatingMixin):
    constraints = [
        models.UniqueConstraint(
            fields=['title', 'season', 'number'],
            name='unique_episode'
        )
    ]

    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    # selecting average rating for every title
    @staticmethod
    def get_average_ratings():
        episodes = Episode.objects \
            .annotate(avg_rating=models.Avg('review__rating')) \
            .filter(review__is_accepted=True)
        return episodes

    def update_avg_rating(self):
        review_set = Review.objects.filter(is_accepted=True, episode=self.pk)
        self.rating = review_set.aggregate(models.Avg('rating'))['rating__avg']
        self.save()


class EpisodeSubmission(AbstractEpisode):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    episode_request = models.OneToOneField(
        'EpisodeRequest',
        on_delete=models.CASCADE,
        related_name='episode_submission'
    )

    def as_dict(self):
        res_dict = super().as_dict()
        res_dict['title'] = self.title.pk if self.title else None
        return res_dict


class EpisodeRequest(AbstractRequest):
    class Meta:
        permissions = [
            ("accept_episoderequest", "Can accept Episode Request"),
            ("reject_episoderequest", "Can reject Episode Request"),
        ]

    current_episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Review(models.Model):
    class Meta:
        permissions = [
            ("accept_review", "Can accept Review"),
            ("reject_review", "Can reject Review"),
        ]
        ordering = ('-created',)
        constraints = [
            models.CheckConstraint(
                check=(
                        (Q(title__isnull=True) & Q(episode__isnull=False)) |
                        (Q(title__isnull=False) & Q(episode__isnull=True))
                ),
                name='review_optional_relation'
            ),
            models.UniqueConstraint(
                fields=['user', 'title'],
                name='unique_review_title'
            ),
            models.UniqueConstraint(
                fields=['user', 'episode'],
                name='unique_review_episode'
            )
        ]

    user = models.ForeignKey(
        User,
        models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.CASCADE
    )
    episode = models.ForeignKey(
        Episode,
        null=True,
        on_delete=models.CASCADE
    )

    header = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Rating cannot be less than 1'),
            MaxValueValidator(10, 'Rating cannot be greater than 10'),
        ],
    )
    is_accepted = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)


class AbstractLog(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created',)

    moderator = models.ForeignKey(User, on_delete=models.CASCADE)

    details = models.TextField()
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)


ActionLog_LOG_USER = 'U'


class ActionLog(AbstractLog):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        (
                            Q(log_type=ActionLog_LOG_USER) & Q(user__isnull=False)
                        ) |
                        (
                            Q(user__isnull=True)
                        )
                ),
                name='action_log_optional_relation'
            ),
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='action_logs_of_user')

    LOG_USER = ActionLog_LOG_USER
    LOG_ADMIN = 'A'
    LOG_MODERATOR = 'M'
    LOG_TYPES = [
        (LOG_USER, 'User log'),
        (LOG_ADMIN, 'Admin log'),
        (LOG_MODERATOR, 'Moderator log'),
    ]
    log_type = models.CharField(
        max_length=3,
        choices=LOG_TYPES
    )


class RequestLog(AbstractLog):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        (
                            Q(title_request__isnull=True) & Q(episode_request__isnull=True) &
                            Q(person_request__isnull=False)
                        ) |
                        (
                            Q(title_request__isnull=True) & Q(episode_request__isnull=False) &
                            Q(person_request__isnull=True)
                        ) |
                        (
                            Q(title_request__isnull=False) & Q(episode_request__isnull=True) &
                            Q(person_request__isnull=True)
                        )
                ),
                name='request_log_optional_relation'
            ),
        ]
    title_request = models.ForeignKey(TitleRequest, on_delete=models.CASCADE, null=True)
    episode_request = models.ForeignKey(EpisodeRequest, on_delete=models.CASCADE, null=True)
    person_request = models.ForeignKey(PersonRequest, on_delete=models.CASCADE, null=True)
