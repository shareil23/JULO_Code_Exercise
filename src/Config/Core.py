from .Config import caches


def getCache(id):
    return caches.get(str(id))


def setCache(id, data):
    return caches.set(str(id), data)


def updateCache(id, new_data):
    caches.delete(str(id))
    return caches.set(str(id), new_data)


def deleteCache(id):
    return caches.delete(str(id))