import setuptools
setuptools.setup(
     name='export_garmin',  
     version='0.1',
     entry_points={
         'console_scripts': ['export_garmin=export_garmin:main'],
     },
     author='Daniel Margolis',
     author_email='dan@af0.net.',
     description='Backup Garmin activities to TSX files',
     long_description=open('README.md', 'r').read(),
     long_description_content_type='text/markdown',
     url='https://github.com/danmarg/export_garmin',
     packages=setuptools.find_packages(
         include=['export_garmin', 'export_garmin.*'],
     ),
     classifiers=[
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
     ],
     install_requires=[
         'garminconnect',
         'garth',
         'requests',
    ],
 )
