#!/usr/bin/python
# -*- coding: UTF-8 -*- 

activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


from controller import create_app
app = create_app()


if __name__ == '__main__':
	app.run()