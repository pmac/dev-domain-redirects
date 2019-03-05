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
    full_host = req.headers.get('host')
    host = 'NONE'
    if full_host:
        print(full_host)
        parts = full_host.split('.')
        if len(parts) == 2:
            host = parts[0]
            resp.html = api.template('home.html', host=host)
            statsd.incr(f'{host}.homepage')
            return

        if len(parts) == 3:
            host = parts[1]
            cname = parts[0]
            destination = None
            if host == 'mozillian':
                destination = f'https://mozillians.org/u/{cname}/'
            elif host in CNAMES and cname in CNAMES[host]:
                destination = CNAMES[host][cname]

            if destination:
                api.redirect(resp, destination)
                statsd.incr(f'{host}.cname.{cname}')
                return

            statsd.incr(f'{host}.cname.{cname}.404')

    resp.status_code = api.status_codes.HTTP_404
    resp.html = api.template('404.html')
    statsd.incr(f'{host}.404')


if __name__ == '__main__':
    api.run()
