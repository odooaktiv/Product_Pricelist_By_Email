# -*- coding: utf-8 -*-

from odoo import api, fields, models
import base64
from datetime import datetime
from calendar import monthrange


class Pricelist(models.Model):
    """Class Inherited to send pricelist details."""

    _inherit = "product.pricelist"

    def sent_product_pricelist_by_email(self, attachment_id):
        """Method for Send mail when scheduler is run."""
        email_template = self.env.ref(
            'product_pricelist_by_email.email_template_pricelist')
        context = self._context
        current_uid = context.get('uid')
        user_id = self.env['res.users'].browse(current_uid)
        email_to = ''
        for user in self.env['res.users'].search([]):
            if user.has_group('base.group_user') and user.has_group(
                    'sales_team.group_sale_manager'):
                email_to += (',' + user.partner_id.email)
        if email_template:
            email_template.attachment_ids = attachment_id
            email_template.write({
                'email_from': user_id.email or self.company_id.email})
            ctx = {
                'user': user_id.name,
                'company': user_id.partner_id.company_id.name
            }
            email_template.email_to = email_to or ''
            email_template.with_context(ctx).send_mail(
                self.id, raise_exception=False, force_send=True)

    def get_items(self, pricelist):
        """Get Pricelist Items."""
        pricelist_id = self.env['product.pricelist'].browse(pricelist)
        date_value = datetime.today().date()
        month_date_end = date_value.replace(day=monthrange(
            date_value.year, date_value.month)[1])
        first_day_of_month = date_value.replace(day=1)
        item = []
        for items in pricelist_id.item_ids:
            if items.date_end:
                if items.date_end >= first_day_of_month and items.date_end <= month_date_end:
                    item.append(items)
            if not items.date_start or not items.date_end:
                item.append(items)
        return item

    @api.model
    def cron_create_product_pricelist_report(self):
        """"generate pdf every week from cron job."""
        report = 'product_pricelist_by_email.action_report_product_pricelist'
        pricelist_obj = self.env['product.pricelist'].search([])
        date_value = datetime.today().date()
        month_date_end = date_value.replace(day=monthrange(
            date_value.year, date_value.month)[1])
        first_day_of_month = date_value.replace(day=1)
        pricelist = []
        pricelist = [
            item.pricelist_id.id for item in pricelist_obj.item_ids.search([
                ('date_end', '>=', first_day_of_month),
                ('date_end', '<=', month_date_end)])]
        pricelist += [
            item.pricelist_id.id for item in pricelist_obj.item_ids.filtered(
                lambda x: not x.date_start or not x.date_end)]
        # items = [item for item in pricelist_obj.item_ids.search([
        #     ('date_end', '>=', first_day_of_month),
        #     ('date_end', '<=', month_date_end)])]
        # for item in pricelist_obj.item_ids:
        #     print ("\n\n Item :::::::::::: Item", item)
        #     if not item.date_start or not item.date_end:
        #         print("\n\n item!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", item.pricelist_id)
        pricelist_ids = pricelist_obj.browse(set(pricelist))
        print("\n\n item!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", pricelist_ids)
        # print (ll)
        pdf = self.env.ref(report).render_qweb_pdf(pricelist_ids.ids)
        b64_pdf = base64.b64encode(pdf[0])
        attachment = "Pricelist" + ' - ' + str(fields.Date.today())
        attachment_id = self.env['ir.attachment'].create({
            'name': attachment,
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': attachment,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })
        self.sent_product_pricelist_by_email(attachment_id)
