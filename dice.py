import math
import hmac
import hashlib
import sys
import time
import os
import collections
import asyncio
import requests
import random
import string
#import aiohttp
#import numpy as np
from tkinter import *
import tkinter as Tkinter
import configparser as cp
from threading import Thread

hashlook = False



roll = 0
server_seed = ""
client_seed = ""
nonce = 0

bet_id = ""
activeClientSeed = ""
activeServerHash = ""
iid = ""
seed_pair = {}
switch = 0



edge = 0.99
nog = 0
target = 2
condition = "above"
condition1 = "below"
condition2 = "above"
current_code = ""
percent = []
percent_a = []
win_lose = {}
listed = {}
total_luck = {}
total_ch = {}
due = {}
between = 0
multiply = 1
profit_lost = 0
bet_win = 0
wager_10 = 0
seed = 0
wallet = 0
wallet_base = []
new = 0
vault_limit = 0.1
nog_streak = 100000
losestreak = 0
winstreak = 0
win_strk = []
lose_strk = []
loss_target = 0
wins_target = 0


win = 0
loss = 0
max_key = 0
luck = 0
luck_wins = 0
luck_lose = 0
wins = 0
lose = 0
per = 0
run = 0
target_set = False
reset = 0
totalwager = 0
total_prof = 0
nog_set = 0
nog_count = 0

saved_bal = 1
saved_profit = 0

balance = 10
base_bal = balance
bet = balance / 10000
base_bet = bet
profit = 0
wager = 0
vault = 0
prof = 0

base = 0.00005
percentage = 0
percent = 0
limit = 20000

multiplier = 1

lucky_below = [0] * 100
lucky = [0] * 100
roll_count = {}
result = {}

def randomSeed(length):
    seed = "".join(random.choices(
        string.ascii_lowercase + string.digits,
        k=length
    ))
    return seed
    
#TARGET PAYOUT CALCUALTION
def payout(condition, target, edge, maxroll):
    if condition == 'above':
        payout = float(((maxroll-edge)/(maxroll-target)))
        return payout
    else:
        payout = float(((maxroll-edge)/(target)));
        return payout

# CONDITION CHECK
def op(roll, condition, target):
    op = {
        'above': roll > target,
        'below': roll < target,
    }
    return op[condition];

# GENERATING RESULTS
def verify ( serverSeed, clientSeed, nonce ):
    round = 0
    nonceSeed = '{}:{}:{}'.format(clientSeed, nonce, round)
    hex = hmac.new(bytes(serverSeed, 'utf-8'), bytes(nonceSeed, 'utf-8'), hashlib.sha256).hexdigest()[0:8]
    i = 0
    end = 0
    while i < 4:
        end += int(hex[i*2:i*2+2], 16) / math.pow(256, i+1)
        i+=1
    end = math.floor(end * 10001) / 100
    return str(end)

