#!/usr/bin/python
# encoding: utf-8
import willie
import time
import datetime
import schedule
import os.path
import pickle

class botStatus:
    def __init__(self):
        self.active_list = {} 	# wer ist da
        self.week_list = {}		# soll
        self.working_minutes = {}	# ist
        self.pending_messages = {}  # nicht zugestellt
        self.overtime = {}          # aktuelle Überstunden


friends = {"name1":"greeting1", "name2":"greeting2"}
today = datetime.date
botswana = botStatus()

def check():
    for user in active_list.keys():
        willie.msg(user, "!!! Du wurdest automatisch ausgestempelt !!!")
        willie.msg(user, "Bitte trage deine Arbeitszeit für gestern nach.")
        willie.msg(user, "addtime <Stunden>:<Minuten>")
    active_list.clear()
    if(datetime.date.weekday == 0): 
        for user in botswana.working_minutes.keys():
            if (user in week_list):
                botswana.pending_messages[user].append("Wochenresumee zum Montagmorgen:")
                botswana.pending_messages[user].append("ist:   " + seconds2time(botswana.week_list[user]))
                botswana.pending_messages[user].append("soll:  " + seconds2time(botswana.working_hours[user]))
                delta = botswana.working_minutes[user] - int(botswana.week_list[user])
                
                if(delta > 0):
                    botswana.pending_messages[user].append("delta: " + seconds2time(delta) + " Stunden zu wenig")
                else:
                    botswana.pending_messages[user].append("delta: " + seconds2time(delta * -1) + "Plusstunden!")
            if(user not in overtime):
                overtime[user] = 0
            else:
                botswana.pending_messages[user].append("Gesamte Überstunden: " + str(botswana.overtime[user] + delta))
            botswana.overtime[user] += delta;	


def seconds2time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%dh %02dm" % (h, m)

# This method is only used for week-hours
def check4int(hours):
	try:
		i_hours = int(hours)
		return i_hours
	except ValueError:
		return -1

# This method is used to add time on the schedule
def check4time(tstring):
    ret = []
    try:
        pos = tstring.find(":")
    # Python has no switch/case. This is uuugly as hell :/
        if(pos == -1): # hours only
            hours = int(tstring)
            minutes = 0
        else:
            if (pos == 0): # minutes only
                hours = 0
                minutes = int(tstring[1:])
            else:
                hours = int(tstring[:pos])
                minutes = int(tstring[pos+1:])
        ret.append(hours)
        ret.append(minutes)
        print(ret)
        return ret
    except ValueError:
        return []
        

@willie.module.nickname_commands('addtime')
#TODO: Regex hinzufügen
#TODO: Minuten
def addtime(willie, trigger):
    sender_l = (str(trigger.nick)).lower()
    
    if(sender_l not in botswana.working_minutes):
        willie.msg(sender_l, "Sorry, members only!")
        return
    
    if(trigger.group(3) is None):
        willie.msg(sender_l, "addtime <Stunden>[:<Minuten>]")
        return
    time2add = check4time(trigger.group(3))
    if(len(time2add) < 2):
        willie.msg(sender_l, "Das mit dem Input üben wir aber nochmal!")
        return
    seconds = time2add[0] * 3600 + time2add[1] * 60
    botswana.working_minutes[sender_l] += seconds
    if(seconds > 0):
        willie.msg(sender_l, "Dein Zeitkonto wurde auf " + seconds2time(botswana.working_minutes[sender_l]) + " aufgestockt")
    else:
        willie.msg(sender_l, "Dein Zeitkonto wurde auf " + seconds2time(botswana.working_minutes[sender_l]) + " reduziert")
	
@willie.module.nickname_commands('wtime')
def wtime(willie, trigger):
    sender_l = (str(trigger.nick)).lower()
    if(trigger.group(3) is None):
        if(sender_l in botswana.week_list):
            willie.msg(sender_l, "Aktuell hast du bei mir " + str(botswana.week_list[sender_l] / 3600) + " Stunden vermerkt")
        else:
            willie.msg(sender_l, "Tut mir leid, kein Eintrag für dich vorhanden!")
        return
    ret = check4int(trigger.group(3))
    if(ret > 0):
        botswana.week_list[sender_l] = ret * 3600
        willie.msg(sender_l, "Du hast " + str(ret) + " Wochenstunden")
    else:
        willie.msg(sender_l, "Bitte gib ein x:{x∈ℕ} an!")

@willie.module.nickname_commands('moin', 'Moin', 'tach', 'hi', 'Tach', 'Hi', 'Hey')
def add(willie, trigger):
    sender = str(trigger.nick)
    sender_l = sender.lower()

    if(sender_l in botswana.active_list.keys()):
        willie.say("Kollege, du bist doch eingestempelt!")
        willie.say("Einmal ausstempeln, wenn du die Zeiten korrigieren willst")
        return

    if(sender_l in friends.keys()):
        willie.say(friends[sender_l])
    else:
        willie.say("Ohai thar, " + sender)

    if (sender_l not in botswana.week_list):
        willie.say(sender + " bitte verrate mir noch deine wochenarbeitszeit!")
        willie.say(sender + " wtime <Zeit in Stunden>")
    if (sender_l not in botswana.working_minutes):
        botswana.working_minutes[sender_l] = 0
    else:
        willie.msg(sender, "Deine bisherige Wochenarbeitszeit ist " + seconds2time(botswana.working_minutes[sender_l]))

