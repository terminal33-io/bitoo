class ChatMessage:
    HELLO = "Hello, how can I help you?"
    UNABLE_TO_ANSWER = "I cannot answer, reach out to the GC support staff."
    UNAUTHORIZED = "You are not authorized to access other location data. Kindly contact the GC Support."
    ERROR = "Some error occurred. Please try again!"
    NO_REPORT_ERROR = "No such report exists as per my knowledge!"
    SQL_RESULT_ERROR = "Cannot answer since query execution failed and didn't provide any results."

    @classmethod
    def is_constant(cls, message: str):
        for attr_name in dir(cls):
            # Skip special methods and attributes
            if not attr_name.startswith("__"):
                attr_value = getattr(cls, attr_name)
                if message == attr_value:
                    return True
        return False
