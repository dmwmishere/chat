#!/usr/bin/python
import logging, hashlib;
from twisted.internet import protocol, reactor;
from time import ctime;
from chatData_pb2 import CMD, MSG;
system_name = 'ChatServer';
logging_level = logging.DEBUG;
log = logging.getLogger(system_name);
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s');
fh = logging.FileHandler(system_name + '.log');
fh.setFormatter(formatter);
ch = logging.StreamHandler();
ch.setFormatter(formatter);
log.addHandler(fh);
log.addHandler(ch);
log.setLevel(logging_level);

PORT = 6666;
class ChatServerProtocol(protocol.Protocol):
	def connectionMade(self):
		clnt = self.clnt = self.transport.getPeer().host;
		log.info('%s connected', clnt);
	
	def dataReceived(self, data):
		log.debug('Received: ' + data);
		cmd = CMD();
		cmd.ParseFromString(data);
		log.info('Command %d', cmd.cmd);
		self.transport.write('done');

if __name__ == '__main__':
	factory = protocol.Factory();
	factory.protocol = ChatServerProtocol;
	log.info('Waiting for client...');
	reactor.listenTCP(PORT, factory);
	reactor.run();
