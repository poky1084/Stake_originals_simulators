from tkinter import *
from tkinter import ttk
import aiohttp
import asyncio
import math
import random
import hmac
import hashlib
import sys
import time
import os
import configparser as cp
#import numpy as np
from threading import *

METHODS = ['BET', 'VERIFY']
CURRENCY = ['BTC', 'XRP', 'DOGE', 'ETH', 'LTC', 'TRX', 'BCH', 'EOS']
DISPLAY = ['COIN', 'USD', 'EUR', 'JPY']

api_key = ''
server_seed = '535e8f53eee1402b242c7eff4038787d3de850c3ba27bde6a370225e1a2f23dd'
client_seed = '8cf82c02b3'
ver_nonce = 1

pattern = [["five","queen","king","king","three"],["queen","jack","nine","nine","ten"],["ten","three","five","five","jack"],["three","queen","ten","ace","two"],["jack","ace","three","two","king"],["ace","wild","king","jack","ten"],["four","queen","jack","one","wild"],["ten","jack","wild","ten","king"],["queen","five","queen","four","nine"],["two","nine","ten","jack","one"],["nine","queen","three","three","ten"],["ten","three","nine","queen","five"],["scatter","king","jack","five","ace"],["queen","one","one","jack","jack"],["jack","jack","ace","ten","scatter"],["wild","two","ten","four","nine"],["queen","ten","four","ace","ace"],["ace","one","ace","queen","four"],["two","nine","king","scatter","queen"],["king","scatter","one","ten","ace"],["one","ace","nine","king","four"],["queen","four","ten","three","ten"],["five","ten","two","jack","five"],["king","king","queen","four","queen"],["four","two","nine","nine","three"],["ten","jack","four","ace","nine"],["one","queen","king","two","wild"],["nine","five","five","nine","jack"],["three","jack","nine","ace","two"],["ten","four","scatter","wild","queen"],["king","king","king","king","king"],["five","five","five","five","five"],["jack","jack","jack","jack","jack"],["ten","ten","ten","ten","ten"],["three","three","three","three","three"],["queen","queen","queen","queen","queen"],["four","four","four","four","four"],["nine","nine","nine","nine","nine"],["one","one","one","one","one"],["ace","ace","ace","ace","ace"],["nine","nine","nine","nine","nine"]]

paytable = {'wild':{'2':10,'3':200,'4':2000,'5':10000},
            'scatter':{'2':2,'3':6,'4':50,'5':500},
            'one':{'2':2,'3':25,'4':100,'5':750},
            'two':{'2':2,'3':25,'4':100,'5':750},
            'three':{'2':0,'3':15,'4':100,'5':400},
            'four':{'2':0,'3':10,'4':75,'5':250},
            'five':{'2':0,'3':10,'4':50,'5':250},
            'ace':{'2':0,'3':10,'4':50,'5':125},
            'king':{'2':0,'3':5,'4':50,'5':100},
            'queen':{'2':0,'3':5,'4':25,'5':100},
            'jack':{'2':0,'3':5,'4':25,'5':100},
            'ten':{'2':0,'3':5,'4':25,'5':100},
            'nine':{'2':2,'3':5,'4':25,'5':100}
            }
            

     

    
