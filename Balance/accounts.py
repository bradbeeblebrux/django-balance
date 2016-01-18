# -*- coding: utf-8 -*-

import xlrd
import datetime
import xml.etree.ElementTree as ET
from lxml import etree
from django.utils.translation import ugettext as _


class ParsedTransaction:

    def __init__(self, date, desc, reference, amount=0.0):
        self.date = date
        self.desc = desc
        self.reference = reference
        self.amount = amount

    # def __init__(self, **kwargs):
    #     self.date = kwargs.get('date', None)
    #     self.desc = kwargs.get('desc', None)
    #     self.reference = kwargs.get('reference', None)
    #     self.debit = kwargs.get('debit', 0.0)
    #     self.credit = kwargs.get('credit', 0.0)

    def __unicode__(self):
        return "(%s, %s, %s, %.2f)" %(self.date, self.desc, self.reference, self.amount)

    def __str__(self):
        return unicode(self).encode('utf-8')

# class BankAccount(object):
#     __metaclass__ = ABCMeta
#
#     def __init__(self):
#         self.trans_list = []
#
#     @abstractmethod
#     def parseFile(self, filename):
#         pass


def LeumiBankParser(filename):
    workbook = xlrd.open_workbook(filename.name, file_contents=filename.read())
    worksheet = workbook.sheet_by_index(0)
    curr_row = 15
    trans_list = []

    while curr_row < worksheet.nrows:
        row = worksheet.row(curr_row)
        if all([not x.value for x in row]):
            break

        date = worksheet.cell_value(curr_row, 0)
        desc = worksheet.cell_value(curr_row, 1) #.encode('utf-8')
        reference = worksheet.cell_value(curr_row, 2)
        amount = 0

        if worksheet.cell_type(curr_row, 3) != xlrd.XL_CELL_EMPTY:
            amount = -1 * float(worksheet.cell_value(curr_row, 3))

        if worksheet.cell_type(curr_row, 4) != xlrd.XL_CELL_EMPTY:
            amount = float(worksheet.cell_value(curr_row, 4))

        tmp_trans = {'date': datetime.datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'),
                     'desc': desc,
                     'reference': reference,
                     'amount': amount,
                     }

        t = ParsedTransaction(**tmp_trans)
        trans_list.append(t)
        curr_row += 1

    return trans_list

def DiscountBankParser(filename):
    workbook = xlrd.open_workbook(filename.name, file_contents=filename.read())
    worksheet = workbook.sheet_by_index(0)
    curr_row = 13
    trans_list = []
    empty_row = [xlrd.empty_cell]*7

    while curr_row < worksheet.nrows:
        row = worksheet.row(curr_row)
        if str(row) == str(empty_row):
            break

        date = worksheet.cell_value(curr_row, 0)
        desc = worksheet.cell_value(curr_row, 3)
        amount = float(worksheet.cell_value(curr_row, 5))

        tmp_trans = {'date': datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d'),
                     'desc': desc,
                     'reference': '',
                     'amount': amount,
                     }

        t = ParsedTransaction(**tmp_trans)
        trans_list.append(t)
        curr_row += 1

    return trans_list

def LeumiCardParser(filename):
    trans_list = []
    ns = {'leumicard': 'urn:schemas-microsoft-com:office:spreadsheet'}
    root = ET.fromstring(filename.read())
    worksheet = root.find('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet').find('{urn:schemas-microsoft-com:office:spreadsheet}Table')
    rows = worksheet.findall('leumicard:Row', ns)
    for row in rows[1:]:
        cells = row.findall('leumicard:Cell', ns)
        #data = cells[0].find('leumicard:Data', ns)

        desc = cells[2][0].text
        amount = float(cells[6][0].text)
        full_amount = float(cells[5][0].text)
        remark = ''
        if cells[7][0].text is not None:
            remark = cells[7][0].text
        if amount != full_amount:
            desc = ', '.join([desc, cells[3][0].text, cells[5][0].text, remark])

        tmp_trans = {'date': datetime.datetime.strptime(cells[0][0].text, '%Y-%m-%dT00:00:00').strftime('%Y-%m-%d'),
                     'desc': desc,
                     'reference': cells[2][0].text,
                     'amount': -1 * amount,
                     }

        t = ParsedTransaction(**tmp_trans)
        trans_list.append(t)

    return trans_list


def VisaCalParser(filename):
    trans_list = []
    tree = etree.HTML(filename.read())
    table = tree.xpath("//td[@id='tdCalGrid']")[0].getchildren()[0]
    for row in table.getchildren()[1]:
        tds = row.getchildren()
        if len(tds) != 7:
            continue

        if tds[0].text is None:
            desc = tds[1].find('span').text
            amount = float(tds[4].find('span').text.replace(',', ''))
            symbol_amount = tds[5].text
            full_amount = float(tds[2].find('span').text.replace(',', ''))
            symbol_full_amount = tds[3].text
            purchase_date = tds[0].find('span').text
            reference = tds[1].find('span').text
        else:
            desc = tds[1].text
            amount = float(tds[4].text.replace(',', ''))
            symbol_amount = tds[5].text
            full_amount = float(tds[2].text.replace(',', ''))
            symbol_full_amount = tds[3].text
            purchase_date = tds[0].text
            reference = tds[1].text

        if amount != full_amount:
            if symbol_amount != symbol_full_amount:
                str_full_amount = "%s%s" % (full_amount, symbol_full_amount)

            tmp = [desc, str_full_amount, tds[6].text]
            desc = ', '.join(filter(None, tmp))

        tmp_trans = {
                'date': datetime.datetime.strptime(purchase_date, '%d/%m/%y').strftime('%Y-%m-%d'),
                'desc': desc,
                'reference': reference,
                'amount': -1*amount,
        }

        t = ParsedTransaction(**tmp_trans)
        trans_list.append(t)

    return trans_list

def IsraCardParser(filename):
    trans_list = []
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.parse(filename, parser)
    table = tree.xpath("//table")[3].getchildren()[1]

    for row in table.getchildren():
        tds = row.xpath(".//td")
        if tds[0].text is None:
            break

        desc = tds[1].text
        full_amount = float(tds[2].getchildren()[1].text)
        amount = float(tds[3].getchildren()[1].text)
        if amount != full_amount:
            desc = ', '.join([desc, tds[2].text, tds[5].text])

        tmp_trans = {
            'date': datetime.datetime.strptime(tds[0].text, '%d/%m/%Y').strftime('%Y-%m-%d'),
            'desc': desc,
            'reference': tds[4].text,
            'amount': -1*amount,
        }

        t = ParsedTransaction(**tmp_trans)
        trans_list.append(t)

    return trans_list
