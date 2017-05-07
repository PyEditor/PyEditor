DEFAULT_MCPI_SCRIPT= """\
from mcpi import minecraft

mc = minecraft.Minecraft.create()
mc.postToChat("Hello world, from PyEditor!")
"""
DEFAULT_SCRIPT="""\
import time

for no in range(3):
    print("{no} Hello World! (äöüß)".format(no=no))
    time.sleep(1)
"""
