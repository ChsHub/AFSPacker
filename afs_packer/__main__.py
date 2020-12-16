from datetime import datetime
from io import SEEK_SET, BytesIO
from os import utime, mkdir, listdir
from os.path import splitext, exists, join
from time import mktime

__version__ = '1.0.0'
SIGN = {b'AFS\x00': 'little', b'\x00SFA': 'big'}


class Token:
    def __init__(self, size, offset):
        self.size = size
        self.offset = offset
        self.name = None


class Header:
    def __init__(self, file_stream: BytesIO):
        """
        Parse .AFX file for meta information
        :param file_stream: .AFS file stream
        """
        self.file_count = None
        self.tokens = []

        # Check for little or big endian
        self.sign = file_stream.read(4)
        if self.sign in SIGN:
            print('Signature: OK')
            self.sign = SIGN[self.sign]
        else:
            raise ValueError('Signature: NOT OK')

        # Get number of files
        self.file_count = self._to_int(file_stream.read(4))
        print('Files:', self.file_count)

        self._read_tokens(file_stream)
        self._read_attributes(file_stream)

    def _to_int(self, bytes_in: bytes) -> int:
        """
        Convert bytes to integer depending on the file's endianness
        :param bytes_in: Input bytes
        :return: Integer
        """
        return int.from_bytes(bytes_in, byteorder=self.sign)

    def _read_tokens(self, file_stream: BytesIO) -> None:
        """
        Read the file's positions and size
        :param file_stream: .AFS file stream
        """
        for i in range(self.file_count):
            offset = file_stream.read(4)
            size = file_stream.read(4)
            self._add_new_token(offset, size)

    def _seek_attribute_table(self, file_stream: BytesIO) -> int:
        """
        Locate the file attribute table
        :param file_stream: .AFS file stream
        :return: End position of the attribute table
        """
        attribute_table_offset = 0
        attribute_table_size = 0
        if file_stream.tell() != len(self.tokens) * 8 + 8:
            raise ValueError('Wrong file position')

        while attribute_table_offset == 0:
            attribute_table_offset = self._to_int(file_stream.read(4))
            attribute_table_size = self._to_int(file_stream.read(4))
            if file_stream.tell() >= self.tokens[0].offset:
                raise ValueError('No file attributes found')

        print('SKIP', attribute_table_offset - file_stream.tell(), 'BYTES')  # TODO investigate skipped bytes
        file_stream.seek(attribute_table_offset, SEEK_SET)  # Set offset in relation to file start

        return attribute_table_offset + attribute_table_size

    def _read_attributes(self, file_stream: BytesIO) -> None:
        """
        Find and parse the file attribute table
        :param file_stream: .AFS stream
        """
        attribute_table_end = self._seek_attribute_table(file_stream)
        for i, token in enumerate(self.tokens):
            token.name = file_stream.read(32)
            token.name = token.name.strip(b'\x00').decode('UTF-8')  # Remove zeroes, get string
            print('File name:', token.name)
            date = []
            for i in range(6):
                date.append(self._to_int(file_stream.read(2)))
            token.date = date
            token.file_size = self._to_int(file_stream.read(4))

        if file_stream.tell() != attribute_table_end:
            raise ValueError('Attribute table not read completely')

    def _add_new_token(self, offset, size):
        new_size = self._to_int(size)
        new_token = Token(new_size, self._to_int(offset))
        self.tokens.append(new_token)


def _create_directory(file_path: str) -> str:
    """
    Create target directory for the extracted files
    :param file_path: Parent path
    :return: Path of new directory
    """
    file_path, _ = splitext(file_path)
    if exists(file_path):
        raise FileExistsError('ERROR: Folder already exists')
    mkdir(file_path)
    return file_path


def _write_date(token, file_path):
    """
    If date information was found add to extracted file
    :param token: File token
    :param file_path: Path
    """
    try:
        year, month, day, hour, minute, second = token.date
        date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        modTime = mktime(date.timetuple())
        utime(file_path, (modTime, modTime))
    except ValueError as e:
        print(e)


def _write_files(dir_path, header, file_stream, decode_bip=False):
    """
    Write files to disk
    :param dir_path: target directory
    :param header: Meta data header
    :param file_stream: .AFS file stream
    :param decode_bip: Try to decode file
    """
    no_name_count = 0
    for token in header.tokens:
        if not token.name:
            token.name = 'NO_NAME_%s' % no_name_count
            no_name_count += 1
            print('No file name found. Set name %s' % token.name)

        file_name = join(dir_path, token.name)
        with open(file_name, mode='wb') as f:
            file_stream.seek(token.offset, SEEK_SET)
            file_content = file_stream.read(token.size)
            f.write(file_content)
            del file_content

        _write_date(token, file_name)


def extract(file_path: str):
    """
    Extract files contained in .AFS file
    :param file_path: .AFS
    """
    with open(file_path, mode='rb') as file_stream:
        # noinspection PyTypeChecker
        header = Header(file_stream=file_stream)
        file_path = _create_directory(file_path)
        _write_files(file_path, header, file_stream)


def extract_batch(dir_path: str):
    """
    Extract files from all .AFS files contained in directory path
    :param dir_path: Path
    """
    for file in listdir(dir_path):
        if file.endswith('.AFS'):
            extract(join(file_path, file))


def create(path: str):
    """
    Create new .AFS
    :param path: File name
    """
    pass  # TODO


if __name__ == '__main__':
    file_path = input('FILE PATH:')
    file = input('FILE:')
    extract(join(file_path, file))
