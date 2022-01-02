from tkinter import *
from tkinter import ttk
import aiohttp
import asyncio
import math
import hmac
import hashlib
import sys
import time
import os
import random
import configparser as cp
#import numpy as np
from threading import *
METHODS = ['BET', 'VERIFY']

class App(Tk):
    
    run = 0
    data = ''
    
    thread_started = 0
    cfg_folder = './config/'
    cfg_file = 'data.ini'
    cfg_path = '{}{}'.format(cfg_folder, cfg_file)
    
    def __init__(self, loop):
        super().__init__()
        self.server_seed = '535e8f53eee1402b242c7eff4038787d3de850c3ba27bde6a370225e1a2f23dd'
        self.client_seed = '8cf82c02b3'
        self.api_key = ''

        
        
        
        self.title('Mines Client')
        #self.geometry('1000x500')
        self.apikey = StringVar(self)
        self.s_seed = StringVar(self)
        self.c_seed = StringVar(self)
        self.seed_nonce = IntVar(self)
        self.update_seednonce = 0
        self.ver_nonce = 1
        self.seed_nonce.set(self.ver_nonce)
        self.s_seed.set(self.server_seed)
        self.c_seed.set(self.client_seed)    
        
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
        self.edge = 1;
        self.maxroll = 100
        
        self.ver_fields = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
        
        #44 losestreak max
        self.ver_mines = 2
        self.ver_bet = 25
        self.ver_minbet = 1
        self.ver_multiply = 34
        self.rounds = 0
        self.curr = ''
        self.choose = []
        self.picks = 0
        
        self.ver_wagered = 0
        self.ver_profit = 0
        self.ver_maxbal = 0
        self.ver_bal = 836466
        #bal 7596730
        #bal 836466
        self.ver_wins = 0
        self.ver_winstreak = 0
        self.ver_wstrk = []
        self.ver_wstrk.append(0)
        self.ver_lose = 0
        self.ver_losestreak = 0
        self.ver_lstrk = []
        self.ver_lstrk.append(0)
        self.ver_nog = 0
        
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
        self._button_5 = ttk.Button(self._labelframe_1, text = "Start", command=self.start)
        self._button_6 = ttk.Button(self._labelframe_1, text = "Stop", command=self.stop)
        
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

        #self.tasks.append(loop.create_task(self.ver(1/60, self)))
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
                print(self.data)
                              
    def reset_verify(self):
        self.ver_wagered = 0
        self.ver_profit = 0
        self.ver_maxbal = 0
        self.ver_bal = 836466
        self.ver_bet = 25
        self.ver_wins = 0
        self.ver_winstreak = 0
        self.ver_wstrk = []
        self.ver_wstrk.append(0)
        self.ver_lose = 0
        self.ver_losestreak = 0
        self.ver_lstrk = []
        self.ver_lstrk.append(0)
        self.ver_nog = 0
        self.ver_bet = self.ver_minbet
        
    def reset_bet(self):
        pass
    
       
    def ver(self):
        while True:
            #time.sleep(0.01)
            if (self.run == 0):
                break

            mine = verify(self.server_seed, self.client_seed, self.ver_nonce)[0:self.ver_mines]
            #print(mine)
            self.ver_nonce += 1
            self.ver_nog += 1
            self.ver_wagered += self.ver_bet
            multi = 1
            
            diamonds = len(self.ver_fields)
            payout = calculate_multiplier(self.ver_mines, diamonds)
            #print(payout)
            #payout = 5.0043955
            #6.2554946 3 mines 10 picks
            #1.2857143 3 mines 2 picks
            #297.00
            #8.25 2 mines 16 picks
            #24.75 1 mines 24 picks
             #66.4125 5 mines 13 picks

            #multi =( 1 / ( payout - 1)) + 1
            #print(multi)
            #self.ver_fields = random.randint(1, 25)
            #print(payout)
            #print(common_elements(mine, self.ver_fields))
            if common_elements(mine, self.ver_fields) == False:
                self.ver_losestreak = 0
                self.ver_maxbal = 0
                self.ver_wins += 1
                self.ver_winstreak += 1
                self.ver_wstrk.append(self.ver_winstreak)
                self.ver_profit += (self.ver_bet*payout)-self.ver_bet
                self.ver_bal += (self.ver_bet*payout)-self.ver_bet
                #self.ver_bal = 836466
                
                self.curr = (self.ver_bet*payout)-self.ver_bet
                print('bet {} profit {} payout {} choosen{} bombs{} total {} bal {}'.format('{0:.8f}'.format(self.ver_bet / 100000000), '{0:.8f}'.format(self.curr / 100000000), payout, self.ver_fields, [mine], '{0:.8f}'.format(self.ver_profit / 100000000), '{0:.8f}'.format(self.ver_bal / 100000000)))  
                #self.ver_fields = [random.randint(0,24)]
                
                self.ver_bet = 1000
                  
 
            else:
                self.ver_winstreak = 0
                self.ver_profit -= self.ver_bet
                self.ver_bal -= self.ver_bet
                self.curr = 0-self.ver_bet
                self.ver_maxbal = self.ver_bet * self.ver_multiply + self.ver_minbet
                self.ver_lose += 1
                self.ver_losestreak += 1
                
                self.ver_lstrk.append(self.ver_losestreak)
                self.max_balances.append(self.ver_maxbal)
                self.max_balances = [max(self.max_balances)]
                print('bet {} profit {} payout {} choosen{} bombs{} total {} bal {}'.format('{0:.8f}'.format(self.ver_bet / 100000000), '{0:.8f}'.format(self.curr / 100000000), payout, self.ver_fields, [mine], '{0:.8f}'.format(self.ver_profit / 100000000), '{0:.8f}'.format(self.ver_bal / 100000000)))  
                self.ver_bet *= 1
                
            
            
            
            
            
            
            if len(self.ver_fields) < 13:
                self.picks+=2            
                self.ver_fields.append(self.picks)
                
            else:
                self.picks = 0
                self.ver_fields = [0]

            #self.ver_fields.remove(random.randint(0,24))
            #self.ver_fields.remove(random.randint(0,24))
            #two = random.sample(range(0, 24), 2)
            #self.ver_fields.remove(two[0])
            #self.ver_fields.remove(two[1])
            #print(self.ver_fields)
            #38 losestreak max odd()
            # 37 losestreak max even() balance start 836466
            #46 even() later nonce
           #47 losestreak 5 day 
            #54 losestreak 5-13 day nonce 3887405
                

                
            if self.ver_bet < 1:
                self.ver_bet = 1
            if self.ver_bal < self.ver_bet:
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
            
            if (self.ver_nonce % 288000 == 0):
                pass
                #print(self.nonce)
                    
    async def updater(self):
        while await asyncio.sleep(1/60, True):
            if self.update_seednonce == 1:
                self.update_seednonce = 0
                self.seed_nonce.set(self.ver_nonce)
            self.verify_wagered.set("{0:.8f}".format(self.ver_wagered / 100000000))
            self.verify_balance.set("{0:.8f}".format(self.ver_bal / 100000000))
            #self.verify_balance.set("{0:.8f}".format(self.max_balances[0]))
            self.verify_profit.set("{0:.8f}".format(self.ver_profit / 100000000))
            self.verify_wins.set(self.ver_wins)
            self.verify_winstreak.set(max(self.ver_wstrk))
            self.verify_loss.set(self.ver_lose)
            self.verify_losestreak.set(max(self.ver_lstrk))
            self.verify_nonce.set(self.ver_nonce)
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
        self.apikey.set(config['API']['APIKEY'])
        self.s_seed.set(config['API']['SERVER_SEED'])
        self.c_seed.set(config['API']['CLIENT_SEED'])
        self.seed_nonce.set(config['API']['NONCE'])
        
        
        
    def start (self):
        if (self.method_variable.get() == 'VERIFY'):
            self.run = 1
            self.server_seed = self.s_seed.get()
            self.client_seed = self.c_seed.get()
            print(self.server_seed)
            if self.thread_started == 0:
                self.ver_nonce = self.seed_nonce.get()
                self.thread_started = 1
                self.thread = Thread(target = self.ver)
                self.thread.daemon = True
                self.thread.start()
            pass        
        if (self.method_variable.get() == 'BET'):
            self.run = 1

    def stop (self):
        self.update_seednonce = 1
        self.seed_nonce.set(self.ver_nonce)
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

