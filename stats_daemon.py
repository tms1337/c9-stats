import time, threading
import signal
import requests
from requests.auth import HTTPBasicAuth
import mechanize
from requests.exceptions import ConnectionError

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class c9Connection:
    def __init__(self, 
                url, 
                username,
                password, 
                file_name="main.cpp",
                login_url="/index.php", 
                status_url="/status-service.php?serverStatus",
                timeout=10,
                server_start_timeout=30,
                status_ok_keyword="ok",
                file_updated_http_code=201):
        
        self.url = url
        self.login_url = self.url + login_url
        self.status_url = self.url + status_url
        
        self.timeout = timeout
        self.server_start_timeout = server_start_timeout

        self.status_ok_keyword = status_ok_keyword
        self.file_updated_http_code = file_updated_http_code
        
        self.username = username
        self.password = password
        self.file_name = file_name
        
        self._check_url()
        self._check_username()
        self._check_password()

        self.workspace_url = "{}/{}".format(self.url, self.username)
      
        print("Establishing connection...")
        self._try_authenticate()
        self._try_start_server()
        self._try_open_websocket()

    def try_write_text(self, text):
        vfsid = requests.post("http://c9.etf.unsa.ba/fmustafic1/vfs/1", 
                                auth=HTTPBasicAuth(self.username, 
                                                    self.password))
        print( vfsid.text )
        raw_input("stop.")

        file_token = self._get_file_token()
        file_url = "{}/vfs/1/{}/workspace/ASP/T1/Z1/{}"\
                    .format(self.workspace_url, file_token, self.file_name)
        file_auth = HTTPBasicAuth(self.username, self.password)

        try:
            file_response = requests.put(file_url, 
                                        auth=file_auth, 
                                        data=text, 
                                        timeout=self.timeout)
            if file_response.status_code != self.file_updated_http_code:
                print("\tCould not update file, response code {}"\
                        .format(file_response.status_code))
                raise ConnectionError("Could not write to file")
            else:
                print("\tContent of file {} succesfully updated to {}"\
                        .format(file_url, text))
        except requests.exceptions.ConnectionError as e:
            print("Server not reachable within {}s when writing text"\
                    .format(self.timeout))
            raise e

    def _get_file_token(self):
        return "9chXBkE92Ew8fcVs"

    def _check_url(self):
        pass
    
    def _check_username(self):
        pass

    def _check_password(self):
        pass

    def _try_authenticate(self):
        print("\tAuthenticating with {}".format(self.username))
        
        try:
            login_response = requests.post(self.login_url, 
                                data = {
                                    'login': self.username,
                                    'password': self.password},
                                timeout=self.timeout,
                                allow_redirects=False)
        except requests.exceptions.ConnectionError as e:
            print("Login timed out")
            raise e
        
        if "pristupni podaci" in login_response.text:
            raise ValueError("Invalid credentials")
        else:
            print("\tSuccessfully logged in")
            self.session_id = login_response.cookies["PHPSESSID"]
            self.cookie = {"PHPSESSID": self.session_id, 
                            "old_login": self.username}

    def _try_start_server(self):
        try:
            with timeout(self.server_start_timeout):
                while True:
                    print("Checking server status at {}"\
                            .format(self.status_url))
                    status_response = \
                        requests.get(self.status_url, cookies=self.cookie)
                    if status_response.text == self.status_ok_keyword:
                        break
        except TimeoutError as e:
            print("Establishing connection to workspace timed out")
            raise e
        except requests.exceptions.ConnectionError as e:
            print("Could not reach status url at {}".format(self.status_url))
            raise e

    def _try_open_websocket(sel):
        print("\tOpening websocket")

class StatisticsGenerator:
    def __init__(self,polling_period=600):
        self.real_time = real_time
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

if __name__ == "__main__":
    conn = c9Connection("http://c9.etf.unsa.ba", 
                        "fmustafic1", 
                        "nisamostaviopassword")

    while True:
        text = raw_input("Enter new content (quit to abort): ")
        if text == "quit":
            break
        conn.try_write_text(text)
    