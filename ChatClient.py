#!/usr/bin/python
import logging, hashlib;
from twisted.internet import protocol, reactor;
from chatData_pb2 import MSG, CMD;
system_name = 'ChatClient';
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

SERVER = 'localhost';
PORT = 6666;

class ChatClientProtocol(protocol.Protocol):
	def connectionMade(self):
		log.info('Connecting to server...');
		command = int(raw_input('''Select command:
		0 - Login,
		1 - Create new lobby,
		2 - Close owned lobby,
		3 - Enter existing lobby,
		4 - Quit existing lobby,
		5 - Register new user
		>'''));
		cmd = CMD();
		if command == 0:
			login, pswd = raw_input('Enter login and password:').split(' ');
			log.debug('entering with %s and %s...', login, pswd);
			cmd.cmd = CMD.LOGIN;
			cmd.data.login = login;
			cmd.data.login = login;
			cmd.data.pswd  = hashlib.md5(pswd).hexdigest();
		elif command == 1:
			return;
		log.debug('Ready 2 send: %r', cmd.SerializeToString());
		self.transport.write(cmd.SerializeToString());
	def dataReceived(self, data):
		log.info('Received: ' + data);

class ChatClientFactory(protocol.ClientFactory):
	protocol = ChatClientProtocol;
	clientConnectionLost = clientConnectionLost = lambda self, connector, reason: reactor.stop();
	
if __name__ == '__main__':
	reactor.connectTCP(SERVER, PORT, ChatClientFactory());
	reactor.run();
