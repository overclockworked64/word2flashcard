from setuptools import setup


setup(
    name='word2flashcard',
    version='0.1.0',
    author='overclockworked64',
    author_email='overclockworked64@users.noreply.github.com',
    description=('A tool to fetch words from Cambridge Dictionary and make flashcards out of it.'),
    license='MIT',
    keywords='cambridge obsidian dictionary flashcard',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'word2flashcard=app:sync_main'
        ],
    },
    install_requires=[
          'trio',
          'trio-parallel',
          'asks',
          'bs4',
          'lxml'
      ],
)