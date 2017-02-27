from twisted.web import resource, server
from twisted.internet import threads

from jinja2 import Template

import os

from . import settings
from .data_store import store


class ShowCallbacks(object):
    def render_template(self):
        with open(os.path.join(settings.TEMPLATES_DIR, 'show.html')) as f:
            template = Template(f.read())
            return str(template.render(data=store.data))

    def clear_store(self):
        store.clear()
        return 'Data has been deleted'

    def successback(self, result, request):
        request.write(result)
        request.finish()

    def errback(self, result):
        return result


class ShowDataResource(resource.Resource):

    isLeaf = True

    callbacks = ShowCallbacks()

    def render_GET(self, request):
        d = threads.deferToThread(self.callbacks.render_template)
        d.addCallback(self.callbacks.successback, request)
        d.addErrback(self.callbacks.errback)
        return server.NOT_DONE_YET

    def render_DELETE(self, request):
        d = threads.deferToThread(self.callbacks.clear_store)
        d.addCallback(self.callbacks.successback, request)
        d.addErrback(self.callbacks.errback)
        return server.NOT_DONE_YET
