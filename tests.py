from unittest import TestCase
from redis_timeline import RedisTimeline
from redis import Redis

class RedisTimelineTest(TestCase):
    def setUp(self):
        """
        Create the RedisTimeline client
        """

        self.key ="timelines:test-timeline"
        self.timeline = RedisTimeline(name="test-timeline", max_length=1000)
        
        self.assertEqual(self.timeline.name, self.key)

    def cleanUp(self):
        self.timeline._redis.delete(self.key)

    def test_push(self):
        """
        Create a Redis timeline and check it.
        """
        timeline = self.timeline

        [timeline.push(x) for x in range(1,10)]

        # Test kwargs
        self.assertEqual(len(timeline.range(offset=0,limit=5)) ,5)

        # Test by count
        self.assertEqual(len(timeline.range(5)), 5)

    def test_pop(self):
        pass

    def test_trim(self):
        """
        Push max+1 items onto the timeline and make sure lengh
        is still max_length for RedisTimeline.
        """

        timeline = self.timeline

        [timeline.push(x) for x in range(1,1000+1)]        

        # Make sure the list was trimmed
        self.assertEqual(timeline.count(), timeline.max_length)