from setuptools import setup

kwargs = {
    'name': 'django-xtags',
    'version': '0.4',
    'description': 'Django tagging framework, easy registering, clouds, merging, autocomplete.',
    'author': 'Tartnskyi Vladimir',
    'author_email': 'fon.vosi@gmail.com',
    'url': 'https://github.com/vosi/django-xtags',
    'keywords': 'django,tagging',
    'license': 'BSD',
    'packages': ['xtags',],
    'include_package_data': True,
    'install_requires': ['setuptools'],
    'zip_safe': False,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
}
setup(**kwargs)
