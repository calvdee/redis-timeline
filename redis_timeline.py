"""
A timeline implementation that uses Redis lists
to represent the timeline.

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
		self.max_length = kwargs.get("max_length", 0)

		if self._redis is None:
			url = kwargs.get('url', None)

			if url is not None:
				self._redis = StrictRedis().from_url(url)
			else:
				self._redis = StrictRedis(**kwargs)

	def push(self, value):
		"""
		Adds the value to the front of the list

		"""
		redis = self.__redis.get_connection()

		redis.lpush(self.name, value)
		redis.ltrim(self.name, 0, self.max_length-1)

	def get_range(self, offset=0, limit=-1):
		"""
		Returns a range values from the list

		"""
		redis = self.__redis.get_connection()

		if limit is 1: 
			limit = offset
		else:
			limit = limit - 1

		return redis.lrange(self.name, offset, offset+limit)

	def count(self):
		return self.__redis.get_connection().llen(self.name)

	def _clean_space(self, value, char="-"):
	    """
	    Returns a lowercase string with spaces replaced by
	    char. Defaults to replacing with an underscore.

	    """
	    return value.lower().replace(" ", char)

	@property
	def length(self):
		return self.count()