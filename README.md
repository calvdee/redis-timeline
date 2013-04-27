Description
===========

A generic timeline, Redis backend timeline.

Installation
============

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
    ['one', '1000', '999']
