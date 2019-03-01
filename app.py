import responder


api = responder.API()


@api.route('/', default=True)
def hello_world(req, resp):
    api.redirect(resp, 'https://pmac.io/')


if __name__ == '__main__':
    api.run()
