import re
from os import getenv

import responder
import toml
from statsd import StatsClient


api = responder.API()
statsd = StatsClient()
CNAMES = toml.load('cnames.toml')
STATSD_URL = getenv('STATSD_URL')
if STATSD_URL:
    match = re.match(r'^statsd://(\w+):(\d+)$', STATSD_URL)
    if match:
        statsd_host, statsd_port = match.groups()
        statsd = StatsClient(host=statsd_host, port=int(statsd_port))


@api.route('/', default=True)
def hello_world(req, resp):
    # full_host = req.headers.get('host')
    full_host = 'thepy.dev'
    if full_host:
        parts = full_host.split('.')
        host = parts[-2]
        if len(parts) == 2:
            resp.html = api.template('home.html', host=host)
            statsd.incr(f'{host}.homepage')
            return

        if len(parts) == 3:
            cname = parts[0]
            if host in CNAMES and cname in CNAMES[host]:
                api.redirect(resp, CNAMES[host][cname])
                statsd.incr(f'{host}.cname.{cname}')
                return

            statsd.incr(f'{host}.cname.{cname}.404')

    else:
        host = 'NONE'

    resp.status_code = api.status_codes.HTTP_404
    resp.html = api.template('404.html')
    statsd.incr(f'{host}.404')


if __name__ == '__main__':
    api.run()
