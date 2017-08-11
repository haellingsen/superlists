from fabric.api import run
from fabric.context_managers import settings

def _get_manage_dot_py(host):
	return '~/sites/%s/virtualenv/bin/python ~/sites/%s/source/manage.py' % (host,)

def reset_database(host):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string='ubuntu@%s' % (host,)):
		run('%s flush --noinput' % (manage_dot_py,))

def create_session_on_server(host, email):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string='ubuntu@%s' % (host,)):
		session_key = run('%s create_session %s' % (manage_dot_py,email,))
		return session_key.strip()