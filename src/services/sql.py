import sqlite3
from config import Config
import logging

class DataBase:
    def __init__(self, db_file):
        logging.basicConfig(level=logging.INFO, filename='log_sql.log', filemode='w')
        self.logger_ = logging.getLogger()
        self.logger_.info(f"INFO: DB inited")
        self.connect = sqlite3.connect(db_file)
        self.curs = self.connect.cursor()

    def check_if_user_in_db(self, tg_id):
        self.logger_.info(f"INFO: DB checked if user in db ({tg_id})")
        with self.connect:
            exists = self.curs.execute("SELECT active_season FROM users WHERE tg_id=?", [tg_id,]).fetchall()
            if exists == []: return 0
            else: return 1

    def add_user(self, tg_id, tg_name, tg_username):
        self.logger_.info(f"INFO: DB added user ({tg_id}, {tg_name}, {tg_username})")
        with self.connect:
            self.curs.execute("INSERT INTO users (tg_id, tg_name, tg_username) VALUES (?, ?, ?)", [tg_id, tg_name, tg_username])
            self.connect.commit()
            return 1
        
    def update_tg_id(self, tg_id, username):
        self.logger_.info(f"INFO: DB updated tg id ({tg_id}/{username})")
        with self.connect:
            self.curs.execute("UPDATE users SET tg_id=? WHERE tg_username=?", [tg_id, username])
            return 1
        
    def get_mine_username(self, tg_id):
        self.logger_.info(f"INFO: DB got minecraft nick ({tg_id})")
        with self.connect:    
            return self.curs.execute("SELECT minecraft_username FROM users WHERE tg_id=?", [tg_id, ]).fetchall()
        
    def check_season_avail(self, tg_id):
        self.logger_.info(f"INFO: DB checked if season available ({tg_id})")
        with self.connect:
            return self.curs.execute("SELECT active_season FROM users WHERE tg_id=?", [tg_id,]).fetchall()
        
    def check_priv_avail(self, tg_id):
        self.logger_.info(f"INFO: DB checked if private available ({tg_id})")
        with self.connect:
            return self.curs.execute("SELECT private_avail FROM users WHERE tg_id=?", [tg_id,]).fetchall()
        
    def check_admin(self, tg_id):
        self.logger_.info(f"INFO: DB checked if user is admin ({tg_id})")
        with self.connect:
            return self.curs.execute("SELECT admin FROM users WHERE tg_id=?", [tg_id,]).fetchall()
        
    def get_tg_id_by_username(self, username):
        self.logger_.info(f"INFO: DB got tg id by username ({username})")
        with self.connect:
            return self.curs.execute("SELECT tg_id FROM users WHERE tg_username=?", [username,]).fetchall()
        
    def update_mine_nick(self, nick, tg_id):
        self.logger_.info(f"INFO: DB updated minecraft nick ({tg_id}, {nick})")
        with self.connect:
            self.curs.execute("UPDATE users SET minecraft_username=? WHERE tg_id=?", [nick, tg_id])
            self.connect.commit()
            return 1
        
    def get_season_descr(self):
        self.logger_.info(f"INFO: DB got active season description")
        with self.connect:
            return self.curs.execute("SELECT description FROM seasons WHERE active=1").fetchall()
        
    def get_season_price(self):
        self.logger_.info(f"INFO: DB got active season price")
        with self.connect:
            return self.curs.execute("SELECT price FROM seasons WHERE active=1").fetchall()
        
    def get_now_season(self):
        self.logger_.info(f"INFO: DB got active season")
        with self.connect:
            return self.curs.execute("SELECT id FROM seasons WHERE active=1").fetchall()
        
    def update_label(self, label, tg_id):
        self.logger_.info(f"INFO: DB updated label ({tg_id})")
        with self.connect:
            self.curs.execute("UPDATE users SET label=? WHERE tg_id=?", [label, tg_id])
            return 1
        
    def update_payment_status(self, status, tg_id):
        self.logger_.info(f"INFO: DB updated payment status ({tg_id}, {status})")
        with self.connect:
            self.curs.execute("UPDATE users SET bought=? WHERE tg_id=?", [status, tg_id])
            return 1

    def get_payment_status(self, tg_id):
        self.logger_.info(f"INFO: DB got payment status ({tg_id})")
        with self.connect:
            return self.curs.execute("SELECT bought, label FROM users WHERE tg_id=?", [tg_id,]).fetchall()
        
    def update_season_avail(self, tg_id):
        self.logger_.info(f"INFO: DB updated seasnon available ({tg_id})")
        with self.connect:
            active_season = self.curs.execute("SELECT id FROM seasons WHERE active=1").fetchall()[0][0]
            self.curs.execute("UPDATE users SET active_season=? WHERE tg_id=?", [active_season, tg_id])
            return 1
        
    def get_admins(self):
        self.logger_.info(f"INFO: DB got admins")
        with self.connect:
            return self.curs.execute("SELECT tg_id FROM users WHERE admin=1").fetchall()
        
    def get_id(self, id_):
        self.logger_.info(f"INFO: DB got tg_id by id ({id_})")
        with self.connect:
            return self.curs.execute("SELECT tg_id FROM users WHERE id=?", [id_]).fetchall()[0][0]
        
    def get_ids_num(self):
        self.logger_.info(f"INFO: DB got ids")
        with self.connect:
            return self.curs.execute("SELECT id FROM users").fetchall()[0]
            
    def discord_username(self, tg_id):
        self.logger_.info(f"INFO: DB got discord nick ({tg_id})")
        with self.connect:    
            return self.curs.execute("SELECT discord_username FROM users WHERE tg_id=?", [tg_id, ]).fetchall()
        
    def update_diss_nick(self, nick, tg_id):
        self.logger_.info(f"INFO: DB updated discord nick ({tg_id}, {nick})")
        with self.connect:
            self.curs.execute("UPDATE users SET discord_username=? WHERE tg_id=?", [nick, tg_id])
            self.connect.commit()
            return 1