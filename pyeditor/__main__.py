#!/usr/bin/env python3
# coding: utf-8

import logging
import sys

log = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

log.info("Python v%s", sys.version.replace("\n", ""))

from pyeditor.editor_window import EditorWindow


def main():
    gui = EditorWindow()
    gui.root.mainloop()


if __name__ == "__main__":
    main()
