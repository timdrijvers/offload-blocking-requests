from flask import Flask, make_response
from flask_redis import FlaskRedis
import time
import uwsgi

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
redis_store = FlaskRedis(app)

DURATION = 10


class Data:
    @classmethod
    def get(cls, key):
        d = redis_store.get('data-{}'.format(key))
        if d:
            return float(d.decode("utf-8"))
        return d

    @classmethod
    def new(cls):
        counter = redis_store.incr('counter')
        redis_store.set('data-{}'.format(counter), time.time())
        return counter


@app.route('/create_blocking')
def create_blocking():
    time.sleep(DURATION)
    return 'Hello world!'


@app.route('/status')
def status():
    return 'OK'


@app.route('/create_uwsgi')
def create_uwsgi():
    new_id = Data.new()
    uwsgi.add_var("OFFLOAD_TO_POLLER", "y")
    uwsgi.add_var("POLLER_ID", str(new_id))
    return make_response('id: {}'.format(new_id), 200, {})


@app.route('/create_nginx', methods=['GET', 'POST'])
def create_nginx():
    new_id = Data.new()
    return make_response(
        'id: {}'.format(new_id),
        418,
        {
            'X-OffloadToPoller-Url': '/poll',
            'X-OffloadToPoller-Args': str(new_id)
        }
    )


@app.route('/poll/<int:poll_id>/<call_try>', methods=['GET', 'POST'])
def poll(poll_id, call_try):
    ttl = Data.get(poll_id)
    if ttl is None:
        return ('', 404)
    elif time.time() - ttl < DURATION:
        return ('ttl: {}'.format(time.time() - ttl), 400)
    else:
        return 'Poll response {}'.format(poll_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
