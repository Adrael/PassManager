#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################################
#                                                                                    #
#                          DEVELOPED BY RAPHAEL MARQUES                              #
#                           Copyright (C) 2010 / 2011                                #
#                          See LICENCE for more details                              #
#                                                                                    #
######################################################################################

import sys, os, md5, sqlite3

######################################################################################

class Manage():

######################################################################################

    def __init__(self, pwd):
        self.home = os.getenv('USERPROFILE') or os.getenv('HOME')
        self.pman = os.path.join(self.home, "PassManager")
        self.datas = os.path.join(self.pman, ".datas")
        self.path = os.path.join(self.datas, "database.db")
        self.keyfile = os.path.join(self.datas, ".keyfile")
        if os.path.exists(self.keyfile):
            if not self.check_pwd(pwd): raise Exception, "Please verify your password, then try again ..."
            else:
                self.db = sqlite3.connect(self.path)
                try: self.create_db()
                except: pass
        else: self.update_pwd(pwd)

######################################################################################

    def create_db(self):
        try:
            c = self.db.cursor()
            c.execute('CREATE TABLE passwd (id INTEGER PRIMARY KEY, place TEXT, pseudo TEXT, mail TEXT, password TEXT)')
            self.db.commit()
        finally:
            c.close()

######################################################################################

    def list_db(self):
        c = self.db.cursor()
        res = []
        try:
            c.execute('SELECT * FROM passwd')
            self.db.commit()
            for i in c:
                res.append(i)
        finally:
            c.close()
            return res

######################################################################################

    def add_pwd(self, pl, ps, ml, pd):
        c = self.db.cursor()
        id = int(os.urandom(4).encode('hex'), 16)
        try:
            c.execute('''INSERT INTO passwd (id, place, pseudo, mail, password) values (?,?,?,?,?)''', (id, str(pl), str(ps), str(ml), str(pd).encode("base64").encode("hex")))
            self.db.commit()
        except:
            pass

        finally:
            c.close()

######################################################################################

    def update_click(self, id, pl, ps, ml, pd):
        c = self.db.cursor()
        try:
            c.execute('''UPDATE passwd SET place = ?, pseudo = ?, mail = ?, password = ? WHERE id=?''', (str(pl), str(ps), str(ml), str(pd).encode("base64").encode("hex"), int(id)))
            self.db.commit()
        except:
            pass

        finally:
            c.close()

######################################################################################

    def isExisting(self, id):
        c = self.db.cursor()
        res = None
        try:
            c.execute('SELECT * FROM passwd WHERE id=%d' % int(id))
            self.db.commit()
            res = c.fetchone()
        except:
            pass
        
        finally:
            c.close()
            if res != None: return True
            else: return False

######################################################################################

    def check_pwd(self, pwd):
        if os.path.exists(self.keyfile):
            with open(self.keyfile, 'rb') as f:
                if md5.new(md5.new(((pwd).encode("base64")).encode("hex")).digest()).hexdigest() == f.read(): return True
                else: return False
                f.close()
        else: return False

######################################################################################

    def update_pwd(self, pwd):
        if os.path.exists(self.keyfile):
            os.remove(self.keyfile)
        with open(self.keyfile, 'wb') as f:
            f.write(md5.new(md5.new(((pwd).encode("base64")).encode("hex")).digest()).hexdigest())
            f.close()
        with open(self.keyfile, 'rb') as f:
            if md5.new(md5.new(((pwd).encode("base64")).encode("hex")).digest()).hexdigest() != f.read(): raise Exception, "Impossible to update password ..."
            f.close()
        return True

######################################################################################

    def get_pwd_by_id(self, id):
        c = self.db.cursor()
        res = None
        try:
            c.execute('SELECT * FROM passwd WHERE id=%d' % int(id))
            self.db.commit()
            res = c.fetchone()
        except:
            pass
        
        finally:
            c.close()
            return res

######################################################################################

    def del_pwd_by_id(self, id):
        c = self.db.cursor()
        res = None
        try:
            c.execute('DELETE FROM passwd WHERE id=%d' % int(id))
            self.db.commit()
        
        finally:
            c.close()
            return res
