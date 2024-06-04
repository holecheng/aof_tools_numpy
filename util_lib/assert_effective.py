import numpy as np


class ConfStat(object):
    def __init__(self):
        self.q = []

    def reset(self):
        self.q = []

    def append(self, v):
        self.q.append(v)

    def __str__(self):
        if len(self.q) == 0.:
            return '%8.3f +/- %7.3f, %6.0f' % (0, 0, 0)
        else:
            mean, var = np.mean(self.q), np.var(self.q)
            return '%8.3f +/- %7.3f, %6.0f' % (mean, 1.96 * np.sqrt(var / len(self.q)), len(self.q))

    def merge(self, other):
        self.q += other.q

    def get(self):
        return np.mean(self.q)

    def getn(self):
        return len(self.q)


class Player(object):
    def __init__(self):
        self.bet = 0.
        self.won = 0.
        self.action = 'u'
        self.hand = ''
        self.river_insure = -1
        self.turn_insure = -1
        self.ev = []
        self.nash_range = -1

    def __str__(self):
        ret = '%10s\tinitchip=%6.1f bet=%6.1f action=%s hand=%4s won=%6.1f reward=%6.1f ti=%4.1f ri=%4.1f ev=%s' % (
        self.pid, self.initchip, self.bet, self.action, self.hand, self.won, self.won - self.bet, self.turn_insure,
        self.river_insure, str(self.ev))
        if not self.nash_range is None:
            ret += ' nash_range=%.3f' % self.nash_range
        return ret


class RowHand(object):
    def __init__(self):
        self.players = []
        self.valid = False
        self.board = None
        self.ante = 0
        self.herolist = None

    def __str__(self):
        ret = 'handno=%s ante=%.1f hero=%d\n' % (self.handno, self.ante, self.hero)
        for i, p in enumerate(self.players):
            if self.hero == i:
                ret += '*%s\n' % p
            elif ((not self.herolist is None) and (p.pid in self.herolist)):
                ret += '+%s\n' % p
            else:
                ret += ' %s\n' % p
        ret += 'board=%s' % (self.board)
        return ret

    def convert(self, json):
        try:
            self.bb = float(json['blindLevel']['blinds'][1]) / 100
            self.ante = float(json['blindLevel']['blinds'][2]) / 100
            self.lvl = json['blindLevel']['blinds']
            self.lvl = [int(int(l) / 100) for l in self.lvl]
            self.lvl = '%s_%s_%s' % (self.lvl[0], self.lvl[1], self.lvl[2])
            self.handno = json['handNumber']
            if 'leagueName' in json:
                self.league = json['leagueName']
            else:
                #    print(json)
                #    haha
                self.league = 'none'
            self.tableid = self.handno.split('-')[0]

            if json['flop'] != '':
                if json['turn'] is None or json['river'] is None:
                    return False, 'board error'
                self.board = json['flop'] + json['turn'] + json['river']
                if len(self.board) != 10:
                    return False, 'board error'
            for i, p in enumerate(json['players']):
                player = Player()
                player.no = p['playerId'].strip()
                player.name = p['playerId']
                player.pid = p['pId']
                player.initchip = float(p['stack']) / 100
                if p['action'] == 'Push':
                    player.action = 'a'
                else:
                    player.action = 'f'
                player.hand = p['cards']
                player.forcebet = self.ante
                if p['isSb']:
                    player.forcebet += self.bb / 2
                if p['isBb']:
                    player.forcebet += self.bb
                if p['straddle'] == 1:
                    player.forcebet += self.bb * 2
                if player.forcebet > player.initchip:
                    player.forcebet = player.initchip
                #                if len(p['flopInsurance']) > 1:
                #                    print(len(p['flopInsurance']),p['flopInsurance'])
                #                    print(i,p)
                for insure in p['flopInsurance']:
                    if insure['defaultPot'] == False:
                        player.turn_insure = float(insure['betStacks'])

                #                    if player.turn_insure == -1:
                #                        player.turn_insure=float(insure['betStacks'])
                #                    else:
                #                        player.turn_insure+=float(insure['betStacks'])
                for insure in p['turnInsurance']:
                    if insure['defaultPot'] == False:
                        player.river_insure = float(insure['betStacks'])

                #                    if player.river_insure == -1:
                #                        player.river_insure=float(insure['betStacks'])
                #                    else:
                #                        player.river_insure+=float(insure['betStacks'])

                if player.action == 'a' and player.hand == '' and (not self.board is None):
                    return False, 'player %s not show hand' % player.pid
                player.ev.append(json['ev'][i])
                player.ev.append(json['outcome'][i])
                if 'nash_range' in json:
                    player.nash_range = json['nash_range'][i]

                self.players.append(player)

            if len(self.players) == 0:
                return False, 'no player'

            npush = 0
            for p in self.players:
                if p.action == 'a':
                    npush += 1
            if not self.board is None and npush <= 1:
                return False, 'too few push player'

            self.hero = int(json['heroIndex'])
            self.winners = json['winners']
            return True, ''
        except Exception as err:
            return False, 'except error %s' % (str(err))


def find_hero(hands, blacklist=[]):
    allplayer = {}  # 所有玩家对应打的局id playerId=>{[handNumber]:1}
    heros = {}  # hero玩家[playerId]=>{[handNumber]:1}
    hero_name = {}
    for hand in hands:
        for player in hand.players:
            u = allplayer.get(player.pid, {})
            u[hand.handno] = 1
            allplayer[player.pid] = u

        if hand.hero == -1:
            continue
        hid = hand.players[hand.hero].pid
        hero_name[hid] = hand.players[hand.hero].name
        u = heros.get(hid, {})
        u[hand.handno] = 1
        heros[hid] = u

    herolist = []
    heroid = list(heros.keys())
    heroid.sort()
    for hid in heroid:
        print(hid, hero_name[hid].replace('\n', '').replace('\r', ''),
              '%5d/%5d' % (len(heros[hid]), len(allplayer[hid])))
        if float(len(heros[hid])) / len(allplayer[hid]) > 0.8:
            herolist.append(hid)
        else:
            print('!!!!')
    return herolist

