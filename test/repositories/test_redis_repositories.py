"""Test redis repositories"""
import hashlib

import redis

from crawl_foreign_business_data.repositories.redis_repositories import (
    RedisRepositories, get_md5)


def test_get_md5():
    """
    test_get_md5
    :return:
    """
    key = '1'
    result = get_md5(key)
    assert result == 'c4ca4238a0b923820dcc509a6f75849b'


def test_add_url():
    """
    test_add_url
    :return:
    """

    def del_set():
        redis_connect = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_connect.delete('key')

    def add():
        md5 = hashlib.md5()
        md5.update('foo'.encode('utf-8'))
        test_redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        test_redis.sadd('key', md5.hexdigest())

    del_set()
    assert RedisRepositories().add_url('bar')
    add()
    assert not RedisRepositories().add_url('foo')


def test_write_to_redis(mocker):
    """
    test_write_to_redis
    :param mocker:
    :return:
    """
    test_content = 'test'
    mock_add_url = mocker.patch.object(RedisRepositories, 'add_url')
    RedisRepositories().write_to_redis('test', test_content)

    mock_add_url.assert_called_with('test')
    assert 'test' in RedisRepositories().read_redis('test')


def test_rewrite():
    """
    test_rewrite
    :return:
    """
    RedisRepositories().rewrite('test', 'test_rewrite')
    assert 'test_rewrite' in RedisRepositories().read_redis('test')
