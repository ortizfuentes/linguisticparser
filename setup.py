import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='linguisticparser',
    version='0.0.1',
    description='Text parser that segments into paragraphs, orthographic sentences and words. Not to be confused with acronyms or abbreviations. It allows the transformation of information into dataframes.',
    long_description=long_description,
    url='git@github.com:ortizfuentes/linguisticparser',
    author='Jorge Ortiz Fuentes',
    author_email='jorge@ortizfuentes.com',
    license='unlicense',
    packages=setuptools.find_packages(),
    zip_safe=False
)
