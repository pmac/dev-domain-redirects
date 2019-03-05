import re
from os import getenv

import responder
import toml
from statsd import StatsClient


api = responder.API()
statsd = StatsClient()
CNAMES = toml.load('cnames.toml')['cnames']
STATSD_URL = getenv('STATSD_URL')
if STATSD_URL:
    match = re.match(r'^statsd://(\w+):(\d+)$', STATSD_URL)
    if match:
        statsd_host, statsd_port = match.groups()
        statsd = StatsClient(host=statsd_host, port=int(statsd_port),
                             prefix='thepy-dev')


@api.route('/', default=True)
def hello_world(req, resp):
    host = req.headers.get('host')
    if host:
        parts = host.split('.')
        if len(parts) == 2:
            resp.text = 'Apex domain. Template goes here.'
            statsd.incr('homepage')
            return

        if len(parts) == 3:
            cname = parts[0]
            if cname in CNAMES:
                api.redirect(resp, CNAMES[cname])
                statsd.incr(f'cname.{cname}')
                return

    resp.status_code = api.status_codes.HTTP_404
    statsd.incr('404')


if __name__ == '__main__':
    api.run()
