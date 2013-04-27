"""
A timeline implementation that uses Redis and Redis lists
as the backing store for a timeline.

"""

from __future__ import absolute_import
from redis import StrictRedis

class RedisTimeline(object):
	_redis = None

	def __init__(self, **kwargs):
		"""
		Creates Redis object with key ``timelines:<id>``.
		"""

		name = kwargs.pop('name')
		prefix = kwargs.pop('prefix', "timelines")
		sep = kwargs.pop('sep', ":")
		
		self.name = "%s%s%s" % (prefix, sep, name)

		# Default to uncapped length
		self.max_length = kwargs.pop("max_length", 0)

		if self._redis is None:
			url = kwargs.get('url', None)

			if url is not None:
				self._redis = StrictRedis().from_url(url)
			else:
				self._redis = StrictRedis(**kwargs)

	def push(self, value):
		"""
		Adds the value to the front of the list and trim if the 
		max length != 0.
		"""

		self._redis.lpush(self.name, value)

		if self.max_length > 0:
			self._redis.ltrim(self.name, 0, self.max_length-1)

	def range(self, count=0, **kwargs):
		"""
		Returns a range values from the front of the list to the limit.
		"""

		redis = self._redis

		if count is 0:
			offset = kwargs.get('offset', 0)
			limit = kwargs.get('limit', -1)
		else:
			offset = 0
			limit = count

		if limit is 1: 
			# Get `range` of length 1 using 
			# LRANGE <timeline> <limit> <limit>
			limit = offset
		else:
			# Regular n-1 rules
			limit = limit - 1

		return redis.lrange(self.name, offset, offset+limit)

	def count(self):
		"""
		Uses Redis LLEN to get the length of the timeline.
		"""
		return self._redis.llen(self.name)

	@property
	def length(self):
		"""
		Access the length (count) as a property.
		"""
		return self.count()