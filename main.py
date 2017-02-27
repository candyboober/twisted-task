from twisted.web import server, resource
from twisted.internet import reactor

from app.main import MainResource
from app.show import ShowDataResource


class Root(MainResource):
    route = {
        'show': ShowDataResource
    }

    def getChild(self, name, request):
        if not name:
            return self
        if name in self.route:
            return self.route[name]()
        else:
            return resource.NoResource()


main_page = Root()
factory = server.Site(main_page)
reactor.listenTCP(8000, factory)
reactor.run()
