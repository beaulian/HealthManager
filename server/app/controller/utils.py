# -*- coding: utf-8 -*-


def change_object_attr(e_dict):
    for key, value in e_dict.iteritems():
        if isinstance(value, dict):
            e_dict[key] = change_object_attr(value)
        else:
            if key == "_id":
                e_dict["id"] = str(value)
                del e_dict[key]
    return e_dict


def get_specific_info(cursor_object, *args):
    args = list(args)
    args.append("_id")
    entitys = []
    for entity in cursor_object:
        entitys.append(dict([(key, entity[key]) for key in args if key in entity]))
    if len(entitys) == 1:
        return entitys[0]
    return entitys


def allow_image(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ["jpg", "jpeg", "gif", "png"]


def save_img(img_file, img_width, img_dir):
    import os
    import hashlib
    from PIL import Image
    from config import basedir

    im = Image.open(img_file)
    width, hight = im.getbbox()[2], im.getbbox()[3]
    if width > img_width:
        im = im.resize((img_width, hight * img_width / width), Image.ANTIALIAS)

    img_url = img_dir + hashlib.md5(img_file.filename).hexdigest() \
    						  + "." + img_file.filename.rsplit(".", 1)[1]
    im.save(os.path.join(basedir, "app"+img_url))

    return img_url


def delete_img(img_file):
    import os
    from config import basedir

    target_file = os.path.join(basedir, "app"+img_file)
    if os.path.isfile(target_file):
        os.remove(target_file)
