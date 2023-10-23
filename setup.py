from setuptools import find_packages, setup

package_name = 'race_line_optimizer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/race_line_optimizer_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aklein5',
    maintainer_email='aklein5@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'race_line_optimizer = race_line_optimizer.race_line_optimizer:main',
        ],
    },
)
