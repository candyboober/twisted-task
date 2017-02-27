from twisted.web import resource, server
from twisted.internet import threads

import os
import re

from . import settings
from .data_store import store


class MainCallbacks(object):

    def render_template(self):
        with open(os.path.join(settings.TEMPLATES_DIR, 'main.html')) as form:
            return form.read()

    def resolve_data(self, ip):
        store.add_object(ip)
        return

    def successback(self, result, request):
        request.write(result)
        request.finish()

    def errback(self, result):
        return result


class MainResource(resource.Resource):

    callbacks = MainCallbacks()

    def render_GET(self, request):
        d = threads.deferToThread(self.callbacks.render_template)
        d.addCallback(self.callbacks.successback, request)
        d.addErrback(self.callbacks.errback)
        return server.NOT_DONE_YET

    def render_POST(self, request):
        ip = request.args['form-ip'][0]
        if not self.valid_ip(ip):
            return 'Data is not a valid'

        d = threads.deferToThread(self.callbacks.resolve_data, ip)
        d.addErrback(self.callbacks.errback)
        return 'Data has been recieved for processing'

    def valid_ip(self, ip):
        return re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
