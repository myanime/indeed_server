from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter


class CSVkwItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')
        kwargs['include_headers_line'] = False
        super(CSVkwItemExporter, self).__init__(*args, **kwargs)
