import responder
import toml


api = responder.API()
CNAMES = toml.load('cnames.toml')['cnames']


@api.route('/', default=True)
def hello_world(req, resp):
    host = req.headers.get('host')
    if host:
        parts = host.split('.')
        if len(parts) == 2:
            resp.text = 'Apex domain. Template goes here.'
            return

        if len(parts) == 3:
            cname = parts[0]
            if cname in CNAMES:
                api.redirect(resp, CNAMES[cname])
                return

    resp.status_code = api.status_codes.HTTP_404


if __name__ == '__main__':
    api.run()