# Sign the user in:
    botswana.active_list[sender_l] = time.time()
    print(sender + " logged on at " + str(botswana.active_list[sender_l]))

@willie.module.nickname_commands('bye', 'Bye', 'ciao', 'bin mal wech')
def remove(willie, trigger):

    sender = str(trigger.nick)
    print(sender + " said goodbye")
    sender_l = sender.lower()
    if(sender_l in botswanaactive_list.keys()):

        delta = time.time() - botswana.active_list[sender_l]
        delta_str = seconds2time(delta)
        willie.say("Ciao. " +  sender)
        if(sender_l not in botswana.working_minutes.keys()):
            botswana.working_minutes[sender_l] = delta
        if(sender_l not in botswana.pending_messages.keys()):
            botswana.pending_messages[sender_l] = []
        botswana.pending_messages[sender_l].append("Dir wurden " + seconds2time(delta) + " angerechnet!")
        if(delta > 23400):
            botswana.working_minutes[sender_l] -= 1800
            botswana.pending_messages[sender_l].append("Abzüglich 30 Minuten Pause")
        if(delta > 32400):
            botswana.working_minutes[sender_l] -= 2700
            botswana.pending_messages[sender_l].append("und nochmal 15 Minuten weil du so lange hier bist!")
        botswana.working_minutes[sender_l] =  botswana.working_minutes[sender_l] + delta
        if(sender_l in botswana.week_list):
            botswana.pending_messages[sender_l].append("Bleiben " + seconds2time(botswana.week_list[sender_l] - botswana.working_minutes[sender_l]))
        else:
            botswana.pending_messages[sender_l].append("Du hast noch keine Wochenstunden eingetragen!")
        del botswana.active_list[sender_l]
    else:
        willie.say("Hö? Wer? Du bist doch gar nicht eingestempelt!")

@willie.module.nickname_commands('was geht', 'status')
def status(willie, trigger):
    sender_l = str(trigger.nick).lower()
    if(sender_l in botswana.active_list):
        willie.msg(sender_l, "Du hast heute schon " + seconds2time(time.time() - botswana.active_list[sender_l]) + " gearbeitet!")
    else:
        willie.say("Members only!")

@willie.module.event('part', 'quit')
@willie.module.rule('.*')
def bye(willie, trigger):
    remove(willie, trigger)

@willie.module.event('join')
@willie.module.rule('.*')
def join(willie, trigger):
    add(willie, trigger)
    sender_l = (str(trigger.nick)).lower()
    if(sender_l in botswana.pending_messages.keys()):
        pms = botswana.pending_messages[sender_l]
        willie.msg(sender_l, "Du hast " + str(len(botswana.pending_messages[sender_l])) + " neue Nachrichten:")
        for message in pms:
            willie.msg(sender_l, message)
        botswana.pending_messages[sender_l] = []     # reset messages
    if(sender_l not in botswana.working_minutes):
        botswana.working_minutes[sender_l] = 0

@willie.module.nickname_commands('tell')
def addMessage(willie, trigger):
    sender_l = (str(trigger.nick)).lower()
    receiver_l = str(trigger.group(3)).lower()
    if(trigger.group(3) is None):
        willie.msg(sender_l, "tell <User> <Nachricht>")
        return
    
    if(receiver_l not in botswana.working_minutes):
        willie.msg(sender_l, "Kenn ich nicht, mach ich trotzdem!")
        botswana.pending_messages[receiver_l] = []
    
    botswana.pending_messages[receiver_l].append(sender_l + " lässt ausrichten: \n" + str(trigger.group(2)))
    
    


@willie.module.thread(True)
@willie.module.interval(3600)
def wipeWeek(willie):
    if(datetime.time.hour == 6):
        check()
    
def setup(willie):
        oldState = load(willie, None)
        botswana.active_list = {}
        botswana.week_list = oldState.week_list
        botswana.working_minutes = oldState.working_minutes
        botswana.pending_messages = oldState.pending_messages
        botswana.overtime = oldState.overtime

@willie.module.nickname_commands('.load')
def load(willie, trigger):
    homedir = os.path.join(os.path.expanduser('~'), '.willie')
    savedState = os.path.join(homedir, "uptime.sav")
    if(os.path.isfile(savedState)):
        # unpickle save file here
        print("Loading " + str(savedState))
        handle = open(savedState,'rb')
        saved = pickle.load(handle)
        # debug:
        print saved.week_list
    else:
        saved = botStatus()
    return saved

@willie.module.nickname_commands('.save')
def shutdown(willie, trigger):
    # save state to a pickle
    homedir = os.path.join(os.path.expanduser('~'), '.willie')
    savedState = os.path.join(homedir, "uptime.sav")
    willie.msg(str(trigger.nick), "saving status to.. " + str(savedState))
    handle = open(savedState,'wb')
    pickle.dump(botswana, handle)
    handle.close()

if __name__ == '__main__':
    print __doc__.strip()



