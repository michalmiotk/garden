import logging as log

format = "%(asctime)s %(levelname)s:%(message)s"
log.basicConfig(format=format, filename="logs.log", level="INFO")
log.getLogger().addHandler(log.StreamHandler())