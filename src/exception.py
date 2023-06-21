import sys, os

def get_error_message(error, sys_obj):
    exc_type, exc_obj, exc_tb = sys_obj.exc_info()
    # file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[-1]
    file_path = exc_tb.tb_frame.f_code.co_filename
    line_no   = exc_tb.tb_lineno
    message = "\n Error occured in script: {0}, \n Line no: {1} \n Error message: {2}".format(file_path, line_no, error)
    return  message

class CustomException(Exception):
    # constructor
    def __init__(self, error, sys_obj):
        self.error = error
        self.error_message = get_error_message(self.error, sys_obj)

    # __str__ to print the value
    def __str__(self):
        return self.error_message

# if __name__ == "__main__":
#     try:
#         a = 2/0
#     except Exception as e:
#         raise CustomException(e, sys)

# try:
#
#     raise(CustomException(3*3, sys))
# except CustomException as err:
#     # exc_type, exc_obj, exc_tb = sys.exc_info()
#     # file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[-1]
#     # file_path = exc_tb.tb_frame.f_code.co_filename
#     print("Exception occured: ",err.error_message)
#     # print("Exception Type: ", exc_type)
#     # print("Exception object: ",exc_obj)
#     # print("Exception file_name: ", file_name)
#     # print("Exception file_path: ", file_path)
#     # print("Line no: ", exc_tb.tb_lineno)