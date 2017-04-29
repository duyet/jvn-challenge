""" Check file """
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
import magic
import os
import pandas as pd

@deconstructible
class FileValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
     'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 
                                   'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            if content_type not in self.content_types:
                params = { 'content_type': content_type }
                raise ValidationError(self.error_messages['content_type'],
                                   'content_type', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)


def validate_score(input_file, validate_file, label_col = 'label', id_col='id'):
  result = {
    'score': 0,
    'message': '',
    'status': 'error'
  }

  if not os.path.isfile(input_file.path) or not os.path.isfile(validate_file.path):
    result['message'] = 'File error'
    return result

  try:
    validate_data = pd.read_csv(validate_file.path)
  except:
    result['message'] = 'Validate file error'
    return result

  try:
    input_data = pd.read_csv(input_file.path)
  except:
    result['message'] = 'Submit file format error'
    return result

  if not len(input_data.index):
    result['message'] = 'Submit file empty'
    return result

  if not label_col in input_data.columns:
    result['message'] = 'The submit file do not have [%s] column.' % label_col
    return result

  if not label_col in validate_data.columns:
    result['message'] = 'The validate file do not have [%s] column.' % label_col
    return result

  validate_data_len = len(validate_data.index)
  input_data_len = len(input_data.index)

  if validate_data_len != input_data_len:
    result['message'] = 'The submit file has %s rows, experted %s rows' % (input_data_len,validate_data_len)
    return result

  checking_df = validate_data.join(input_data, on=id_col, how='left', lsuffix='__validate', rsuffix='__input')
  number_of_right = len(checking_df[checking_df[label_col + '__validate'] == checking_df[label_col + '__input']].index)

  result['message'] = 'OK'
  result['status'] = 'success'
  result['score'] = (100.0 * number_of_right) / validate_data_len

  return result