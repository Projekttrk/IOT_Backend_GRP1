from datetime import datetime
import pandas as pd
import configparser
import logging

CONFIG_PATH = "application/error_conf.ini"

logging.basicConfig(level=logging.DEBUG, filename="log.txt")


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
    def __init__(self, request):
        self.config = _generate_config(CONFIG_PATH)
        try:
            self.number, self.color, self.is_first = self._parse_request(
                request)
        except Exception as e:
            print(e)
            self.number, self.color, self.is_first = None, None, None

    def log_request(self, status):
        timestamp = create_timestamp()
        error_desc = self._get_error_description()
        logging.info("{}: number: {} color: {} problem: {} status: {}".format(
            timestamp, self.number, self.color, error_desc, status))

    def _parse_request(self, request):
        num = request["number"]
        color = request["color"]
        is_first = request["is_first"]

        return num, color, is_first

    def create_response(self):
        if self.number:
            if self.is_first:
                self.log_request("new")
                return {"request_ok": True, "possible_solution": self._generate_possible_solution(), "error_description": self._get_error_description()}
            else:
                self.log_request("moved to prisma")
                return {"request_ok": True, "possible_solution": None, "error_description": None}
        elif not self.number and not self.is_first:
            self.log_request("solved")
            return {"request_ok": True, "possible_solution": None, "error_description": None}
        else:
            self.log_request("internal error")
            return {"request_ok": False, "possible_solution": None, "error_description": None}

    def _generate_possible_solution(self):
        return self.config["possible_solutions"][self.number]

    def _get_error_description(self):
        if not self.number:
            self.number = "01"
        return self.config["descriptions"][self.number]

    def create_DAV_connection(self):
        # creates connection to PRISMA DAV serverself.
        # STAR never gave login details :)
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