def payouts(condition, target, edge, maxroll):
    if condition == 'above':
        payout = float(((maxroll-edge)/(maxroll-target)))
        return payout
    else:
        payout = float(((maxroll-edge)/(target)));
        return payout
        
def op(roll, condition, target):
    op = {
        'above': roll > target,
        'below': roll < target,
    }
    return op[condition];
    
async def roll ():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.stake.com/graphql', json={
        'operationName':'DiceRoll',
        'variables':{'currency':'btc','amount':0,'target':1,'condition':'above','identifier':'b1870b5366230fbe14fd'},
        'query':'mutation DiceRoll($amount: Float!, $target: Float!, $condition: CasinoGameDiceConditionEnum!, $currency: CurrencyEnum!, $identifier: String!) {\n  diceRoll(amount: $amount, target: $target, condition: $condition, currency: $currency, identifier: $identifier) {\n    ...CasinoBetFragment\n    state {\n      ...DiceStateFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CasinoBetFragment on CasinoBet {\n  id\n  active\n  payoutMultiplier\n  amountMultiplier\n  amount\n  payout\n  updatedAt\n  currency\n  game\n  user {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment DiceStateFragment on CasinoGameDice {\n  result\n  target\n  condition\n  __typename\n}\n'
    }, headers = {'x-access-token': '12345'}) as resp:
            data = await resp.json()
            return data
           
