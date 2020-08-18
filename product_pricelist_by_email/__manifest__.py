# © 2018-Today Aktiv Software (http://www.aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/

{
    "name": "Product Price list by Email",
    "summary": "Product price list by email",
    'description': """
        Admin users can receive product price list report on every Monday.
    """,
    "category": "Product",
    "version": "13.0.1.0.0",
    'license': "AGPL-3",
    'author': 'Aktiv Software',
    'website': 'http://www.aktivsoftware.com',
    "depends": [
        'sale_management'],
    "data": [
        'data/mail_template_data.xml',
        'data/pricelist_data.xml',
        'report/report_product_pricelist.xml'],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
