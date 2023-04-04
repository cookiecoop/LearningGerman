setup(
    name="GermanWordsLearning",
    version="1.0.0",
    description="Learn German words",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cookiecoop/LearningGerman",
    author="Sevda Esen",
    author_email="...@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["test"],
    include_package_data=True,
    install_requires=[
        "tkinter"
    ],
    entry_points={"console_scripts": ["test=main"]},
)
