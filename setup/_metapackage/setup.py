import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-project-reporting",
    description="Meta package for oca-project-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-project_task_report',
        'odoo12-addon-project_task_timesheet_report',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
