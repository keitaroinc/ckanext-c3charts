[![CI][]][1] [![Coverage][]][2] [![Gitter][]][3] [![Python][]][4] [![CKAN][]][5]

# Ckan Charts

This extension provides chart library that enables deeper integration of charts into CKAN applications.

## Installation

To install ckanext-c3charts:

1. Activate your CKAN virtual environment, for example:

```
. /usr/lib/ckan/default/bin/activate
```

2. Install the ckanext-c3charts Python package into your virtual environment:

```
pip install ckanext-c3charts
```

3. Add ``c3charts`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

```
sudo service apache2 reload
```

## Config settings

None at present

## Development Installation

To install ckanext-c3charts for development, activate your CKAN virtualenv
and do:

```
git clone https://github.com/ViderumGlobal/ckanext-c3charts.git
cd ckanext-c3charts
python setup.py develop
pip install -r dev-requirements.txt
```

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini --cov=ckanext.c3charts --disable-warnings ckanext/c3charts/tests

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)

  [CI]: https://github.com/keitaroinc/ckanext-c3charts/workflows/CI/badge.svg?branch=ckan-2.9
  [1]: https://github.com/keitaroinc/ckanext-c3charts/actions
  [Coverage]: https://coveralls.io/repos/github/keitaroinc/ckanext-c3charts/badge.svg?branch=ckan-2.9
  [2]: https://coveralls.io/github/keitaroinc/ckanext-c3charts?branch=ckan-2.9
  [Gitter]: https://badges.gitter.im/keitaroinc/ckan.svg
  [3]: https://gitter.im/keitaroinc/ckan?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
  [Python]: https://img.shields.io/badge/python-3.8-blue
  [4]: https://www.python.org
  [CKAN]: https://img.shields.io/badge/ckan-2.9-red
  [5]: https://www.ckan.org