def odd(mines):
    return any(n % 2 == 1 for n in mines)

def even(mines):
    return any(n % 2 == 0 for n in mines)

def nCr(n,r):
  f = math.factorial
  return f(n) // f(r) // f(n-r)

def calculate_multiplier(mines, diamonds):
  house_edge = 0.01
  return (1 - house_edge) * nCr(25, diamonds) / nCr(25 - mines, diamonds)


    
def verify ( serverSeed, clientSeed, nonce ):
    round = 0
    nonceSeed = '{}:{}:{}'.format(clientSeed, nonce, round)
    hex = hmac.new(bytes(serverSeed, 'utf-8'), bytes(nonceSeed, 'utf-8'), hashlib.sha256).hexdigest()[0:8]
    i = 0
    end = 0
    while i < 4:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1)
        i+=1 
    frac, whole = math.modf(end * 25)
    return str(whole)

def common_elements(list_1, list_2):
    a_set = set(list_1)
    b_set = set(list_2)
    if (a_set & b_set):
        return True
    else:
        return False

def nums_to_mine_array(nums) :
    mines = [];
    i = 0
    while i < 25:
        mines.append(i);
        i+=1
    
    result = [];
    k = 0
    while k < len(nums):
        result.append(mines.pop(math.floor((25-k)*nums[k])));
        k+=1
    
    return result;

  
def verify( serverSeed, clientSeed, nonce):
    

    
    hex = hexgen(serverSeed, clientSeed, nonce)
    #print(hex)


    i = 0
    digest = 0
    end = 0
    pow = 1
    index = [] 
    multier = 25   
    float = []


 
         
    while len(float) < 24: 
        while i < digest+4 and pow < 5:
            end += int(hex[i*2:i*2+2], 16) / math.pow(256, pow)            
            pow+=1
            i+=1
           
        float.append(end)
        #index.append(int((end * multier)))
        
        multier -= 1
        pow = 1
        digest+=4
        end = 0
    
    #print(float)
    #print(index)    
        
        
    
    result = nums_to_mine_array(float)
    #print(result)
    return result  
    
def hexgen(serverSeed, clientSeed, nonce): 
    hex = ''
    round = 0
    while round < 3:
        nonceSeed = '{}:{}:{}'.format(clientSeed, nonce, round)
        hex += hmac.new(bytes(serverSeed, 'utf-8'), bytes(nonceSeed, 'utf-8'), hashlib.sha256).hexdigest()
        round += 1
    return hex     



loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
loop.close()