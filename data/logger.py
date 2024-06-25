import datetime
from string import Template
from typing import Literal
from rich.console import Console

console = Console()
pprint = console.print

COLORED_LEVELS = {
    "info": "[[purple]LOG[/purple]",
    "debug": "[[blue]DEBUG[/blue]",
    "warn": "[[yellow]WARNING[/yellow]",
    "error": "[[red]ERROR[/red]",
    "start": "[[magenta]STARTED[/magenta]",
    "close": "[[red]CLOSED[/red]"
}

class Logger:
    def __init__(
        self, process_name: str, log_format: Template, time_format: str, log_file: str
    ) -> None:
        self.console = Console()
        self.name = process_name
        self.format = log_format
        self.time_format = time_format
        self.log_file = log_file

        self.debug("Logger Started!")

    def get_time(self):
        return datetime.datetime.now().strftime(self.time_format)

    def write_to_file(self, log_message: str):
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')

    def log(self, level:Literal["info", "debug", "warning", "error", "start", "close"]="info", text:str=None):
        formatted_text = self.format.substitute(
            time=self.get_time(),
            process=self.name,
            level=COLORED_LEVELS[level],
            message=f"[white]{text}[/white]",
        )
        pprint(f"[gray]{formatted_text}[/gray]")
        self.write_to_file(formatted_text)

    def info(self, message:str=None, exception:str=None, extra:str=None) -> None:
        self.log("info", message)
        if exception:
            self.log("info", exception)
        if extra:
            self.log("info", extra)

    def debug(self, message) -> None:
        self.log("debug", message)

    def warn(self, message) -> None:
        self.log("warn", message)

    def error(self, message) -> None:
        self.log("error", message)

    def start(self, message) -> None:
        self.log("start", message)
    
    def close(self, message) -> None:
        self.log("close", message)


def space(list_max_lenght, word, add_space:int = 0):
    spaces = (list_max_lenght-len(str(word))+add_space)
    return " "*spaces

def set_logger(
    process_name: str = __name__,
    proccess_tabs: int = 10,
    log_format: Template|str = None,
    time_format: str = "%d.%m.%Y %H:%M:%S",
    log_path:str = "logs.log",
) -> Logger:
    if not log_format:
        log_format = Template(f"[$time {space(list_max_lenght=proccess_tabs, word=process_name)}$process] $level] $message")
    return Logger(process_name, log_format, time_format, log_path)
