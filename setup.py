from setuptools import setup, find_packages

setup(
    name="atui",
    version="0.1.2",
    packages=find_packages(),  # Это автоматически найдет все пакеты и модули
    description="A UI development library with markup lenguage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucifer",
    author_email="at2823743@gmail.com",
    url="https://github.com/Lucifer13072/ATUI",  # Укажи, если у тебя есть репозиторий на GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Версия Python
    install_requires=[],  # Список зависимостей
)