#VERIFICATION OF WIN/LOSS
def verifier():
    global server_seed 
    global client_seed
    global nonce

    global roll_count
    global loss_target
    global wins_target
    global lucky_below
    global lucky
    global seed_pair
    global hashlook
    global nog_count
    global nog_set
    global totalwager
    global total_prof
    global lose_strk
    global win_strk
    global winstreak
    global losestreak
    global nog_streak
    global edge
    global nog
    global target
    global condition
    global condition1
    global condition2
    global current_code
    

    global saved_profit
    global saved_bal
    global result
    global multiplier
    global cond
    global wallet_base
    global new
    global wallet
    global wager_10
    global seed
    global multiply
    global percent
    global percent_a
    global listed
    global max_key
    global total_ch
    global total_luck
    global luck
    global luck_wins
    global luck_lose
    global switch
    global reset
    global between
    global due
    global win
    global loss
    global profit_lost
    global win_last
    global bet_win
    
    global wins
    global lose
    global per
    global run
    
    global base_bal
    global base_bet
    global bet 
    global balance
    global profit
    global wager
    global vault
    global prof
    
    global base
    global percentage
    global percent
    global limit

    while True:
        if run == 0:
            break
        #time.sleep(0.001)
        won = False
        lost = False
        nonce += 1
        nog += 1
        nog_count += 1
        roll = float(verify(server_seed, client_seed, nonce))
        multiplier = payout(condition, target, 1, 100)
        if(op(roll, condition, target)):
            #if bet > 0:
            wins_target += 1
            wins += 1
            luck_wins += 1
            win += 1
            won = True
            lost = False
            bet_round = float('{:.8f}'.format(bet))
            wager += bet_round
            profit += (bet_round*multiplier)-bet_round
            balance += (bet_round*multiplier)-bet_round
            per = float('{:.2f}'.format((wins) / (wins + lose) *100))
            percentage = float("{:.1f}".format((win) / (win + loss) * 100))
            #if not target == 2:
            print('bal {:.8f} profit {:.8f} +{:.8f} bet {:.8f} x{} roll {} "{}" {}'.format(balance, profit, (bet*multiplier)-bet, bet, float(format(multiplier, '.2f')), roll, condition, target)) 
            prof += (bet_round*multiplier)-bet_round
            

        else:
            loss_target += 1
            #if bet > 0:    
            lose += 1
            luck_lose += 1
            loss += 1
            won = False
            lost = True
            bet_round = float('{:.8f}'.format(bet))
            wager += bet_round
            profit -= bet_round
            balance -= bet_round
            multiplier = 0
            per = float('{:.2f}'.format((wins) / (wins + lose) *100))
            percentage = float("{:.1f}".format((win) / (win + loss) * 100))
            #if not target == 2:
            print('bal {:.8f} profit {:.8f} -{:.8f} bet {:.8f} x{} roll {} "{}" {}'.format(balance, profit, bet, bet, float(format(multiplier, '.2f')), roll, condition, target))
            prof -= bet_round
            
            #if not target == 2:
                #bet *= (1 / (payout(condition, target, 1, 100) - 1)) + 1
            #if bet > balance:
                #break

        
      



       
        # WINCHANCE AND LUCK FORMULAS
        
        #if hashlook == False:
        winchance = 0
        if condition == "above":
            winchance = float(100-target)

        else:
            winchance = float(target)
        #total_ch.append(winchance)
        try:
            total_ch[winchance] += 1
        except:
            total_ch[winchance] = 1
        total_key = sum([k*v for k,v in total_ch.items()])
        total_val = sum([v for k,v in total_ch.items()])
        total_chance = total_key / total_val
        
        # LUCK FACTOR  
        winrate = float('{:.4f}'.format((luck_wins) / (luck_wins + luck_lose) *100))
        luck_all = (winrate * (100 / winchance))
        #total.append(luck_all)
        try:
            total_luck[luck_all] += 1
        except:
            total_luck[luck_all] = 1
        luck_key = sum([k*v for k,v in total_luck.items()])
        luck_val = sum([v for k,v in total_luck.items()])
        luck = luck_key / luck_val
        winluck = luck / (100 / total_chance)
        current_code = "LUCK - {:.2f} %  | AVG CHANCE ~{:.2f}\nWIN % - {:.2f}\nROLLED - {} | TARGET - {} '{}'".format(luck, total_chance, winluck, roll, target, condition)
        luck_wins = 0
        luck_lose = 0
        
        #CURRENT LUCK RATE
        
        win_total = (wins / (wins + lose)) * 100
        lose_total = (lose / (wins + lose)) * 100
        
        luck_won = win_total * (100 / total_chance)
        luck_lost = lose_total * (100 / (100 - total_chance))
        
        #luck_index = [luck_below, luck_above].index(min([luck_below, luck_above]))
        #luck_current = [luck_won, luck_lost].index(max([luck_won, luck_lost]))
            
        reset = 0   

        #CURRENTLY RUNNING CODE:__________________________________________________________________
        
        
        #index = int(repr(round(int(roll), 2)).replace(".", ""))
        #if roll >= 1 and roll <= 99.99:
            #index = int(roll)
    
        if roll <= 99.99:
            index = int(roll)
            lucky_below[index] = lucky_below[index] + (int(roll)+1)
            lucky[index] = lucky_below[index] / (int(roll)+1)
            avg = sum(lucky) / len(lucky)
            if won:
                position = lucky.index(min(lucky, key=lambda x:abs(x-avg)))
                target = position + 1
                condition = "below"
        


        #________________________________________________  ______________________ 

            
        ###for idx, val in enumerate(lucky):
        ###min_val = [val for val in lucky if val.is_integer()]
        ### subtract from 4 ###############################
        ###min_val = max(lucky, key=lambda x:abs(x-2))
        ###index_val = lucky.index(min_val)
        ###min_val = max(values, key=lambda x:abs(x-luck))
        ###min_val = max(list_val) 
        ####median = sum(list_min) / len(list_min)
        ####min_val = min(list_min, key=lambda x:abs(x-median))

            
        #if round(profit, 8) < -0.005:
            #if condition == "below":
                #bet *= 1.005
                #bet = abs(profit) / (payout(condition, target, 1, 100))   
        #else:
            #bet = base_bet
            
 
        if bet > balance:
            break
            
       
            
        # check if below max luckrate changed to above max and set switch
      
 
 
              
        

            

 # GUI CODE   
    
