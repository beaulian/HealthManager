# -*- coding: utf-8 -*- 

from flask import jsonify


def healthmanager_error(error_code, **kwargs):
	error_code_map_message = {
		"2000": "need_confirm",
		"2001": "email_occupied",
		"2002": "username_occupied",
		"2003": "need_login",
		"2004": "auth_error",
		"2005": "no_such_uid",
		"2006": "wrong_token",
		"2007": "need_permission",
		"2008": "not_found",
		"2009": "missing_args",
		"2010": "image_too_large",
		"2011": "image_unknow",
		"2012": "image_wrong_format",
		"2013": "out_of_pages",
		"2014": "invalid_id",
		"2015": "create_family_occupied",
		"2016": "add_user_occupied",
		"2099": "unknow_error"
	}
	response = jsonify(
			dict({
	            "status": "failed",
	            "error_code": error_code,
	            "error_msg": error_code_map_message[error_code]
	        }, **kwargs)
		)
	response.status_code = 400
	return response