import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'depends_override': {
            'formio': False,
            'formio_storage_filestore': False,
        },
    }
)
