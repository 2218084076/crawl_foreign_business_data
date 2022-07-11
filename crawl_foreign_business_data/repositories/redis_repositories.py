import hashlib
import logging

import redis

logger = logging.getLogger(__name__)


class RedisRepositories:
    """redis repositories"""

    def __init__(self):
        self.redis_content = redis.StrictRedis(
            host='127.0.0.1',
            port=6379,
            db=0,
            decode_responses=True)

    def add_url(self, url: str):
        res = self.redis_content.sadd('key', get_md5(url))

        if res == 0:
            return False
        else:
            return True

    def write_to_redis(self, name: str, content: str):
        """
        write to redis
        :param name:
        :param content:
        """
        if self.add_url(content):
            self.redis_content.lpush(name, content)
        logger.debug('write to %s %s' % (name, content))

    def read_redis(self, name: str):
        end_num = self.redis_content.llen(name)
        content_list = self.redis_content.lrange(name, 0, end_num)

        return content_list

    def rewrite(self, name: str, content: str):
        """
        rewrite
        :param name:
        :param content:
        :return:
        """
        self.redis_content.lpush(name, content)


def get_md5(val):
    """
    把目标数据进行哈希，用哈希值去重更快
    :param val:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()