class App(Tk):
    
    run = 0
    data = ''
    
    thread_started = 0
    cfg_folder = './config/'
    cfg_file = 'data.ini'
    cfg_path = '{}{}'.format(cfg_folder, cfg_file)

    def __init__(self, loop):
        super().__init__()
        
        

        
        
        
        self.title('Scarab Spin Client')
        #self.geometry('1000x500')
        self.apikey = StringVar(self)
        self.s_seed = StringVar(self)
        self.c_seed = StringVar(self)
        self.seed_nonce = IntVar(self)
        self.update_seednonce = 0
        self.seed_nonce.set(ver_nonce)
        #self.s_seed.set(server_seed)
        #self.c_seed.set(client_seed)    
        
        if not os.path.isdir(self.cfg_folder):
            os.mkdir(self.cfg_folder)
     
        if not os.path.isfile(self.cfg_path):
            self.saveini()
        else:
            self.loadini()

        
        self.time_yr = 0
        self.time_mth = 0
        self.time_day = 0
        self.time_hr = 0
        self.time_min = 0
        self.time_sec = 0

        
        self.max_balances = [0]
        
        
        self.ver_bet = 0.0000033
        self.ver_minbet = self.ver_bet
        self.ver_wagered = 0
        self.ver_profit = 0
        self.ver_balance = 0.06615000
        self.ver_wins = 0
        self.ver_winstreak = 0
        self.ver_wstrk = []
        self.ver_wstrk.append(0)
        self.ver_lose = 0
        self.ver_losestreak = 0
        self.ver_lstrk = []
        self.ver_lstrk.append(0)     
        self.ver_nog = 0
        self.ver_multiply = 1
        
        self.bet_wagered = 0
        self.bet_profit = 0
        self.bet_balance = 0
        self.bet_wins = 0
        self.bet_winstreak = 0
        self.bet_wstrk = []
        self.bet_wstrk.append(0)
        self.bet_lose = 0
        self.bet_losestreak = 0
        self.bet_lstrk = []
        self.bet_lstrk.append(0)
        self.bet_nog = 0
        self.bet_multiply = 1        
        
        self.show_wagered = self.ver_wagered
        self.show_profit = self.ver_profit
        self.show_balance = self.ver_balance
        
        self.verify_wagered = StringVar(self)
        self.verify_profit = StringVar(self)
        self.verify_balance = StringVar(self)
        self.verify_wins = StringVar(self)
        self.verify_winstreak = StringVar(self)
        self.verify_loss = StringVar(self)
        self.verify_losestreak = StringVar(self)
        self.verify_nonce = StringVar(self)
        self.verify_nog = StringVar(self)
        self.verify_time = StringVar(self)
        
        self.bet_wagered = StringVar(self)
        self.bet_profit = StringVar(self)
        self.bet_balance = StringVar(self)
        self.bet_wins = StringVar(self)
        self.bet_winstreak = StringVar(self)
        self.bet_loss = StringVar(self)
        self.bet_losestreak = StringVar(self)
        self.bet_nonce = StringVar(self)
        self.bet_nog = StringVar(self)
        self.bet_time = StringVar(self)
        # -------------MENU------------------------
        self._labelframe_1 = LabelFrame(self, text = "Api", )
        self._labelframe_7 = LabelFrame(self, text = "Seed /  Nonce", )
        self._labelframe_8 = LabelFrame(self, borderwidth = 0, )
        self._labelframe_4 = LabelFrame(self, text = "Time Elapsed", )
        self._labelframe_9 = LabelFrame(self._labelframe_8, text = "Verify stat", font='Helvetica 18 bold' )
        self._labelframe_10 = LabelFrame(self._labelframe_8, text = "Bet stat", font='Helvetica 18 bold')
        self._label_5 = ttk.Label(self._labelframe_1, text = "Api Key:", )
        self._entry_2 = ttk.Entry(self._labelframe_1, textvariable = self.apikey, width = 30, )
        self.method_variable = StringVar(self._labelframe_1)
        self.method_variable.set(METHODS[0])
        self.method_menu = ttk.OptionMenu(self._labelframe_1, self.method_variable, METHODS[1], *METHODS)
        self.currency_variable = StringVar(self._labelframe_1)
        self.currency_variable.set(CURRENCY[0])
        self.currency_menu = ttk.OptionMenu(self._labelframe_1, self.currency_variable, CURRENCY[0], *CURRENCY)
        self._button_5 = ttk.Button(self._labelframe_1, text = "Start", command=self.start)
        self._button_6 = ttk.Button(self._labelframe_1, text = "Stop", command=self.stop)
        self._label_45 = ttk.Label(self._labelframe_1, text = "Show:",)
        self.display_variable = StringVar(self._labelframe_1)
        self.display_variable.set(DISPLAY[0])
        self.display_menu = ttk.OptionMenu(self._labelframe_1, self.display_variable, DISPLAY[0], *DISPLAY)
        
        #------------SEED--------------------------
        self._label_6 = ttk.Label(self._labelframe_7, text = "Server Seed", )
        self._entry_3 = ttk.Entry(self._labelframe_7, textvariable = self.s_seed, width = 30, )
        self._label_7 = ttk.Label(self._labelframe_7, text = "Client Seed", )
        self._entry_4 = ttk.Entry(self._labelframe_7, textvariable = self.c_seed, width = 30, )
        self._label_8 = ttk.Label(self._labelframe_7, text = "Start Nonce", )
        self._entry_5 = ttk.Entry(self._labelframe_7, textvariable = self.seed_nonce, width = 10, )
        
        #--------------VERIFY---------------------
        self._label_2 = ttk.Label(self._labelframe_9, text = "Wagered:", width = 10, )       
        self._label_1 = ttk.Label(self._labelframe_9, text = 0.00000000, width = 15, anchor = E, textvariable=self.verify_wagered)
        self._label_4 = ttk.Label(self._labelframe_9, text = "Profit:", width = 10, )
        self._label_3 = ttk.Label(self._labelframe_9, text = 0.00000000, width = 15, anchor = E, textvariable=self.verify_profit)
        self._label_13 = ttk.Label(self._labelframe_9, text = "Balance:", width = 10)
        self._label_14 = ttk.Label(self._labelframe_9, text = 0.00000000, width = 15, anchor = E, textvariable=self.verify_balance)
        self._label_15 = ttk.Label(self._labelframe_9, text = "Luck:", width = 10)
        self._label_16 = ttk.Label(self._labelframe_9, text = "_", width = 15, anchor = E,)
        self._label_17 = ttk.Label(self._labelframe_9, text = "Wins:", width = 10)
        self._label_18 = ttk.Label(self._labelframe_9, text = 0, width = 15, anchor = E, textvariable=self.verify_wins)
        self._label_19 = ttk.Label(self._labelframe_9, text = "Winstreak:", width = 10)
        self._label_20 = ttk.Label(self._labelframe_9, text = 0, width = 15, anchor = E, textvariable=self.verify_winstreak)
        self._label_41 = ttk.Label(self._labelframe_9, text = "Losses:", width = 10)
        self._label_40 = ttk.Label(self._labelframe_9, text = 0, width = 15, anchor = E, textvariable=self.verify_loss) 
        self._label_42 = ttk.Label(self._labelframe_9, text = "Losestreak:", width = 10)
        self._label_43 = ttk.Label(self._labelframe_9, text = 0, width = 15, anchor = E, textvariable=self.verify_losestreak)
        self._label_21 = ttk.Label(self._labelframe_9, text = "Nonce:", width = 10)
        self._label_22 = ttk.Label(self._labelframe_9, text = 1, width = 15, anchor = W, textvariable=self.verify_nonce)
        self._label_23 = ttk.Label(self._labelframe_9, text = "№ Bets:", width = 10)
        self._label_24 = ttk.Label(self._labelframe_9, text = 0, width = 15, anchor = W, textvariable=self.verify_nog )
        
        #------------------BET-----------------------------------
        self._label_12 = ttk.Label(self._labelframe_10, text = "Profit:", width = 10, )
        self._label_11 = ttk.Label(self._labelframe_10, text = 0.00000000, width = 15, anchor = E, textvariable=self.bet_profit )
        self._label_9 = ttk.Label(self._labelframe_10, text = "Wagered:", width = 10, )
        self._label_10 = ttk.Label(self._labelframe_10, text = 0.00000000, width = 15, anchor = E, textvariable=self.bet_wagered)
        self._label_25 = ttk.Label(self._labelframe_10, text = "Balance:", width = 10,)
        self._label_26 = ttk.Label(self._labelframe_10, text = 0.00000000, width = 15, anchor = E, textvariable=self.bet_balance)
        self._label_27 = ttk.Label(self._labelframe_10, text = "Luck:", width = 10,)
        self._label_28 = ttk.Label(self._labelframe_10, text = "_", width = 15, anchor = E, )
        self._label_29 = ttk.Label(self._labelframe_10, text = "Wins:", width = 10,)
        self._label_30 = ttk.Label(self._labelframe_10, text = 0, width = 15, anchor = E, textvariable=self.bet_wins)
        self._label_31 = ttk.Label(self._labelframe_10, text = "Winstreak:", width = 10,)
        self._label_32 = ttk.Label(self._labelframe_10, text = 0, width = 15, anchor = E, textvariable=self.bet_winstreak)
        self._label_33 = ttk.Label(self._labelframe_10, text = "Losses:", width = 10,)
        self._label_34 = ttk.Label(self._labelframe_10, text = 0, width = 15, anchor = E, textvariable=self.bet_loss)
        self._label_35 = ttk.Label(self._labelframe_10, text = "Losestreak:", width = 10,)
        self._label_36 = ttk.Label(self._labelframe_10, text = 0, width = 15, anchor = E, textvariable=self.bet_losestreak)
        self._label_44 = ttk.Label(self._labelframe_10, text = "Bets:", width = 10,)
        self._label_48 = ttk.Label(self._labelframe_10, text = 0, width = 15, anchor = W, textvariable=self.bet_nog)
        
        #---------------TIME--------------------------------
        self._label_37 = ttk.Label(self._labelframe_4, text = "_label_37", width = 50, textvariable=self.bet_time)
        self._label_38 = ttk.Label(self._labelframe_4, text = "_label_38", width = 50, textvariable=self.verify_time)
        
        #--------------strategy-------------
        self._button_1 = ttk.Button(self._labelframe_9, text = "Strategy", command=self.strategybox)
        self._button_2 = ttk.Button(self._labelframe_10, text = "Strategy", command=self.strategybox)

        #----reset-----
        self._button_3 = ttk.Button(self._labelframe_9, text = "Reset", command=self.reset_verify)
        self._button_4 = ttk.Button(self._labelframe_10, text = "Reset", command=self.reset_bet)
        
        #currency
        #self._button_5 = Tkinter.Button(self._labelframe_1,text = "Currency",command=self.set_currency)
        # widget commands
      



        # Geometry Management
        self._labelframe_1.grid( in_ = self, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._labelframe_7.grid( in_ = self, column = 1, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._labelframe_8.grid( in_ = self, column = 1, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._labelframe_4.grid( in_ = self, column = 1, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._labelframe_9.grid( in_ = self._labelframe_8, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._labelframe_10.grid( in_ = self._labelframe_8, column = 2, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._label_5.grid( in_ = self._labelframe_1, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._entry_2.grid( in_ = self._labelframe_1, column = 2, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "ew")
        self.method_menu.grid( in_ = self._labelframe_1, column = 3, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_5.grid( in_ = self._labelframe_1, column = 4, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_6.grid( in_ = self._labelframe_1, column = 5, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_6.grid( in_ = self._labelframe_7, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._entry_3.grid( in_ = self._labelframe_7, column = 2, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "ew")
        self._label_7.grid( in_ = self._labelframe_7, column = 3, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._entry_4.grid( in_ = self._labelframe_7, column = 4, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "ew")
        self._label_8.grid( in_ = self._labelframe_7, column = 5, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._entry_5.grid( in_ = self._labelframe_7, column = 6, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "ew")
        self._label_10.grid( in_ = self._labelframe_10, column = 4, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_1.grid( in_ = self._labelframe_9, column = 4, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_2.grid( in_ = self._labelframe_9, column = 3, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_3.grid( in_ = self._labelframe_9, column = 2, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_4.grid( in_ = self._labelframe_9, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_9.grid( in_ = self._labelframe_10, column = 3, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_11.grid( in_ = self._labelframe_10, column = 2, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_12.grid( in_ = self._labelframe_10, column = 1, row = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_13.grid( in_ = self._labelframe_9, column = 1, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_14.grid( in_ = self._labelframe_9, column = 2, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_15.grid( in_ = self._labelframe_9, column = 3, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_16.grid( in_ = self._labelframe_9, column = 4, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_17.grid( in_ = self._labelframe_9, column = 1, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_18.grid( in_ = self._labelframe_9, column = 2, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_19.grid( in_ = self._labelframe_9, column = 3, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_20.grid( in_ = self._labelframe_9, column = 4, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_21.grid( in_ = self._labelframe_9, column = 1, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_22.grid( in_ = self._labelframe_9, column = 2, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_23.grid( in_ = self._labelframe_9, column = 3, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_24.grid( in_ = self._labelframe_9, column = 4, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_25.grid( in_ = self._labelframe_10, column = 1, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_26.grid( in_ = self._labelframe_10, column = 2, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_27.grid( in_ = self._labelframe_10, column = 3, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_28.grid( in_ = self._labelframe_10, column = 4, row = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_29.grid( in_ = self._labelframe_10, column = 1, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_30.grid( in_ = self._labelframe_10, column = 2, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_31.grid( in_ = self._labelframe_10, column = 3, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_32.grid( in_ = self._labelframe_10, column = 4, row = 3, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_33.grid( in_ = self._labelframe_10, column = 1, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_34.grid( in_ = self._labelframe_10, column = 2, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_35.grid( in_ = self._labelframe_10, column = 3, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_36.grid( in_ = self._labelframe_10, column = 4, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_40.grid( in_ = self._labelframe_9, column = 2, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_41.grid( in_ = self._labelframe_9, column = 1, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_42.grid( in_ = self._labelframe_9, column = 3, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_43.grid( in_ = self._labelframe_9, column = 4, row = 4, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_44.grid( in_ = self._labelframe_10, column = 3, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_48.grid( in_ = self._labelframe_10, column = 4, row = 8, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_37.grid( in_    = self._labelframe_4, column = 2, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_38.grid( in_    = self._labelframe_4, column = 1, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        #----strat====
        self._button_1.grid( in_    = self._labelframe_9, column = 4, row    = 7, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_2.grid( in_    = self._labelframe_10, column = 4, row    = 7, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        #----reset
        self._button_3.grid( in_    = self._labelframe_9, column = 3, row    = 7, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_4.grid( in_    = self._labelframe_10, column = 3, row    = 7, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        #-currency 
        self.currency_menu.grid(in_    = self._labelframe_1,column = 6,row    = 1,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "")
        self.display_menu.grid( in_    = self._labelframe_1, column = 8, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._label_45.grid( in_    = self._labelframe_1, column = 7, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        # Resize Behavior
        self.grid_rowconfigure(1, weight = 0, minsize = 26, pad = 0)
        self.grid_rowconfigure(2, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(3, weight = 0, minsize = 299, pad = 0)
        self.grid_rowconfigure(4, weight = 0, minsize = 40, pad = 0)
        self.grid_columnconfigure(1, weight = 0, minsize = 514, pad = 0)
        self._labelframe_1.grid_rowconfigure(1, weight = 0, minsize = 3, pad = 0)
        self._labelframe_1.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(3, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(4, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(5, weight = 0, minsize = 40, pad = 0)
        self._labelframe_10.grid_rowconfigure(1, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(2, weight = 0, minsize = 6, pad = 0)
        self._labelframe_10.grid_rowconfigure(3, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(4, weight = 0, minsize = 2, pad = 0)
        self._labelframe_10.grid_rowconfigure(5, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(6, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(7, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(8, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(9, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(10, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(11, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_rowconfigure(12, weight = 0, minsize = 5, pad = 0)
        self._labelframe_10.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_10.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_10.grid_columnconfigure(3, weight = 0, minsize = 40, pad = 0)
        self._labelframe_10.grid_columnconfigure(4, weight = 0, minsize = 40, pad = 0)
        self._labelframe_4.grid_rowconfigure(1, weight = 0, minsize = 17, pad = 0)
        self._labelframe_4.grid_rowconfigure(2, weight = 0, minsize = 2, pad = 0)
        self._labelframe_4.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_4.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_rowconfigure(1, weight = 0, minsize = 14, pad = 0)
        self._labelframe_7.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_columnconfigure(3, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_columnconfigure(4, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_columnconfigure(5, weight = 0, minsize = 40, pad = 0)
        self._labelframe_7.grid_columnconfigure(6, weight = 0, minsize = 40, pad = 0)
        self._labelframe_8.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_8.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_8.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_9.grid_rowconfigure(1, weight = 0, minsize = 7, pad = 0)
        self._labelframe_9.grid_rowconfigure(2, weight = 0, minsize = 2, pad = 0)
        self._labelframe_9.grid_rowconfigure(3, weight = 0, minsize = 2, pad = 0)
        self._labelframe_9.grid_rowconfigure(4, weight = 0, minsize = 2, pad = 0)
        self._labelframe_9.grid_rowconfigure(5, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(6, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(7, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(8, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(9, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(10, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(11, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_rowconfigure(12, weight = 0, minsize = 5, pad = 0)
        self._labelframe_9.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_9.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_9.grid_columnconfigure(3, weight = 0, minsize = 40, pad = 0)
        self._labelframe_9.grid_columnconfigure(4, weight = 0, minsize = 40, pad = 0)

        
        self.loop = loop
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.rotator(1/60, self)))

        self.tasks.append(loop.create_task(self.currency_update()))
        self.tasks.append(loop.create_task(self.updater()))
        
    def strategybox(self):
        self.win = Toplevel()
        self.win.wm_title("Window")
        self._labelframe_1 = LabelFrame(self.win, text = "Strategy",)
        self._frame_1 = Frame(self.win,)
        self._button_1 = ttk.Button(self._frame_1, text = "Save",)
        self._button_2 = ttk.Button(self._frame_1, text = "Load",)
        self._button_3 = ttk.Button(self._labelframe_1, text = "_button_3",)
        # Geometry Management
        self._labelframe_1.grid( in_    = self.win, column = 1, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._frame_1.grid( in_    = self.win, column = 1, row    = 2, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "news")
        self._button_1.grid( in_    = self._frame_1, column = 1, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_2.grid( in_    = self._frame_1, column = 2, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        self._button_3.grid( in_    = self._labelframe_1, column = 1, row    = 1, columnspan = 1, ipadx = 0, ipady = 0, padx = 0, pady = 0, rowspan = 1, sticky = "")
        # Resize Behavior
        self.win.grid_rowconfigure(1, weight = 0, minsize = 262, pad = 0)
        self.win.grid_rowconfigure(2, weight = 0, minsize = 12, pad = 0)
        self.win.grid_columnconfigure(1, weight = 0, minsize = 442, pad = 0)
        self._frame_1.grid_rowconfigure(1, weight = 0, minsize = 11, pad = 0)
        self._frame_1.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._frame_1.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_rowconfigure(2, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self._labelframe_1.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)

    async def rotator(self, interval, command):
        while await asyncio.sleep(interval, True):
            if (self.run == 1 and self.method_variable.get() == 'BET'):
                self.data = await roll()
                try:

                    
                    index = self.data['data']['slotsBet']['state']['rounds'][0]['offsets']
                    payout = self.data['data']['slotsBet']['payoutMultiplier']
                    
                    line = indexed(index)
                    
                    #print(line[0])
                    #print(line[1])
                    #print(line[2])
                    #print(payout)
                    #print('')
                    lines = []
                    lines.extend(line[0])
                    lines.extend(line[1])
                    lines.extend(line[2])
                    
                    if self.is_sublist(['scatter', 'wild', 'wild'], line[1]) and float(payout) >= 0:
                        print(line[0])
                        print(line[1])
                        print(line[2])
                        print(payout)
                        print('')
                except Exception as e: 
                    print(e)
                #print(self.data)
    
    def is_sublist(self, a, b):
        if not a: return True
        if not b: return False
        return b[:len(a)] == a or self.is_sublist(a, b[1:])   
        
    def reset_verify(self):
        self.ver_wagered = 0.00000000
        self.ver_profit = 0.00000000
        self.ver_balance = 0
        self.ver_wins = 0
        self.ver_winstreak = 0
        self.ver_wstrk = []
        self.ver_wstrk.append(0)
        self.ver_lose = 0
        self.ver_losestreak = 0
        self.ver_lstrk = []
        self.ver_lstrk.append(0)
        self.ver_nog = 0
        
    def reset_bet(self):
        pass

   



        
 
                
 
           
            
    def ver(self):
        global ver_nonce
        while True:
            #time.sleep(0.01)
            if (self.run == 0):
                break

            index = verify(self.server_seed, self.client_seed, ver_nonce)
            

            self.ver_nog += 1
            self.ver_wagered += self.ver_bet
           
            #print(payout)
            #print(index)
            
            line = indexed(index)
            payout = payouts(line) 
            lines = []
            lines.extend(line[0])
            lines.extend(line[1])
            lines.extend(line[2])
            
           # if lines.count('scatter') > 4:
                #print(line[0])
                #print(line[1])
                #print(line[2])
                #print(payout)  
                #print(ver_nonce)
            
            ver_nonce += 1
                                       
            if(payout > 0):
                self.ver_losestreak = 0                
                self.ver_wins += 1
                self.ver_winstreak += 1
                self.ver_wstrk.append(self.ver_winstreak)
                self.ver_profit += (self.ver_bet*payout)-self.ver_bet
                self.ver_balance += (self.ver_bet*payout)-self.ver_bet
                
                print("win. x", payout, "line 2: ", line[0], " line 1: ", line[1], " line 3: ", line[2])
                #self.ver_bet = 0.0001

                
                    
 
            else:
                self.ver_winstreak = 0
                self.ver_profit -= self.ver_bet
                self.ver_balance -= self.ver_bet
                self.ver_lose += 1
                self.ver_losestreak += 1
                
                self.ver_lstrk.append(self.ver_losestreak)
                self.max_balances.append(self.ver_balance)
                self.max_balances = [max(self.max_balances)]
                print("lose. x0 line 2: ", line[0], " line 1: ", line[1], " line 3: ", line[2])
                
            #if random.randint(1,100) == 100:
                #self.ver_bet *= 1.5
            #if self.ver_bet < 0.00000001:
                #self.ver_bet = 0.00000001
            if self.ver_balance <= self.ver_bet:
                break

            self.ver_wstrk = [max(self.ver_wstrk)]
            self.ver_lstrk = [max(self.ver_lstrk)]    
            total = self.ver_wins+self.ver_lose
            duration = total*300
            t = dt(duration)
            self.time_yr = t['y']
            self.time_mth = t['mo']
            self.time_day = t['d']
            self.time_hr = t['h']
            self.time_min = t['m']
            self.time_sec = t['s']
            
            if (ver_nonce % 288000 == 0):
                pass
                #print(self.nonce)
                
    async def currency_update(self):
        while await asyncio.sleep(1/60, True):
            if (self.display_variable.get() == 'COIN'):
                self.verify_wagered.set("{0:.8f}".format(self.ver_wagered))
                self.verify_balance.set("{0:.8f}".format(self.ver_balance))#self.max_balances[0]
                self.verify_profit.set("{0:.8f}".format(self.ver_profit))
            if (self.display_variable.get() == 'USD'):
                self.show_wagered = self.ver_wagered * 39634.89
                self.show_profit = self.ver_profit * 39634.89
                self.show_balance = self.ver_balance * 39634.89
                self.verify_profit.set("{0:.8f}".format(self.show_profit))
                self.verify_wagered.set("{0:.8f}".format(self.show_wagered))
                
            
            
    async def updater(self):
        while await asyncio.sleep(1/60, True):
            if self.update_seednonce == 1:
                self.update_seednonce = 0
                self.seed_nonce.set(ver_nonce)                
                        
            self.verify_wins.set(self.ver_wins)
            self.verify_winstreak.set(max(self.ver_wstrk))
            self.verify_loss.set(self.ver_lose)
            self.verify_losestreak.set(max(self.ver_lstrk))
            self.verify_nonce.set(ver_nonce)
            self.verify_nog.set(self.ver_nog)
            self.verify_time.set('{} year {} month {} day -- {:02d}:{:02d}:{:02d}'.format(self.time_yr, self.time_mth, self.time_day, self.time_hr, self.time_min, self.time_sec))
            #self.stat_nonce.configure(text=self.up_verify_nonce)
            #self.bet_label.update();        
            self.update()

    def close(self):
        self.saveini()
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()
        
    def saveini(self):
        config = cp.ConfigParser()
        config['API'] = {
            'APIKEY': self.apikey.get(),
            'SERVER_SEED': self.s_seed.get(),
            'CLIENT_SEED': self.c_seed.get(),
            'NONCE': self.seed_nonce.get()
            }
        config['BET STRATEGY'] = {
            'APIKEY': self.apikey.get(),
            'SERVER_SEED': self.s_seed.get(),
            'CLIENT_SEED': self.c_seed.get(),
            'NONCE': self.seed_nonce.get()
            }
        config['VERIFY STRATEGY'] = {
            'APIKEY': self.apikey.get(),
            'SERVER_SEED': self.s_seed.get(),
            'CLIENT_SEED': self.c_seed.get(),
            'NONCE': self.seed_nonce.get()
            }
        with open(self.cfg_path, 'w') as configfile:
            config.write(configfile)
            
    def loadini(self):
        config = cp.ConfigParser()
        config.read(self.cfg_path)
        api_key = config['API']['APIKEY']
        server_seed = config['API']['SERVER_SEED']
        client_seed = config['API']['CLIENT_SEED']
        ver_nonce = config['API']['NONCE']
        
        self.apikey.set(api_key)
        self.s_seed.set(server_seed)
        self.c_seed.set(client_seed)
        self.seed_nonce.set(ver_nonce)
        
        
        
    def start (self):
        global api_key
        global server_seed
        global client_seed
        global ver_nonce
        api_key = self.apikey.get()
        server_seed = self.s_seed.get()
        client_seed = self.c_seed.get()
        ver_nonce = self.seed_nonce.get()
        if (self.method_variable.get() == 'VERIFY'):
            self.run = 1
            self.server_seed = self.s_seed.get()
            self.client_seed = self.c_seed.get()
            print(self.server_seed)
            if self.thread_started == 0:
                ver_nonce = self.seed_nonce.get()
                self.thread_started = 1
                self.thread = Thread(target = self.ver)
                self.thread.daemon = True
                self.thread.start()
            pass        
        if (self.method_variable.get() == 'BET'):
            self.run = 1

    def stop (self):
        self.update_seednonce = 1
        self.seed_nonce.set(ver_nonce)
        self.run = 0  
        self.thread_started = 0
        self.index = 0

def dt (d):
	dt = {
		'ms': math.floor((d % 1000)),
		'd': math.floor((d / (1000 * 60 * 60 * 24)) % 30),
		'mo': math.floor((d / (1000 * 60 * 60 * 24 * 30)) % 12),
		'y': math.floor((d / (1000 * 60 * 60 * 24 * 30 * 12)) % 100),
		'h': math.floor((d / (1000 * 60 * 60)) % 24),
		'm': math.floor((d / (1000 * 60)) % 60),
		's': math.floor((d / 1000) % 60),
	}
	return dt;


        
def op(roll, condition, target):
    op = {
        'above': roll > target,
        'below': roll < target,
    }
    return op[condition];
    
async def roll ():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.stake.com/graphql', json={"operationName":"slotBet","variables":{"currency":"btc","amount":0,"lines":1,"identifier":"60aaff979c0f5717fc94"},"query":"mutation slotBet($amount: Float!, $lines: Int!, $currency: CurrencyEnum!, $identifier: String!) {\n  slotsBet(amount: $amount, currency: $currency, lines: $lines, identifier: $identifier) {\n    ...CasinoBetFragment\n    state {\n      ...SlotsStateFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CasinoBetFragment on CasinoBet {\n  id\n  active\n  payoutMultiplier\n  amountMultiplier\n  amount\n  payout\n  updatedAt\n  currency\n  game\n  user {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment SlotsStateFragment on CasinoGameSlots {\n  lines\n  rounds {\n    offsets\n    paylines {\n      payline\n      hits\n      multiplier\n      symbol\n      __typename\n    }\n    scatterMultiplier\n    roundMultiplier\n    totalMultiplier\n    bonusRemaining\n    bonusTotal\n    __typename\n  }\n  __typename\n}\n"}
, headers = {'x-access-token': '12345'}) as resp:
            data = await resp.json()
            return data
           
 
def verify ( serverSeed, clientSeed, nonce):
    round = 0
    nonceSeed = '{}:{}:{}'.format(clientSeed, nonce, round)
    hex = hmac.new(bytes(serverSeed, 'utf-8'), bytes(nonceSeed, 'utf-8'), hashlib.sha256).hexdigest()[0:40]
    i = 0
    end = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    while i < 4:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1)
        i+=1
    frac, one = math.modf(end * 30)   
    end = 0
    while i < 8:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1-4)
        i+=1
    frac, two = math.modf(end * 30)   
    end = 0
    while i < 12:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1-8)
        i+=1
    frac, three = math.modf(end * 30)
    end = 0
    while i < 16:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1-12)
        i+=1
    frac, four = math.modf(end * 30)
    end = 0
    while i < 20:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1-16)
        i+=1
    frac, five = math.modf(end * 41)
    index = [int(one), int(two), int(three), int(four), int(five)]
    return index

def indexed(index):
    global pattern
    one = []                                
    two = []
    three = []
    for i in range(len(index)):
        index2 = index[i]-1
        index3 = index[i]+1 
        if index2 < 0:
            if i > 3:
                index2 = 40
                #print(index2)
            else:
                index2 = 29             
        if index3 > 29 and i < 4:
            index3 = 0
        if index3 > 40:
            index3 = 0 

        two.append(pattern[index2][i])
        one.append(pattern[index[i]][i])
        three.append(pattern[index3][i])             
    return [two, one, three]

def wilds(symbol, index):
    global paytable
    payout = 0
    wilds = 0
    while index <= 5:
        if 'wild' in symbol[1][0:index]:
            #print(symbol[1])
            #print(index)
            nowild = list(filter(lambda a: a != 'wild', symbol[1][0:index]))
            #print(nowild)               
            wilds = symbol[1][0:index].count('wild')
            if len(nowild) > 0:
                if nowild.count(nowild[0]) == len(nowild):
                    if wilds >= 2 and 'scatter' not in nowild:
                        if paytable[nowild[0]][str(index)] * 2 > paytable['wild'][str(wilds)]:
                            payout = paytable[nowild[0]][str(index)] * 2                            

                        else:
                            payout = paytable['wild'][str(wilds)] 
                    elif wilds < 2 and symbol[1][0:index].count('scatter') == 0:
                        payout = paytable[nowild[0]][str(index)] * 2 
                    
            elif wilds > 1 and len(nowild) == 0:
                payout = paytable['wild'][str(wilds)] 
                

          
        index += 1
    return payout 
    
def payouts(line):
    global paytable
    global server_seed
    global client_seed
    global ver_nonce

    
    payout = 0
    prev = ''
    a = []
    for i in range(len(line[1])):
        if line[1][i] != prev:
            a.append(1)
        else:
            a[len(a)-1] += 1
        prev = line[1][i]
    if 'wild' in line[1]:
        payout = wilds(line, 2)
    else:    
        if a[0] > 1 and line[1][0] != 'scatter':
            payout = paytable[line[1][0]][str(a[0])]
        
    lines = []
    lines.extend(line[0])
    lines.extend(line[1])
    lines.extend(line[2])
    if lines.count('scatter') > 1:
        payout += paytable['scatter'][str(lines.count('scatter'))]
    if lines.count('scatter') > 2:
        rounds = 15
        current = 1
        index = verify_bonus(server_seed, client_seed, ver_nonce, rounds, current)
        line = index['line']
        payout += index['payout']

        print(payout)  
        print(ver_nonce) 


        #print(a)
    return payout  

def bonus_payouts(line, rounds):
    global paytable
    payout = 0
    prev = ''
    a = []

    for i in range(len(line[1])):
        if line[1][i] != prev:
            a.append(1)
        else:
            a[len(a)-1] += 1
        prev = line[1][i]
    if 'wild' in line[1]:
        payout = wilds(line, 2) * 3
    else:    
        if a[0] > 1 and line[1][0] != 'scatter':
            payout = paytable[line[1][0]][str(a[0])] * 3
        
    lines = []
    lines.extend(line[0])
    lines.extend(line[1])
    lines.extend(line[2])
    if lines.count('scatter') > 1:
        payout += paytable['scatter'][str(lines.count('scatter'))] * 3
    if lines.count('scatter') > 2:
        rounds += 15


   
    #print(a)
    return [payout, rounds] 
       
  
    

obj = {'line':[],'payout':0} 
def verify_bonus ( serverSeed, clientSeed, nonce, rounds, current):
    

    
    hex = hexgen(serverSeed, clientSeed, nonce)
    #print(hex)


    i = 0
    digest = 0
    if current >= 1:
        i = 20
        digest = 20
    end = 0
    pow = 1
    payout = 0
    multier = 30
    index = []    

        
     
      
    while current <= rounds and rounds <= 180:    
        while len(index) < 5: 
            while i < digest+4 and pow < 5:
                end += int(hex[i*2:i*2+2], 16) / math.pow(256, pow)            
                pow+=1
                i+=1
                
            if len(index) > 3:
                multier = 41
            else:
                multier = 30
            index.append(int(end * multier))
            pow = 1
            digest+=4
            end = 0
        
        
        
        
    
        line = indexed(index) 
        index = []
        bonus = bonus_payouts(line, rounds)
        payout += bonus[0]
        rounds = bonus[1]
        #print('{}/{}'.format(current, rounds))
        #print(line[0])
        #print(line[1])
        #print(line[2])
        #print(bonus[0])
        
        current += 1
        #print(rounds)
    
        obj['line'] = line
        obj['payout'] = payout
    
    return obj

def hexgen(serverSeed, clientSeed, nonce): 
    hex = ''
    round = 0
    while round < 190:
        nonceSeed = '{}:{}:{}'.format(clientSeed, nonce, round)
        hex += hmac.new(bytes(serverSeed, 'utf-8'), bytes(nonceSeed, 'utf-8'), hashlib.sha256).hexdigest()
        round += 1
    return hex


loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
loop.close()