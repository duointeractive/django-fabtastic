django-fabtastic
================

Deploying Django_ projects is not an inherently fun task. It's not an
extremely difficult process, however, there are plenty of tedious, repetitive 
tasks that take precious time and keystrokes.

Each person or company handles their deployments in a slightly different
manner. There are a near infinite number of ways to deploy, maintain, and
update Django projects, each with their own benefits and limitations.
django-fabtastic is `DUO Interactive`_'s 
philosophy on deployment, and is what we use for our own projects. 

This Django_ app can be dropped into any project, providing you with a quick, 
easy, standardized deployment method.

Why would I use fabtastic?
--------------------------

These are just based on what we wanted in a deployment system, so you may not
find these to be compelling reasons for your project(s).

* We like Python_, and wanted a simple Python-based deployment solution.
* We like Fabric_. It's simple and works really well for us.
* We did not like maintaining a mess of slightly different fabfiles for our
  handful of projects in production and development. Whenever an enhancement
  was made to one, we had to spend time porting it to the other projects for
  them to benefit from the enhancements.
* Our deployments were similar enough to pretty much do the same exact
  steps to deploy them all. We can now toss the example fabfile.py into each
  of our projects, add fabtastic to our Django_ settings.py, and we're on
  our way to worrying about more important stuff like developing the product.
  
Notes and assumptions
---------------------

django-fabtastic does not attempt to be a one-size-fits-all solution. It is
aimed at what we need for our deployments. As is such, if you need a feature
implemented, feel free to open an issue in the tracker, or better yet,
fork and send a pull request.

As far as assumptions we make for those wishing to use this app:

* You are running Django_ 1.1 or higher.
* We strongly recommend Python_ 2.6+, but not 3.x (yet). It very well may run
  just fine on earlier Python versions, but we have done no testing below
  Python 2.6.
* You are using or wanting to use Fabric_.
* We currently only implement Postgres DB operations. We'd love patches for
  others, though.
* You are using virtualenv_ and virtualenvwrapper_.
  
Philosophy
----------

We like Django. We like Fabric. Fabric is [thankfully] not at all tied to
Django, which is great. However, we found ourselves juggling Django
settings and environment stuff way too often. We also found ourselves wishing
we could just run certain segments of the deployment process in-place on
an arbitrary server or staging or development machine without any thought.

Fabric *can* do this just fine, but we didn't like cluttering our
fabfile with all of the extra sub-sections of our deployment process. We also
realized that our deployment scripts being ran entirely from a client machine
meant that some really bad assumptions were being made:

* The values in all of our local settings.py (and deployment/staging settings)
  are always in sync with what's in production.
* No overridden (local_settings.py, anyone?) values exist in production.

These caused us some grief, as we tend to keep sensitive settings out of our
git repositories. The best way to overcome the aformentioned limitations and
correct our assumptions was to chunk the deployment process out into
manage.py commands and some includable Fabric scripts that call them as needed.

In this way, we find ourselves with a useful set of management and deployment
commands that are guaranteed to always have the correct settings and
Django environment on all of our machines: local, staging, or production.

Installation
------------

Right now, Fabtastic is only available via our github repository. Fortunately,
``pip`` can pull directly from it.

* Add ``git+http://github.com/duointeractive/django-fabtastic.git#egg=fabtastic``
  to your requirements.txt file.
* Run ``pip install git+http://github.com/duointeractive/django-fabtastic.git#egg=fabtastic``
  manually to install it.
* Add ``fabtastic`` to your `INSTALLED_APPS`` in settings.py.
* If you run ``./manage.py help``, you should now see some more commands.
* Read on to the fabfile.py construction section in this README. Generally you
  can copy the `example fabfile.py`_ to your project and modify it as needed.
  
.. _example fabfile.py: http://github.com/duointeractive/django-fabtastic/blob/master/examples/fabfile.py

Staying up to date
------------------

At any time, you may run ``./manage.py ft_fabtastic_update`` to get the latest
version. There is also a Fabric task included, ``fabtastic_update``.

fabfile.py Construction
-----------------------

If you downloaded the source distribution, take a look at your ``examples/``
directory. The most common example will be in ``fabfile.py``. If you installed
via pip, you can point your browser at it here_ to follow along.

.. _here: http://github.com/duointeractive/django-fabtastic/blob/master/examples/fabfile.py

The important thing to note is that all we are doing in the fabfile is pulling
whatever we want together. You are free to mix in your own custom commands,
selectively use ours, or use all of ours plus some of your own.

django-fabtastic is primarily for DUO's deployments, so some of it is aimed to
fit our usage case. As is such, unless you use all of our dependencies, the
following line might need to be made a little more specific::

    from fabtastic.fabric.commands import *

It is important to note that you can selectively import commands from
``fabtastic.fabric.commands``. See the note and example in ``examples/fabfile.py``.
For a full list of modules, check your ``fabtastic/fabric/commands`` directory,
or look at our `git repository`_.

.. _git repository: http://github.com/duointeractive/django-fabtastic/tree/master/fabtastic/fabric/commands/
 
.. _Python: http://python.org
.. _DUO Interactive: http://duointeractive.com
.. _Fabric: http://docs.fabfile.org/
.. _Django: http://djangoproject.com
