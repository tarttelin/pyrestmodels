pyrestmodels
============

A python client library for consuming XML and JSON REST apis. The syntax is based on the Django style of declarative models. Although based on Django models, it has no dependency on Django.

## Dependencies ##

If you have lxml installed, then it will use lxml for all xml parsing and xpath.  If not, then it will use the bundled py-dom-xpath, which is a comparatively slow pure python xpath library.

## Test Driven ##

All the source code was written test first which, in addition to any benefits to design and quality, also provides an excellent set of examples on how to use the apis. 

## Documentation ##

The [documentation can be found here](http://tarttelin.github.com/pyrestmodels/)