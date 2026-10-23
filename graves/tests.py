from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse

from .models import (
    Cemetery,
    Grave,
    MonumentCondition,
    MonumentMacroType,
    MonumentPosition,
    MonumentTradition,
    MonumentType,
    Person,
)


class SearchViewTests(TestCase):
    def setUp(self):
        self.cemetery = Cemetery.objects.create(
            name="Staro groblje",
            city="Živinice",
            village="Šerići",
            status=Cemetery.STATUS_APPROVED,
        )
        self.grave = Grave.objects.create(
            cemetery=self.cemetery,
            title="Kameni mezar",
            status=Grave.STATUS_APPROVED,
        )
        self.person = Person.objects.create(
            grave=self.grave,
            first_name="Rasim",
            last_name="Numanagić",
            birth_year=1901,
            death_year=1982,
            status=Person.STATUS_APPROVED,
        )

    def search_persons(self, query):
        response = self.client.get(
            reverse("graves:search"),
            {"q": query},
        )

        self.assertEqual(response.status_code, 200)
        return list(response.context["persons"].object_list)

    def search_cemeteries(self, query):
        response = self.client.get(
            reverse("graves:search"),
            {"q": query},
        )

        self.assertEqual(response.status_code, 200)
        return list(response.context["cemeteries"].object_list)

    def test_cemetery_search_matches_name_city_and_village(self):
        queries = (
            "Staro groblje",
            "Zivinice",
            "Serici",
        )

        for query in queries:
            with self.subTest(query=query):
                self.assertEqual(
                    self.search_cemeteries(query),
                    [self.cemetery],
                )

    def test_cemetery_search_ranks_exact_name_before_partial_name(self):
        partial_match = Cemetery.objects.create(
            name="Staro groblje na brdu",
            status=Cemetery.STATUS_APPROVED,
        )

        self.assertEqual(
            self.search_cemeteries("Staro groblje"),
            [self.cemetery, partial_match],
        )

    def test_cemetery_results_have_independent_pagination(self):
        for index in range(11):
            Cemetery.objects.create(
                name=f"Groblje {index:02d}",
                status=Cemetery.STATUS_APPROVED,
            )

        response = self.client.get(
            reverse("graves:search"),
            {
                "q": "groblje",
                "cemeteries_page": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cemeteries"].number, 2)
        self.assertEqual(response.context["cemeteries"].paginator.count, 12)
        self.assertEqual(len(response.context["cemeteries"].object_list), 2)

    def test_cemetery_only_query_does_not_list_all_related_graves(self):
        response = self.client.get(
            reverse("graves:search"),
            {"q": "Staro groblje"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["cemeteries"].object_list),
            [self.cemetery],
        )
        self.assertEqual(
            list(response.context["graves"].object_list),
            [],
        )

    def test_search_does_not_show_unapproved_cemetery(self):
        Cemetery.objects.create(
            name="Skriveno groblje",
            city="Živinice",
            status=Cemetery.STATUS_PENDING,
        )

        self.assertEqual(
            self.search_cemeteries("Skriveno groblje"),
            [],
        )

    def test_cemetery_and_location_filters_work_without_text_query(self):
        filter_queries = (
            {"cemetery": self.cemetery.pk},
            {"location": "Zivinice"},
        )

        for parameters in filter_queries:
            with self.subTest(parameters=parameters):
                response = self.client.get(
                    reverse("graves:search"),
                    parameters,
                )

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["has_search"])
                self.assertEqual(
                    list(response.context["cemeteries"].object_list),
                    [self.cemetery],
                )
                self.assertEqual(
                    list(response.context["graves"].object_list),
                    [self.grave],
                )
                self.assertEqual(
                    list(response.context["persons"].object_list),
                    [self.person],
                )

    def test_birth_and_death_year_ranges_filter_all_result_groups(self):
        Person.objects.create(
            grave=self.grave,
            first_name="Starija",
            last_name="Osoba",
            birth_year=1850,
            death_year=1910,
            status=Person.STATUS_APPROVED,
        )

        response = self.client.get(
            reverse("graves:search"),
            {
                "birth_year_from": 1900,
                "birth_year_to": 1910,
                "death_year_from": 1980,
                "death_year_to": 1990,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["persons"].object_list),
            [self.person],
        )
        self.assertEqual(
            list(response.context["graves"].object_list),
            [self.grave],
        )
        self.assertEqual(
            list(response.context["cemeteries"].object_list),
            [self.cemetery],
        )

    def test_invalid_year_range_displays_error_without_running_search(self):
        response = self.client.get(
            reverse("graves:search"),
            {
                "birth_year_from": 2000,
                "birth_year_to": 1900,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["has_search"])
        self.assertFormError(
            response.context["search_form"],
            "birth_year_to",
            "Završna godina mora biti jednaka ili veća od početne.",
        )

    def test_basic_classification_filters_apply_to_all_result_groups(self):
        classification_values = {
            "macro_type": MonumentMacroType.objects.create(
                code="MT-T",
                name="Nadgrobnik",
            ),
            "tradition": MonumentTradition.objects.create(
                code="TR-T",
                name="Osmanska tradicija",
            ),
            "monument_type": MonumentType.objects.create(
                code="TIP-T",
                name="Nišan",
            ),
            "condition_classification": MonumentCondition.objects.create(
                code="ST-T",
                name="Dobro očuvano",
            ),
            "monument_position": MonumentPosition.objects.create(
                code="POZ-T",
                name="Uspravno",
            ),
        }

        for field_name, value in classification_values.items():
            setattr(self.grave, field_name, value)

        self.grave.save(update_fields=list(classification_values))

        for field_name, value in classification_values.items():
            with self.subTest(field_name=field_name):
                response = self.client.get(
                    reverse("graves:search"),
                    {field_name: value.pk},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["cemeteries"].object_list),
                    [self.cemetery],
                )
                self.assertEqual(
                    list(response.context["graves"].object_list),
                    [self.grave],
                )
                self.assertEqual(
                    list(response.context["persons"].object_list),
                    [self.person],
                )

    def test_pagination_query_preserves_text_and_filters(self):
        response = self.client.get(
            reverse("graves:search"),
            {
                "q": "Rasim",
                "location": "Zivinice",
                "cemetery": self.cemetery.pk,
                "persons_page": 2,
            },
        )

        pagination_query = response.context["pagination_query"]

        self.assertIn("q=Rasim", pagination_query)
        self.assertIn("location=Zivinice", pagination_query)
        self.assertIn(
            f"cemetery={self.cemetery.pk}",
            pagination_query,
        )
        self.assertNotIn("persons_page", pagination_query)

    def test_person_search_accepts_name_tokens_in_either_order(self):
        queries = (
            "Numanagić Rasim",
            "Rasim Numanagić",
            "Rasim",
            "Numanagić",
        )

        for query in queries:
            with self.subTest(query=query):
                self.assertEqual(
                    self.search_persons(query),
                    [self.person],
                )

    def test_person_search_supports_common_terminal_a_name_form(self):
        self.assertEqual(
            self.search_persons("Numanagić Rasima"),
            [self.person],
        )

    def test_person_search_treats_c_caron_c_acute_and_c_as_equal(self):
        queries = (
            "Numanagić",
            "Numanagič",
            "Numanagic",
        )

        for query in queries:
            with self.subTest(query=query):
                self.assertEqual(
                    self.search_persons(query),
                    [self.person],
                )

    def test_person_search_normalizes_s_and_z_diacritics(self):
        person = Person.objects.create(
            grave=self.grave,
            first_name="Šaćir",
            last_name="Žunić",
            status=Person.STATUS_APPROVED,
        )

        self.assertEqual(
            self.search_persons("Sacir Zunic"),
            [person],
        )

    def test_person_search_treats_d_stroke_as_dj(self):
        person = Person.objects.create(
            grave=self.grave,
            first_name="Đorđe",
            last_name="Đurić",
            status=Person.STATUS_APPROVED,
        )

        queries = (
            "Djordje Djuric",
            "Đorđe Đurić",
        )

        for query in queries:
            with self.subTest(query=query):
                self.assertEqual(
                    self.search_persons(query),
                    [person],
                )

    def test_person_search_matches_numeric_birth_or_death_year(self):
        for query in ("1901", "1982"):
            with self.subTest(query=query):
                self.assertEqual(
                    self.search_persons(query),
                    [self.person],
                )

    def test_person_search_combines_name_and_numeric_year_tokens(self):
        Person.objects.create(
            grave=self.grave,
            first_name="Almir",
            last_name="Numanagić",
            birth_year=1920,
            death_year=2000,
            status=Person.STATUS_APPROVED,
        )

        self.assertEqual(
            self.search_persons("Numanagic 1982"),
            [self.person],
        )

    def test_person_search_ranks_exact_full_name_before_partial_name(self):
        partial_match = Person.objects.create(
            grave=self.grave,
            first_name="Rasimullah",
            last_name="Numanagić",
            status=Person.STATUS_APPROVED,
        )

        self.assertEqual(
            self.search_persons("Numanagic Rasim"),
            [self.person, partial_match],
        )

    def test_person_search_requires_every_token_to_match(self):
        self.assertEqual(
            self.search_persons("Rasim Hadžić"),
            [],
        )

    def test_terminal_a_fallback_does_not_enable_prefix_matches(self):
        Person.objects.create(
            grave=self.grave,
            first_name="Almir",
            last_name="Drugić",
            status=Person.STATUS_APPROVED,
        )

        self.assertEqual(self.search_persons("Alma"), [])

    def test_grave_search_matches_tokens_across_fields(self):
        response = self.client.get(
            reverse("graves:search"),
            {"q": "groblje kameni"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["graves"].object_list),
            [self.grave],
        )

    def test_grave_search_normalizes_diacritics(self):
        self.grave.title = "Oštećeni nišan"
        self.grave.save(update_fields=["title"])

        response = self.client.get(
            reverse("graves:search"),
            {"q": "osteceni nisan"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["graves"].object_list),
            [self.grave],
        )

    def test_grave_search_ranks_title_before_inscription_match(self):
        title_match = Grave.objects.create(
            cemetery=self.cemetery,
            title="Porodični kameni mezar",
            status=Grave.STATUS_APPROVED,
        )
        inscription_match = Grave.objects.create(
            cemetery=self.cemetery,
            title="Drugi spomenik",
            inscription="U blizini se nalazi kameni mezar.",
            status=Grave.STATUS_APPROVED,
        )

        response = self.client.get(
            reverse("graves:search"),
            {"q": "kameni mezar"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["graves"].object_list),
            [self.grave, title_match, inscription_match],
        )

    def test_person_ranking_is_applied_before_independent_pagination(self):
        partial_matches = []

        for index in range(10):
            partial_matches.append(
                Person.objects.create(
                    grave=self.grave,
                    first_name=f"Rasim{index:02d}",
                    last_name="Numanagić",
                    status=Person.STATUS_APPROVED,
                )
            )

        first_page = self.client.get(
            reverse("graves:search"),
            {"q": "Numanagic Rasim"},
        )
        second_page = self.client.get(
            reverse("graves:search"),
            {
                "q": "Numanagic Rasim",
                "persons_page": 2,
            },
        )

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(second_page.status_code, 200)
        self.assertEqual(
            first_page.context["persons"].paginator.count,
            11,
        )
        self.assertEqual(
            first_page.context["persons"].object_list[0],
            self.person,
        )
        self.assertEqual(len(first_page.context["persons"].object_list), 10)
        self.assertEqual(len(second_page.context["persons"].object_list), 1)
        self.assertNotIn(
            self.person,
            second_page.context["persons"].object_list,
        )

    def test_grave_ranking_is_applied_before_independent_pagination(self):
        for index in range(10):
            Grave.objects.create(
                cemetery=self.cemetery,
                title=f"Kameni mezar {index:02d}",
                status=Grave.STATUS_APPROVED,
            )

        first_page = self.client.get(
            reverse("graves:search"),
            {"q": "kameni mezar"},
        )
        second_page = self.client.get(
            reverse("graves:search"),
            {
                "q": "kameni mezar",
                "graves_page": 2,
            },
        )

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(second_page.status_code, 200)
        self.assertEqual(
            first_page.context["graves"].paginator.count,
            11,
        )
        self.assertEqual(
            first_page.context["graves"].object_list[0],
            self.grave,
        )
        self.assertEqual(len(first_page.context["graves"].object_list), 10)
        self.assertEqual(len(second_page.context["graves"].object_list), 1)
        self.assertNotIn(
            self.grave,
            second_page.context["graves"].object_list,
        )

    def test_invalid_page_value_falls_back_without_error(self):
        response = self.client.get(
            reverse("graves:search"),
            {
                "q": "Rasim",
                "persons_page": "nije-broj",
                "graves_page": "nije-broj",
                "cemeteries_page": "nije-broj",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["persons"].number, 1)
        self.assertEqual(response.context["graves"].number, 1)
        self.assertEqual(response.context["cemeteries"].number, 1)

    def test_map_deduplicates_grave_found_directly_and_through_people(self):
        self.grave.location = Point(18.1781, 43.9889, srid=4326)
        self.grave.save(update_fields=["location"])

        self.person.first_name = "Kameni"
        self.person.save(update_fields=["first_name"])
        Person.objects.create(
            grave=self.grave,
            first_name="Kameni",
            last_name="Druga osoba",
            status=Person.STATUS_APPROVED,
        )

        response = self.client.get(
            reverse("graves:search"),
            {"q": "Kameni"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [grave.id for grave in response.context["map_graves"]],
            [self.grave.id],
        )

    def test_cemetery_and_grave_markers_use_separate_collections(self):
        self.cemetery.name = "Kameni groblje"
        self.cemetery.location = Point(18.17, 43.98, srid=4326)
        self.cemetery.save(update_fields=["name", "location"])

        self.grave.location = Point(18.18, 43.99, srid=4326)
        self.grave.save(update_fields=["location"])

        response = self.client.get(
            reverse("graves:search"),
            {"q": "Kameni"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [
                cemetery.id
                for cemetery in response.context["map_cemeteries"]
            ],
            [self.cemetery.id],
        )
        self.assertEqual(
            [grave.id for grave in response.context["map_graves"]],
            [self.grave.id],
        )
        self.assertContains(
            response,
            f"cemeteryMarkers[{self.cemetery.id}]",
        )
        self.assertContains(
            response,
            f"graveMarkers[{self.grave.id}]",
        )

    def test_unapproved_grave_hides_itself_and_approved_people(self):
        for status, label in (
            (Grave.STATUS_PENDING, "GrobNaCekanju"),
            (Grave.STATUS_REJECTED, "OdbijeniGrob"),
        ):
            with self.subTest(status=status):
                grave = Grave.objects.create(
                    cemetery=self.cemetery,
                    title=f"{label} mezar",
                    status=status,
                )
                Person.objects.create(
                    grave=grave,
                    first_name=label,
                    last_name="Osoba",
                    status=Person.STATUS_APPROVED,
                )

                response = self.client.get(
                    reverse("graves:search"),
                    {"q": label},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["graves"].object_list),
                    [],
                )
                self.assertEqual(
                    list(response.context["persons"].object_list),
                    [],
                )

    def test_unapproved_cemetery_hides_all_approved_child_content(self):
        for status, label in (
            (Cemetery.STATUS_PENDING, "GrobljeNaCekanju"),
            (Cemetery.STATUS_REJECTED, "OdbijenoGroblje"),
        ):
            with self.subTest(status=status):
                cemetery = Cemetery.objects.create(
                    name=f"{label} lokacija",
                    status=status,
                )
                grave = Grave.objects.create(
                    cemetery=cemetery,
                    title=f"{label} mezar",
                    status=Grave.STATUS_APPROVED,
                )
                Person.objects.create(
                    grave=grave,
                    first_name=label,
                    last_name="Osoba",
                    status=Person.STATUS_APPROVED,
                )

                response = self.client.get(
                    reverse("graves:search"),
                    {"q": label},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["cemeteries"].object_list),
                    [],
                )
                self.assertEqual(
                    list(response.context["graves"].object_list),
                    [],
                )
                self.assertEqual(
                    list(response.context["persons"].object_list),
                    [],
                )

    def test_search_does_not_show_unapproved_person(self):
        for status in (
            Person.STATUS_PENDING,
            Person.STATUS_REJECTED,
        ):
            Person.objects.create(
                grave=self.grave,
                first_name="Sakriven",
                last_name="Zapis",
                status=status,
            )

        self.assertEqual(self.search_persons("Sakriven Zapis"), [])
