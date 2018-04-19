import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-project-reporting",
    description="Meta package for oca-project-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-project_billing_utils',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
