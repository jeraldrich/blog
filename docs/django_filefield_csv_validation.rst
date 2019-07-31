Django FileField CSV Validation
=======

Let's say that you have a User that want's to attach a CSV file. You would like to validate that CSV file before saving it to your filesystem and associating to the user.

Django model validators make this easy
https://docs.djangoproject.com/en/dev/ref/validators/

A validator is a callback function for a model field that will either return True or return a ValidationError exception message which will then be displayed as an error for that field in Django admin.

For this simple example, I have a csv file that needs to be checked for valid filetype, empty cell values on required columns, and missing headers.

The HEADERS map is designed to be referenced by a separate import process not included in this example, but may give you an idea on how to implement additional sanitization checking and database actions.

If you do decide to have additional file data sanitization checks, I would recommend refactoring the import_document_validator into separate smaller validator functions and append them to the validators list. Otherwise, you are probably going to end up with a 200+ line validator function.

Here's an example::

        import csv

        from django.conf import settings
        from django.db import models
        from django.core.exceptions import ValidationError
        from django.utils.translation import ugettext_lazy as _


        # used to map csv headers to location fields
        HEADERS = {
            'shop_id': {'field':'id', 'required':True},
            'platinum_member': {'field':'platinum_member', 'required':False},
        }

        def import_document_validator(document):
            # check file valid csv format
            try:
                dialect = csv.Sniffer().sniff(document.read(1024))
                document.seek(0, 0)
            except csv.Error:
                raise ValidationError(u'Not a valid CSV file')
            reader = csv.reader(document.read().splitlines(), dialect)
            csv_headers = []
            required_headers = [header_name for header_name, values in
                                HEADERS.items() if values['required']]
            for y_index, row in enumerate(reader):
                # check that all headers are present
                if y_index == 0:
                    # store header_names to sanity check required cells later
                    csv_headers = [header_name.lower() for header_name in row if header_name]
                    missing_headers = set(required_headers) - set([r.lower() for r in row])
                    if missing_headers:
                        missing_headers_str = ', '.join(missing_headers)
                        raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
                    continue
                # ignore blank rows
                if not ''.join(str(x) for x in row):
                    continue
                # sanity check required cell values
                for x_index, cell_value in enumerate(row):
                    # if indexerror, probably an empty cell past the headers col count
                    try:
                        csv_headers[x_index]
                    except IndexError:
                        continue
                    if csv_headers[x_index] in required_headers:
                        if not cell_value:
                            raise ValidationError(u'Missing required value %s for row %s' % 
                                                    (csv_headers[x_index], y_index + 1))
            return True

        class Import(models.Model):
            imported = models.BooleanField(default=False)
            name = models.CharField(primary_key=True, max_length=255)
            document = models.FileField(upload_to='imports', validators=[import_document_validator])
            import_date = models.DateField(auto_now=True)
            
            def __unicode__(self):
                return self.name
