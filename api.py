import responder
import base64
from PIL import Image, ImageFilter
import face_recognition
from io import BytesIO

api = responder.API()
img_path = './image.jpg'


@api.route("/")
async def index(req, resp):

    data = await req.media()
    binary = data['image']
    name = data['name']
    img = base64.b64decode(binary)
    with open(img_path, 'wb') as f:
        f.write(img)

    # face_recognition
    face_locations = get_face_locations(img_path)
    faces = extract_faces(face_locations, img_path)
    filtered_faces = mosaic(faces)

    mosaic_img = embed_filtered_faces(img_path, filtered_faces, face_locations)

    buffered = BytesIO()
    mosaic_img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue())

    img_utf_8 = img_base64.decode("utf-8")

    if len(face_locations) == 0:
        resp.media = {"image": img_utf_8, 'name': name, "status": "No detection"}
    else:
        resp.media = {"image": img_utf_8, 'name': name}


@api.route("/cnn")
async def cnn(req, resp):

    data = await req.media()
    binary = data['image']
    name = data['name']
    img = base64.b64decode(binary)
    with open(img_path, 'wb') as f:
        f.write(img)

    # face_recognition
    face_locations = get_face_locations(img_path, 'cnn')
    faces = extract_faces(face_locations, img_path)
    filtered_faces = gaussian_blur(faces)

    blur_img = embed_filtered_faces(img_path, filtered_faces, face_locations)

    buffered = BytesIO()
    blur_img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue())

    img_utf_8 = img_base64.decode("utf-8")

    if len(face_locations) == 0:
        resp.media = {"image": img_utf_8, 'name': name, "status": "No detection"}
    else:
        resp.media = {"image": img_utf_8, 'name': name}


def get_face_locations(img_path, model=None):
    image = face_recognition.load_image_file(img_path)
    if model is not None:
        face_locations = face_recognition.face_locations(image, model='cnn')
    else:
        face_locations = face_recognition.face_locations(image)
    return face_locations


def extract_faces(face_locations, img_path):
    img = face_recognition.load_image_file(img_path)
    faces = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = img[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        faces.append(pil_image)
    return faces


def gaussian_blur(faces):
    filtered_faces = []
    for face in faces:
        filtered_face = face.filter(ImageFilter.GaussianBlur(10.0))
        filtered_faces.append(filtered_face)

    return filtered_faces


def embed_filtered_faces(img_path, filtered_faces, face_locations):
    img = face_recognition.load_image_file(img_path)
    img = Image.fromarray(img)
    for i in range(len(filtered_faces)):
        face = filtered_faces[i]
        top, _, _, left = face_locations[i]
        img.paste(face, (left, top))

    return img


def mosaic(faces):
    mosaics = []
    for face in faces:
        mosaic_face = face.resize([x // 8 for x in face.size]).resize(face.size)
        mosaics.append(mosaic_face)

    return mosaics


if __name__ == '__main__':
    api.run(address='0.0.0.0', debug=True)
