"""Local Filesystem utilities for common tasks.
"""

import io
import zipfile
from pathlib import Path
from typing import BinaryIO


def csvopen(path) -> list:
    """Open CSV file and return list.

    It's called csvopen but it's essentially for new line delimited files, with one entry per line.
    Reads those files into a list to be used in iterative operations.

    Args:
        path (Path or str): Local file path, either as pathlib Path object or string.

    Returns:
        list: List of strings found in the source file.
    """
    with open(path) as file:
        return [line.strip() for line in file.read().splitlines()]


class Zipper:
    """Zipfile helper class.

    Provides methods to help build zipfiles for Salesforce Site Imports.
    """

    def __init__(self):
        self.zip_file = io.BytesIO()

    @property
    def stream(self) -> bytes:
        """Return stream of Zip object.

        [extended_summary]

        Returns:
            bytes: Zipfile.
        """
        return self.zip_file.getvalue()

    def add(self, payload, relative_path: str) -> BinaryIO:
        """Add data to zip.

        Args:
            payload : String, bytes, io.BytesIO or io.StringIO.
            relative_path (str): Path inside the zipfile including filename.

        Returns:
            BinaryIO: Zipfile IO stream.
        """
        with zipfile.ZipFile(self.zip_file, "a") as zf:
            try:
                zf.writestr(relative_path, payload.getvalue(), zipfile.ZIP_DEFLATED)
            except AttributeError:
                try:
                    zf.writestr(relative_path, payload.read(), zipfile.ZIP_DEFLATED)
                except AttributeError:
                    zf.writestr(relative_path, payload, zipfile.ZIP_DEFLATED)

    def write(self, zip_name: str, local_path: str = ""):
        """Write zip data to file.

        Takes the io.BytesIO stream and writes it to disk given zip_name and local_path.

        Args:
            zip_name (str): Name of file; eg example.zip
            local_path (str, optional): Local path, gets parsed by pathlib. Defaults to "" (CWD).
        """
        writepath = Path.joinpath(Path(local_path), Path(zip_name))
        with open(writepath, "wb") as writeout:
            writeout.write(self.zip_file.getvalue())

    def read(self):
        """Expose zipfile to be used by other functions without writing to disk.

        Returns:
            bytes: Zip file bytestream.
        """
        return self.zip_file.getvalue()

    def filelist(self):
        """Show filelist including relative paths in zip.

        Returns:
            list: List of filepaths relative to archive root.
        """
        return zipfile.ZipFile(self.zip_file).namelist()
