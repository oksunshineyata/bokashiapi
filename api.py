import responder

api = responder.API()


@api.route("/")
def index(req, resp):
    resp.text = "Hello,World!"


if __name__ == '__main__':
    api.run(address='0.0.0.0')
