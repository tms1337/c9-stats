import time, threading



class c9Editor:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        
        self._check_url()
        self._check_username()
        self._check_password()

        self._set_up_connection()

    def write_text(self, text):
        pass

    def backspance(self, backspace_n):
        pass

    def _check_url(self):
        pass
    
    def _check_username(self):
        pass

    def _check_password(self):
        pass

    def _set_up_connection(self):
        pass

class StatisticsGenerator:

    def __init__(self,polling_period=600):
        self.polling_period = polling_period

    def start_polling(self):
        if self.thread is None:
            self.thread = threading.Timer(self.polling_period, self._poll_once)
            self.thread.start()
        else:
            raise UserWarning("Trying to start polling that already started")
    
    def _poll_once(self):
        pass
        # should write to file every n times!

    def stop_polling(self):
        if not self.thread is None:
            self.thread.stop()
        else:
            raise UserWarning("Trying to stop polling that is not yet started")
            