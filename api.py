import responder
import base64

api = responder.API()


@api.route("/")
async def index(req, resp):

    data = await req.media()
    binary = data['image']
    img = base64.b64decode(binary)

    # face_recognition
    ## TBD
    # bokashi
    bokashi = ''

    img_base64 = base64.b64encode(bokashi)
    resp.media = {"Image_base64": img_base64}


if __name__ == '__main__':
    api.run(address='0.0.0.0')
