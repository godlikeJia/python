import redis
import time
r = redis.StrictRedis(host='192.168.159.128', port=6379, db=0)


"""STRING"""
print("**********STRING***************")
r.delete('foo')
r.set('foo', 'bar')
r.append('foo', 'rab')

if not r.get('foo'):
	print("no key named 'foo'")
else:
	print(r.get('foo'))


"""LIST"""
print("**********LIST***************")
r.delete("tlist")
r.rpush("tlist", "123")
print("return value is list length:", r.rpush("tlist", "345"))
r.lpush("tlist", "000")

print(r.lrange("tlist", 0, -1))

while True:
	print(r.lindex("tlist", 0))
	ret = r.lpop("tlist")
	if ret:
		print(ret)
	else:
		break

"""SET"""
print("**********SET***************")
r.sadd("tset", "abc")
r.sadd("tset", "def")
print(r.smembers("tset"))
if r.sismember("tset", "abc"):
	print("'abc' in 'test'")
	r.srem("tset", "abc")
else:
	print("'abc' not in 'test'")
print(r.smembers("tset"))

"""HASH"""
print("**********HASH***************")
r.hset("hkey", "subkey", "hvalue")
r.hset("hkey", "subkey", "hvalue2")
r.hset("hkey", "subkey2", "hvalue")
print(r.hget("hkey", "subkey2"))
print(r.hgetall("hkey"))
print(r.hdel("heky", "subkey"))

"""ZSET"""
print("**********ZSET***************")
r.zadd("zkey", 1.2, "one-dot-two")
r.zadd("zkey", 1.3, "ont-dot-three")
r.zadd("zkey", 2.3, "two-dot-three")
print(r.zrange("zkey", 0, 1))
print(r.zrangebyscore("zkey", 1.3, 2.3))
print(r.zrem("zkey", "two-dot-three"))
print(r.zrangebyscore("zkey", 1.3, 2.3))


"""VOTE Example"""
print("**********VOTE Example***************")
ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432
def article_vote(conn, user, article):
	cutoff = time.time() - ONE_WEEK_IN_SECONDS
	if conn.zscore("time:", article) < cutoff:
		return
	article_id = article.partition(':')[-1]
	if conn.sadd('voted:'+article_id, user):
		conn.zincrby('score:', article, VOTE_SCORE)
		conn.hincrby(article, 'votes', 1)


def post_article(conn, user, title, link):
	article_id = str(conn.incr('article:'))
	voted = 'voted:' + article_id
	conn.sadd(voted, user)
	conn.expire(voted, ONE_WEEK_IN_SECONDS)
	now = time.time()
	article = 'article:' + article_id
	conn.hmset(article, {'title': title,
						'link': link,
						'poster': user,
						'time': now,
						'votes': 1,
			   })
	conn.zadd('score:', now + VOTE_SCORE, article)
	conn.zadd('time:', now, article)
	return article_id

ARTICLES_PER_PAGE = 25
def get_articles(conn, page, order='score:'):
	start = (page-1) * ARTICLES_PER_PAGE
	end = start + ARTICLES_PER_PAGE - 1
	ids = conn.zrevrange(order, start, end)
	articles = []
	for id in ids:
		article_data = conn.hgetall(id)
		article_data['id'] = id
		articles.append(article_data)
	return articles

def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
	article = 'article:' + article_id
	for group in to_add:
		conn.sadd('group:' + group, article)
	for group in to_remove:
		conn.srem('group:' + group, article)
post_article(r, 'user1', 'how to begin Python', 'http://how-to-begin-python')


def clearRedisDB(r):
	for key in r.keys("*"):
		r.delete(key)
clearRedisDB(r)
