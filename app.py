import responder


api = responder.API()


@api.route('/', default=True)
def hello_world(req, resp):
    resp.media = dict(**req.headers)


if __name__ == '__main__':
    api.run()
