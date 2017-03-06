ERROR_MSG = {}


class BusinessError(Exception):
    error_code = 0
    error_msg = None
    error_key = None

    def __init__(self, error_code, error_msg=None, error_key=None):
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_key = error_key
        super(BusinessError, self).__init__(self.get_error_msg())

    def get_error_msg(self):
        if self.error_msg is not None:
            return self.error_msg
        return ERROR_MSG.get(self.error_code, self.error_code)

    @staticmethod
    def get_invalid_parameter_exception(parameter_name='', reason_desc=''):
        return BusinessError('30001', "\"%s\" is invalid, %s" % (parameter_name, reason_desc),
                             error_key=parameter_name)
    @staticmethod
    def get_obj_already_exist(object_name='', reason_desc=''):
        return BusinessError('30001', "\"%s\" has already existed, %s" % (object_name, reason_desc),
                             error_key=object_name)
