#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging
import sys

try:
    import idlelib
except ImportError as err:
    print("\nERROR: Python IDLE not installed: %s" % err)
    print("Install it e.g.:")
    print("\t$ sudo apt install idle\n")
    sys.exit(-1)

from pyeditor.config import DESCRIPTION

log = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

from pyeditor.editor_window import EditorWindow
from pyeditor.version import __version__


def main():
    parser = argparse.ArgumentParser(prog="pyeditor", description=DESCRIPTION)
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )
    args = parser.parse_args()

    log.info("Python v%s", sys.version.replace("\n", ""))

    gui = EditorWindow()
    gui.root.mainloop()


if __name__ == "__main__":
    main()
