from datetime import datetime
import pandas as pd
import configparser

CONFIG_PATH = "application/error_conf.ini"


def process_request(json_request):
    handler = RequestHandler(json_request)
    return handler.create_response()


def _generate_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def create_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")


class RequestHandler:
    LOG_PATH = "log.txt"

    def __init__(self, request):
        self.config = _generate_config(CONFIG_PATH)
        try:
            self.number, self.color, self.is_first = self._parse_request(
                request)
        except Exception as e:
            print(e)
            self.number, self.color, self.is_first = None, None, None

    def log_request(self, path, *args):
        with open(path, 'a') as f:
            for arg in args:
                f.write(str(arg))

    def _parse_request(self, request):
        num = request["number"]
        color = request["color"]
        is_first = request["is_first"]

        return num, color, is_first

    def create_response(self):
        if self.number:
            if self.is_first:
                return {"request_ok": True, "possible_solution": self._generate_possible_solution()}
            else:
                return {"request_ok": True, "possible_solution": None}
        else:
            return {"request_ok": False, "possible_solution": None}

    def _generate_possible_solution(self):
        return self.config["possible_solutions"][self.number]

    def create_DAV_connection(self):
        # creates connection to PRISMA DAV serverself.
        pass


class Record:
    def __init__(self, request_body, is_done):
        self.config = _generate_config(CONFIG_PATH)
        self.details = self._from_request(request_body, is_done)

    def _from_request(self, request_body, is_done):
        error_code = request_body["error"].split(" ")[1]

        description = self.config["descriptions"][error_code]
        prefix = self.config["prefixes"][error_code]
        code_type = self.config["codetypes"][error_code]
        location = self.config["locations"][error_code]
        fault_code = self.config["faultcodes"][error_code]

        date = create_timestamp().split(" ")[0] + " 00:00:00"
        time = create_timestamp().split(" ")[1]

        if is_done:
            message_type = "Info"
            status = "solved"
        else:
            message_type = "Error"
            status = "new"

        # return joined tuple so dataframe has no headers as PRISMA excel has no headers
        return zip([prefix], [code_type], [location], [fault_code],
                   [message_type], [description], [date], [time], [status])

    def to_dataframe(self):
        return pd.DataFrame(self.details)