class App(Tk):
    
    thread_started = 0
    cfg_folder = './config/'
    cfg_file = 'data.ini'
    cfg_path = '{}{}'.format(cfg_folder, cfg_file)
          
    def __init__(self, loop):
        global server_seed
        global client_seed
        global nonce
        super().__init__()

        
        
        
        self.title('Dice Client')
        #self.geometry('1000x500')
        self.apikey = StringVar(self)
        self.s_seed = StringVar(self)
        self.c_seed = StringVar(self)
        self.seed_nonce = IntVar(self)
        self.update_seednonce = 0
        self.ver_nonce = 1
        self.seed_nonce.set(nonce)
        #self.s_seed.set(server_seed)
        #self.c_seed.set(client_seed)    
        
        if not os.path.isdir(self.cfg_folder):
            os.mkdir(self.cfg_folder)
     
        if not os.path.isfile(self.cfg_path):
            self.saveini()
        else:
            self.loadini()

        



        
  
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
        self.verify_vault = StringVar(self)
        
        
        self.code_write = StringVar(self)

        

        self._frame_1 = Tkinter.Frame(self,)
        self._label_1 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0.00000000,textvariable=self.verify_balance)
        self._label_2 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0.00000000, textvariable=self.verify_profit)
        self._label_3 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0.00000000, textvariable=self.verify_vault)
        self._label_4 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0.00000000, textvariable=self.verify_wagered)
        self._label_5 = Tkinter.Label(self,font = "{MS Sans Serif} 15",foreground = "#000000",text = 0,textvariable=self.verify_wins)
        self._label_6 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0,textvariable=self.verify_loss)
        
        #self._label_27 = Tkinter.Label(self,font = "{MS Sans Serif} 15",foreground = "#000000",text = 0,textvariable=self.bel_wins)
        #self._label_28 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0,textvariable=self.bel_lose)
        
        
        self._label_13 = Tkinter.Label(self,font = "{MS Sans Serif} 15",foreground = "#000000",text = 0, textvariable=self.verify_winstreak)
        self._label_14 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = 0, textvariable=self.verify_losestreak)
        self._label_12 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = "-", textvariable=self.verify_nonce)
        self._label_15 = Tkinter.Label(self,font = "{MS Sans Serif} 15",text = "-", textvariable=self.verify_nog)
        self._entry_2 = Tkinter.Entry(self._frame_1,width = 0,)
        self._entry_3 = Tkinter.Entry(self._frame_1,width = 0,textvariable = self.seed_nonce)
        self._entry_4 = Tkinter.Entry(self._frame_1,width = 0, textvariable = self.c_seed)
        self._entry_5 = Tkinter.Entry(self._frame_1,justify = "center",width = 0,textvariable = self.s_seed)
        

        self._label_16 = Tkinter.Label(self,font = "Tahoma 20",text = "Balance:", )
        self._label_17 = Tkinter.Label(self,font = "Tahoma 20",text = "Profit:",)
        self._label_18 = Tkinter.Label(self,font = "Tahoma 20",text = "Vault:",)
        self._label_19 = Tkinter.Label(self,font = "Tahoma 20",text = "Wagered:",)
        self._label_20 = Tkinter.Label(self,font = "Tahoma 20",text = "Wins:", )
        self._label_21 = Tkinter.Label(self,font = "Tahoma 20",text = "Losses:", )
        self._label_24 = Tkinter.Label(self,font = "Tahoma 15",justify = "left", foreground = "blue", text = "",textvariable = self.code_write)
        
        #self._label_25 = Tkinter.Label(self,font = "Tahoma 20",text = "Below Wins:", )
        #self._label_26 = Tkinter.Label(self,font = "Tahoma 20",text = "Below Losses:", )
        
        self._label_22 = Tkinter.Label(self,font = "Tahoma 14",text = "Highest winstreak:",)
        self._label_23 = Tkinter.Label(self,font = "Tahoma 14",text = "Highest losestreak:",)
        self._label_10 = Tkinter.Label(self,font = "Tahoma 20",text = "Nonce:",)
        self._label_11 = Tkinter.Label(self,font = "Tahoma 20",text = "# Bets:",)
        self._label_7 = Tkinter.Label(self._frame_1,font = "{MS Sans Serif} 12",text = "Server seed",)
        self._label_8 = Tkinter.Label(self._frame_1,font = "{MS Sans Serif} 12",text = "Client seed",)
        self._label_9 = Tkinter.Label(self._frame_1,font = "{MS Sans Serif} 12",text = "Start nonce",)
        self._button_2 = Tkinter.Button(self._frame_1,font = "{MS Sans Serif} 12",text = "Stop", command=self.stop)
        self._button_1 = Tkinter.Button(self._frame_1,font = "{MS Sans Serif} 12",text = "Start", command=self.start)


        # widget commands
        # Geometry Management
        self._frame_1.grid(in_    = self,column = 1,row    = 1,columnspan = 5,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "news")
        self._label_1.grid(in_    = self,column = 3,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_2.grid(in_    = self,column = 3,row    = 4,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_3.grid(in_    = self,column = 3,row    = 5,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_4.grid(in_    = self,column = 3,row    = 6,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_5.grid(in_    = self,column = 5,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_6.grid(in_    = self,column = 5,row    = 4,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._entry_2.grid(in_    = self._frame_1,column = 4,row    = 2,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "ew")
        self._entry_3.grid(in_    = self._frame_1,column = 3,row    = 2,columnspan = 2,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "ew")
        self._entry_4.grid(in_    = self._frame_1,column = 2,row    = 2,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "ew")
        self._entry_5.grid(in_    = self._frame_1,column = 1,row    = 2,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "ew")
        self._button_2.grid(in_    = self._frame_1,column = 4,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "e")
        self._label_13.grid(in_    = self,column = 5,row    = 5,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_14.grid(in_    = self,column = 5,row    = 6,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_16.grid(in_    = self,column = 2,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_17.grid(in_    = self,column = 2,row    = 4,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_18.grid(in_    = self,column = 2,row    = 5,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_19.grid(in_    = self,column = 2,row    = 6,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_20.grid(in_    = self,column = 4,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_21.grid(in_    = self,column = 4,row    = 4,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_24.grid( in_    = self,column = 4,row    = 7,columnspan = 2,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 4,sticky = "nw")

        #self._label_25.grid(in_    = self,column = 4,row    = 7,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        #self._label_26.grid(in_    = self,column = 4,row    = 8,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        #self._label_27.grid(in_    = self,column = 5,row    = 7,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        #self._label_28.grid(in_    = self,column = 5,row    = 8,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        
        
        self._label_22.grid(in_    = self,column = 4,row    = 5,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_23.grid(in_    = self,column = 4,row    = 6,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_7.grid(in_    = self._frame_1,column = 1,row    = 1,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "")
        self._label_8.grid(in_    = self._frame_1,column = 2,row    = 1,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "")
        self._label_9.grid(in_    = self._frame_1,column = 3,row    = 1,columnspan = 2,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "")
        self._button_1.grid(in_    = self._frame_1,column = 3,row    = 3,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "")
        self._label_10.grid(in_    = self,column = 2,row    = 8,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_11.grid(in_    = self,column = 2,row    = 9,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_12.grid(in_    = self,column = 3,row    = 8,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        self._label_15.grid(in_    = self,column = 3,row    = 9,columnspan = 1,ipadx = 0,ipady = 0,padx = 0,pady = 0,rowspan = 1,sticky = "w" )
        
        self.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(2, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(3, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(4, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(5, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(6, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(7, weight = 0, minsize = 61, pad = 0)
        self.grid_rowconfigure(8, weight = 0, minsize = 43, pad = 0)
        self.grid_rowconfigure(9, weight = 0, minsize = 40, pad = 0)
        self.grid_rowconfigure(10, weight = 0, minsize = 40, pad = 0)
        self.grid_columnconfigure(1, weight = 0, minsize = 2, pad = 0)
        self.grid_columnconfigure(2, weight = 0, minsize = 100, pad = 0)
        self.grid_columnconfigure(3, weight = 0, minsize = 101, pad = 0)
        self.grid_columnconfigure(4, weight = 0, minsize = 221, pad = 0)
        self.grid_columnconfigure(5, weight = 0, minsize = 139, pad = 0)
        self._frame_1.grid_rowconfigure(1, weight = 0, minsize = 24, pad = 0)
        self._frame_1.grid_rowconfigure(2, weight = 0, minsize = 12, pad = 0)
        self._frame_1.grid_rowconfigure(3, weight = 0, minsize = 25, pad = 0)
        self._frame_1.grid_columnconfigure(1, weight = 0, minsize = 557, pad = 0)
        self._frame_1.grid_columnconfigure(2, weight = 0, minsize = 81, pad = 0)
        self._frame_1.grid_columnconfigure(3, weight = 0, minsize = 40, pad = 0)
        self._frame_1.grid_columnconfigure(4, weight = 0, minsize = 40, pad = 0)


        
        self.loop = loop
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.updater()))
    
    async def updater(self):
        while await asyncio.sleep(1/60, True):
            if self.update_seednonce == 1:
                self.update_seednonce = 0
                self.seed_nonce.set(nonce)
            self.verify_wagered.set("{0:.8f}".format(wager))
            self.verify_balance.set("{0:.8f}".format(balance))
            self.verify_profit.set("{0:.8f}".format(profit))
            self.verify_vault.set("{0:.8f}".format(vault))
            self.verify_wins.set(wins)
            self.code_write.set(current_code)
            self.verify_loss.set(lose)
            self.verify_nonce.set('-' if nonce == 0 else nonce)
            self.verify_nog.set('-' if nog == 0 else nog)            
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
        global server_seed
        global client_seed
        config = cp.ConfigParser()
        config.read(self.cfg_path)
        self.apikey.set(config['API']['APIKEY'])
        self.s_seed.set(config['API']['SERVER_SEED'])
        self.c_seed.set(config['API']['CLIENT_SEED'])
        server_seed = config['API']['SERVER_SEED']
        client_seed = config['API']['CLIENT_SEED']
        self.seed_nonce.set(config['API']['NONCE'])
        
        
        
    def start (self):
        global run
        global server_seed
        global client_seed
        global nonce
        run = 1
        server_seed = self.s_seed.get()
        client_seed = self.c_seed.get()
        print(server_seed)
        if self.thread_started == 0:
            nonce = self.seed_nonce.get()
            self.thread_started = 1
            self.thread = Thread(target = verifier)
            self.thread.daemon = True
            self.thread.start()


    def stop (self):
        global run
        self.update_seednonce = 1
        self.seed_nonce.set(nonce)
        run = 0  
        self.thread_started = 0

loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
loop.close()