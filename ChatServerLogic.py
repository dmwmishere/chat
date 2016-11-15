import logging, sqlite3, hashlib, time
from chatData_pb2 import CMD, MSG

db = sqlite3.connect(database='chats', isolation_level=None)
c = db.cursor()

log = logging.getLogger('Logic')


def login(login, pswd):
    if c.execute('select count(*) from users where login = ? and pswd = ?', (login, hashlib.md5(pswd).hexdigest())).fetchone()[0] > 0:
        c.execute('update users set state = ?, last_login = ? where login = ?', (1, time.ctime(), login))
        return True
    else:
        return False


def register_new(login, pswd, name):
    if c.execute("select count(*) from users where login = ?", (login,)).fetchone()[0] < 1:
        log.info("Registering new user:\nlogin = %s,\nname = %s", login, name)
        c.execute("insert into users (login, pswd, name, state) values (?, ?, ?, 0)",
                  (login, hashlib.md5(pswd).hexdigest(), name))
        db.commit()
        return True
    else:
        return False
