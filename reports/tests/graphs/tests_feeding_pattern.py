# -*- coding: utf-8 -*-
import datetime as dt

from django.test import TestCase
from django.utils import timezone

from core import models
from reports.graphs import feeding_pattern


class FeedingPatternTestCase(TestCase):
    def setUp(self):
        self.original_tz = timezone.get_current_timezone()
        self.tz = dt.timezone(dt.timedelta(days=-1, hours=1))
        timezone.activate(self.tz)

    def tearDown(self):
        timezone.activate(self.original_tz)

    def test_feeding_pattern(self):
        c = models.Child(birth_date=dt.datetime.now())
        c.save()

        models.Feeding.objects.create(
            child=c,
            start=dt.datetime(2000, 1, 1, 0, 0, tzinfo=dt.timezone.utc),
            end=dt.datetime(2000, 1, 1, 0, 1, tzinfo=dt.timezone.utc),
        )

        feeding_pattern(models.Feeding.objects.order_by("start"))
