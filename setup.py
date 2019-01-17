import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='sunshine',  
     version='1.0dev',
     scripts=['sunshine'] ,
     author="Brian Arbuckle",
     author_email="brian@brianarbuckle.com",
     description="A Solar Calculator",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/tzujan/sunshine",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
