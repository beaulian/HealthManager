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