import re

from watcher.constant import FULL_SHADOW_REGEX_PATTERN


class FeedParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def parse_feed_name(self) -> (str, str):

        shadow_file_source_match = re.search(FULL_SHADOW_REGEX_PATTERN, self.file_name)
        if shadow_file_source_match:
            return shadow_file_source_match.group(1), shadow_file_source_match.group(2)

        else:
            return "FILE_IGNORE", "FILE_IGNORE"
