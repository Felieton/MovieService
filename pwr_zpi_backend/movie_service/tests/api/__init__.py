from movie_service.models import Person, CastRole, Lang, Country, Genre


def init_title_related_simple_objects(amount=30):
    for i in range(amount):
        Person.objects.update_or_create(
            defaults={
                'name': f'Morgan{i}',
                'surname': f'Freeman{i}',
                'birthdate': '1937-06-01',
            },
            id=i + 1
        )
        CastRole.objects.update_or_create(
            defaults={'name': f'director{i}'},
            id=i + 1
        )
        Lang.objects.update_or_create(
            defaults={'name': f'English{i}'},
            id=i + 1
        )
        Country.objects.update_or_create(
            defaults={'name': f'United States{i}', 'short_name': f'USA{i}'},
            id=i + 1
        )
        Genre.objects.update_or_create(
            defaults={'name': f'Fantasy{i}'},
            id=i + 1
        )
