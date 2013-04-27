Description
===========

A Redis-backed generic timeline implementation.

Installation
============

    git clone https://github.com/calvdee/redis_timeline.git
    pip install redis
    pip install hiredis
    
Getting Started
===============


    >>> from redis_timeline import RedisTimeline
    >>> t = RedisTimeline(name="test-timeline", max_length=1000)
    >>> t.push('one')
    'one'
    >>> t.push('two')
    'two'
    >>> t.push('three')
    'three'
    >>> r.range(3)
    ['three', 'two', 'one']
