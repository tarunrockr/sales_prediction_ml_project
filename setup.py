from setuptools import find_packages, setup

hyphen_e = "-e ."
def get_requirements(file_name):
    with open(file_name) as file:
        lines = [ line.rstrip() for line in file]
    if hyphen_e in lines:
        lines.remove(hyphen_e)
    return  lines

# print(get_requirements('requirements.txt'))
# Metadata information for the project
setup(
    name = 'big_mart_sales_prediction',
    version = '0.0.1',
    author = 'Name',
    author_email = 'dummy@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)