Install Instructions
====================

Preparation
===========

Linux
-----

The needed packages are python = 2.6, postgresql >= 8.4 (client and
server), libxml2, libxslt, and freetype2 all with their respective dev
packages, a working compiler (usually gcc) and the pip, virtualenv and
bzr python programs.

Ubuntu
------

On ubuntu just do an apt-get for everything you will need:

$ sudo apt-get install build-essential python2.6-dev postgresql-8.4
libpq-dev libfreetype6-dev python-pip bzr libxml2-dev
python-virtualenv libxslt1-dev libjpeg62-dev liblcms1-dev libpng12-dev

Mac OSX
-------

Download and install postgresql(it includes pgadmin) from:

http://www.enterprisedb.com/products-services-training/pgdownload#osx

Download and install freetype from:

Download and install Bzr from:

http://wiki.bazaar.canonical.com/MacOSXDownloads

Download and install pip:

$ curl -O https://github.com/pypa/pip/raw/master/contrib/get-pip.py
$ sudo python get-pip.py

Windows
-------

TODO

Common Installation
===================

This part is common to linux/mac.

The first step is to create an openerp directory

$ mkdir openerp
$ cd openerp

For faster downloads from launchpad it is recommended that you have an
account on launchpad, submit your public ssh key and use "bzr
launchpad-login <launchpad-username>" to use the bzr+ssh protocol.

Download code from bazaar

$ bzr branch lp:openobject-server/6.0 server
$ bzr branch lp:openobject-addons/6.0 addons
$ bzr branch lp:openobject-addons/extra-6.0 addons-extra
$ bzr branch lp:openobject-client-web/6.0 web

And for the localization:
$ git clone https://github.com/proge/openerp-pt_br.git 

Remove l10n_br from addons, the one that comes with OpenERP is incomplete

$ rm -rf addons/l10n_br

Create postgresql user for OpenERP

$ sudo -u postgres -i
$ createuser --createdb --username postgres --no-createrole --pwprompt openuser
$ exit

Create a virtualenv to isolate OpenERP from the rest of the system
$ virtualenv --no-site-packages -p python2.6 oerp_venv
$ ./oerp_venv/bin/pip install -r openerp-pt_br/requirements.txt

The first time you start the OpenERP server you will pass some
parameters that get written to ~/.openerp_serverrc

$ ./oerp_venv/bin/python server/bin/openerp-server.py --db_user=openuser --db_host=127.0.0.1 --db_port=5432 --save --db_password=<PASSWORD>

Now close it with 'ctrl-c' and edit the ~/.openerp_serverrc:

$ nano ~/.openerp_serverrc

Go to the line that starts with  "addons_path = " and add all the
other addons repositories that were downloaded (addons, addons-extra
and openerp.pt-br-localiz-proge) separated by ",". For example, if my
install directory was /home/me/openerp the line should read:

addons_path =
/home/me/openerp/server/bin/addons,/home/me/openerp/addons,/home/me/openerp/addons-extra,/home/me/openerp/openerp-pt_br

Now save the file (ctrl+o in nano, cmd+s in textedit) and exit the
editor.

Now we are ready to go:

$ ./oerp_venv/bin/python server/bin/openerp-server.py

An to run the web front-end go to another terminal, or set the server
to be a background job (ctrl+d on bash):

$ ./oerp_venv/bin/python web/openerp-web.py


Brazilian Localization
======================

Create a new database
escolha lingua português(br)
entre no openerp e escolha a interface extendida e feche o wizard
va em administração->módulos->módulos
filtre os modulos por br (primeiro campo)
clique no icone de instalar em todos menos cep e os 3 ultimos (chart
of accounts e outros que tem br no nome mas não são da localização).
clique em applicar atualizações agendadas no menu e pronto.
um timeout vai acontecer mas não se preocupe, as atualizações
continuam no servidor, é só o cliente que esta parado

Creating init jobs
==================

TODO
