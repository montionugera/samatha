from samatha.exceptions import BusinessError

MIN_LENGTH = 3
MAX_LENGTH = 64

class InputValidator(object):
    def validate_require_parameter(self, **kwarg):
        for k, v in kwarg.iteritems():
            if v is None:
                raise BusinessError.get_invalid_parameter_exception(
                    parameter_name=k, reason_desc="Value is None")
            if type('') is str and v < MIN_LENGTH:
                raise BusinessError.get_invalid_parameter_exception(
                    parameter_name=k,
                    reason_desc="Value is too short "
                                "(MIN Length is %s)" % MIN_LENGTH)

    def validate_not_too_long_parameter(self, **kwarg):
        max_len = kwarg.get('max_len', MAX_LENGTH)
        for k, v in kwarg.iteritems():
            if k == 'max_len':
                continue
            if len(v) > max_len:
                raise BusinessError.get_invalid_parameter_exception(
                    parameter_name=k,
                    reason_desc="Value is too long "
                                "(MAX Length is %s)" % max_len)

    def validate_shuoud_be_float_parameter(self, **kwarg):
        for k, v in kwarg.iteritems():
            if type(v) is not float:
                raise BusinessError.get_invalid_parameter_exception(
                    parameter_name=k,
                    reason_desc="Value must be float "
                                "(%s)" % v)

    def validate_shuoud_be_int_parameter(self, **kwarg):
        options = ['allow_null']
        allow_null = kwarg.get('allow_null', False)
        for k, v in kwarg.iteritems():
            if allow_null and v is None:
                continue
            if k not in options and type(v) is not int:
                raise BusinessError.get_invalid_parameter_exception(
                    parameter_name=k,
                    reason_desc="Value must be int "
                                "(%s)" % v)
