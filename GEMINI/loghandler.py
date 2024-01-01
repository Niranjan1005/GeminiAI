import logging
import os

# Custom logging handler to check and rotate log file based on the maximum lines
class MaxLinesRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=10000, mode='a', encoding=None, delay=0):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.line_count = self.get_line_count()

    def emit(self, record):
        if self.should_rotate():
            self.rotate_log_file()

        super().emit(record)

    def should_rotate(self):
        return self.line_count >= self.max_lines

    def rotate_log_file(self):
        self.close()
        backup_count = 1
        while os.path.exists(self.get_backup_filename(backup_count)):
            backup_count += 1

        os.rename(self.baseFilename, self.get_backup_filename(backup_count))
        self.line_count = 0
        self.stream = self._open()

    def get_line_count(self):
        try:
            with open(self.baseFilename, 'r') as f:
                return sum(1 for _ in f)
        except FileNotFoundError:
            return 0

    def get_backup_filename(self, backup_count):
        return f"{self.baseFilename}.backup{backup_count}"


# Test the logger
# logging.info("Log message 1")
# logging.info("Log message 2")
