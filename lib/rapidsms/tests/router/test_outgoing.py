from django.test import TestCase

from rapidsms.router.test import BlockingRouter
from rapidsms.messages.outgoing import OutgoingMessage
from rapidsms.tests.harness.base import MockBackendRouter


class OutgoingTest(MockBackendRouter, TestCase):

    def setUp(self):
        self.contact = self.create_contact()
        self.backend = self.create_backend({'name': 'simple'})
        self.connection = self.create_connection({'backend': self.backend,
                                                  'contact': self.contact})
        self.router = BlockingRouter()

    def test_outgoing(self):
        """
        Router.outgoing should call backend.send() method
        and set message.sent flag respectively
        """
        msg = OutgoingMessage(self.connection, 'hello!')
        self.router.outgoing(msg)
        self.assertTrue(msg.sent)
        self.assertEqual(msg, self.outbox[0])

    def test_handle_outgoing_with_connection(self):
        """
        Router.handle_outgoing with a connection
        """
        self.router.handle_outgoing('hello!', connection=self.connection)
        self.assertEqual('hello!', self.outbox[0].text)
        self.assertEqual(self.connection, self.outbox[0].connection)