from unittest import TestCase
from redis_timeline import RedisTimeline

class RedisTimelineTest(TestCase):
    def test_create_timeline(self):
        timeline = RedisTimeline(name="test-timeline")
        key = "timelines:test-timeline"
        
        self.assertEqual(timeline.name, key, "Key is: %s" % timeline.name)


    # def test_timeline_no_exist(self):
    #     timeline = RedisTimeline(name="doesnotexist")
    #     length = timeline.length

    #     self.assertEqual(
    #         length, 0, "Empty timeline length is not %s not 0" % length)