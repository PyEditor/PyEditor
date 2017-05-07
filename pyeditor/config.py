import os

DESCRIPTION="Python Editor for beginners and Minecraft Fans"

DEFAULT_FILETYPES=[ # for askopenfile, asksaveasfile, etc.
    ("Python files", "*.py", "TEXT"),
    ("All files", "*"),
]
DEFAULTEXTENSION = "*.py"

BASE_DIR_NAME="PyEditor files"
RUN_BACKUP_SUBDIR="run backups"
AUTO_BACKUP_SUBDIR="auto backups"

HOME_PATH=os.path.expanduser("~")

BASE_PATH=os.path.join(HOME_PATH, BASE_DIR_NAME) # ~/PyEditor files/
RUN_BAK_PATH=os.path.join(BASE_PATH, RUN_BACKUP_SUBDIR) # ~/PyEditor files/run backups
AUTO_BAK_PATH=os.path.join(BASE_PATH, AUTO_BACKUP_SUBDIR) # ~/PyEditor files/auto backups
