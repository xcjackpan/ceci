To deploy to ElasticBeanstalk, we want a folder structure of:

root
  -- application.py
  -- other stuff

_application.py_ in the root level is what is executed. Just provide a callable _application_ object in there so EB can find it.