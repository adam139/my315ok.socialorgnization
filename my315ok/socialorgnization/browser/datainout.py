# -*- coding: UTF-8 -*-
from my315ok.socialorgnization import _
from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.events import CreateOrgEvent
from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from zope import event
from zope.interface import implements

import csv


data_PROPERTIES = [
    'title',
    'description',
    'address',
    'legal_person',
    'supervisor',
    'register_code',
    'belondto_area',
    'organization_type',
    'announcement_type',
    'passDate'
]
# need byte string
data_VALUES = [
    u"社会组织名称".encode('utf-8'),
    u"经营范围".encode('utf-8'),
    u"注册地址".encode('utf-8'),
    u"法定代表热".encode('utf-8'),
    u"上级主管部门".encode('utf-8'),
    u"登记证号".encode('utf-8'),
    u"所属区县".encode('utf-8'),
    u"社会组织类型".encode('utf-8'),
    u"公告类别".encode('utf-8'),
    u"批准日期".encode('utf-8')
]


class DataInOut (BrowserView):
    """Data import and export as CSV files.
    """

    def __call__(self):
        method = self.request.get('REQUEST_METHOD', 'GET')
        if (method != 'POST') or not int(
                self.request.form.get('form.submitted', 0)):
            return self.index()

        if self.request.form.get('form.button.Cancel'):
            return self.request.response.redirect('%s/plone_control_panel'
                                                  % self.context.absolute_url())

        if self.request.form.get('form.button.Import'):
            return self.importData()

        if self.request.form.get('form.button.CSVErrors'):
            return self.getCSVWithErrors()

        if self.request.form.get('form.button.Export'):
            return self.exportData()

        if self.request.form.get('form.button.ExportXiangtanshi'):
            return self.exportData(orgnization_belondtoArea="xiangtanshi")

        if self.request.form.get('form.button.ExportXiangtanshiShetuan'):
            return self.exportData(
                orgnization_belondtoArea="xiangtanshi", orgnization_orgnizationType="shetuan")

        if self.request.form.get('form.button.ExportXiangtanshiMinfei'):
            return self.exportData(
                orgnization_belondtoArea="xiangtanshi", orgnization_orgnizationType="minfei")

        if self.request.form.get('form.button.ExportXiangtanshiJijinhui'):
            return self.exportData(
                orgnization_belondtoArea="xiangtanshi", orgnization_orgnizationType="jijinhui")

    def getCSVTemplate(self):
        """Return a CSV template to use when importing members."""
        datafile = self._createCSV([])
        return self._createRequest(
            datafile.getvalue(), "orgs_sheet_template.csv")

    def IdIsExist(self, Id):
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(object_provides=IOrgnization.__identifier__, id=Id)
        return bool(brains)

    def importData(self):
        """Import Data from CSV file.

        In case of error, return a CSV file filled with the lines where
        errors occured.
        """
        file_upload = self.request.form.get('csv_upload', None)
        if file_upload is None or not file_upload.filename:
            return
        reader = csv.reader(file_upload)
        header = reader.next()
        if header != data_VALUES:
            msg = _(
                'Wrong specification of the CSV file. Please correct it and retry.')
            type = 'error'
            IStatusMessage(self.request).addStatusMessage(msg, type=type)
            return

        validLines = []
        invalidLines = []
        for line in reader:
            #            datas = dict(zip(header, line))
            validLines.append(line)
        usersNumber = 0

        for line in validLines:
            #            datas = dict(zip(header, line))
            datas = dict(zip(data_PROPERTIES, line))

            try:
                #                groups = [g.strip() for g in datas.pop('groups').split(',') if g]
                name = datas['title']
                if not isinstance(name, unicode):
                    filename = unicode(name, 'utf-8')
                id = IUserPreferredFileNameNormalizer(
                    self.request).normalize(filename)
#                id = datas['id']
                if self.IdIsExist(id):
                    continue
                title = filename
                description = datas.pop('description')
                address = datas.pop('address')
                legal_person = datas['legal_person']
                supervisor = datas.pop('supervisor')
                register_code = datas.pop('register_code')
                belondto_area = datas.pop('belondto_area')
                organization_type = datas['organization_type']
                announcement_type = datas.pop('announcement_type')
                passDate = datas.pop('passDate')

# send a add organization event
                try:
                    event.notify(CreateOrgEvent(
                        id, title, description,
                        address, legal_person, supervisor, register_code,
                        belondto_area, organization_type, announcement_type, passDate))

                except (AttributeError, ValueError), err:
                    logging.exception(err)
                    IStatusMessage(
                        self.request).addStatusMessage(
                        err, type="error")
                    return
                usersNumber += 1
            except BaseException:
                invalidLines.append(line)
                print "Invalid line: %s" % line

        if invalidLines:
            datafile = self._createCSV(invalidLines)
            self.request['csverrors'] = True
            self.request.form['orgs_sheet_errors'] = datafile.getvalue()
            msg = _('Some errors occured. Please check your CSV syntax and retry.')
            type = 'error'
        else:
            msg, type = _('Data successfully imported.'), 'info'

        IStatusMessage(self.request).addStatusMessage(msg, type=type)
        self.request['users_results'] = usersNumber
        self.request['groups_results'] = 0
        return self.index()

    def getCSVWithErrors(self):
        """Return a CSV file that contains lines witch failed."""

        users_sheet_errors = self.request.form.get('orgs_sheet_errors', None)
        if users_sheet_errors is None:
            return  # XXX
        return self._createRequest(users_sheet_errors, "orgs_sheet_errors.csv")

    def exportData(self, **kw):
        """Export Data within CSV file."""

        datafile = self._createCSV(self._getDataInfos(**kw))
        return self._createRequest(
            datafile.getvalue(), "orgs_sheet_export.csv")

    def tranVoc(self, value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(
            self.context, 'translation_service')
        title = translation_service.translate(
            value,
            domain='my315ok.socialorgnization',
            mapping={},
            target_language='zh_CN',
            context=self.context,
            default=u"未填写")
        return title

    def _getDataInfos(self, **kw):
        """Generator filled with the orgs data."""

        catalog = getToolByName(self.context, "portal_catalog")
        query = kw
        query.update({"object_provides": IOrgnization.__identifier__})

        brains = catalog(query)

        for i in brains:
            dataobj = i.getObject()
            props = []
            if dataobj is not None:
                for p in data_PROPERTIES:  # data properties
                    #                    import pdb
                    #                    pdb.set_trace()
                    if p == "organization_type" or p == "announcement_type" or p == "belondto_area":
                        props.append(self.tranVoc(getattr(dataobj, p)))
                    else:
                        props.append(getattr(dataobj, p))
            yield props

    def _createCSV(self, lines):
        """Write header and lines within the CSV file."""
        datafile = StringIO()
        writor = csv.writer(datafile)
        writor.writerow(data_VALUES)
        map(writor.writerow, lines)
        return datafile

    def _createRequest(self, data, filename):
        """Create the request to be returned.

        Add the right header and the CSV file.
        """
        self.request.response.addHeader(
            'Content-Disposition',
            "attachment; filename=%s" %
            filename)
        self.request.response.addHeader(
            'Content-Type', "text/csv;charset=utf-8")
        self.request.response.addHeader("Content-Transfer-Encoding", "8bit")
        self.request.response.addHeader('Content-Length', "%d" % len(data))
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader(
            'Cache-Control',
            "must-revalidate, post-check=0, pre-check=0, public")
        self.request.response.addHeader('Expires', "0")
        return data
