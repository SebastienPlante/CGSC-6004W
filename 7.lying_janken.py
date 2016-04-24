### Winning Liar's Janken / Paper-Rock-Scissors With Psycho-social Dimension ###

# This variant of Paper-Rock-Scissors ("janken" in Japanese, from whom Western culture
# learned the game) involves an additional stage; before throwing their play, the
# referee asks each player to announce what their play will be.  Player don't have
# to follow what they say, and are permitted to lie.
#
# For this simulation, in the first round, player A will always go first. After the
# first round, in the Winning version, the winner of the previous round will always
# announce their move first (in Losing Liar's Janken, the loser from the previous
# round will always announce their move first). In a normal, non-simulated game, the
# person to go first would be chosen by playing normal, silent janken.
#
# Normally, if there's a tie, the person who announced second in the tying round gets
# to go first. Here, to avoid having to deal with memory and record-keeping, in a tie
# the first liar is chosen at random.
#
# Partly because of time constraints, and partly because I don't want to make more work
# for myself than necessary, this program is designed to run through once, with A going
# first every time, and ending with the referee keeping score. I reckoned that's already
# about 10x more coding than anything I've done in class, and is complicated as balls,
# so that's enough for now.  I'll introduce multi-round score keeping later.
#
# This program is heavily based on Robert West's model of regular janken play.

import ccm
log=ccm.log()
from ccm.lib.actr import *

###########################################
### The Environment
###########################################

class MyEnvironment(ccm.Model):
    
    player_A=ccm.Model(signal='OK')
    hand_A=ccm.Model(move='none')
    score_A=ccm.Model(score=0)
    player_A_voice=ccm.Model(isa='voice',message='none')
    
    player_B=ccm.Model(signal='OK')
    hand_B=ccm.Model(move='none')
    score_B=ccm.Model(score=0)
    player_B_voice=ccm.Model(isa='voice',message='none')
    
    referee=ccm.Model(signal='A_first_lie')
    trial_count=ccm.Model(trial=0)

###########################################
### Motor Module
###########################################

class MotorModule(ccm.Model):

############### Agent A ###############

# Agent A's Words
    def A_say_paper(self):           
        print "'A will do paper'"
        self.parent.parent.player_A_voice.message='paper'
    def A_say_rock(self):           
        print "'A will do rock'"
        self.parent.parent.player_A_voice.message='rock'
    def A_say_scissors(self):           
        print "'A will do scissors'"
        self.parent.parent.player_A_voice.message='scissors'

# Agent A's Actions
    def A_paper(self):           
        print "A's hand = paper"
        self.parent.parent.hand_A.move='paper'
    def A_rock(self):           
        print "A's hand = rock"
        self.parent.parent.hand_A.move='rock'
    def A_scissors(self):           
        print "A's hand = scissors"
        self.parent.parent.hand_A.move='scissors'

# Agent A General Play
    def A_closed(self):           
        print "A's hand = blank"
        self.parent.parent.hand_A.move='closed'
    def A_OK(self):           
        print "A is ready"
        self.parent.parent.player_A.signal='OK'
    def A_spoken(self):
        print "A has announced his move"
        self.parent.parent.player_A.signal='spoken'
    def A_busy(self):
        print "A is doing something"
        self.parent.parent.player_A.signal='active'

############### Agent B ###############

# Agent B's Words
    def B_say_paper(self):           
        print "'B will do paper'"
        self.parent.parent.player_B_voice.message='paper'
    def B_say_rock(self):           
        print "'B will do rock'"
        self.parent.parent.player_B_voice.message='rock'
    def B_say_scissors(self):           
        print "'B will do scissors'"
        self.parent.parent.player_B_voice.message='scissors'

# Agent B's Actions
    def B_paper(self):           
        print "B's hand = paper"
        self.parent.parent.hand_B.move='paper'
    def B_rock(self):           
        print "B's hand = rock"
        self.parent.parent.hand_B.move='rock'
    def B_scissors(self):           
        print "B's hand = scissors"
        self.parent.parent.hand_B.move='scissors'

# Agent B General Play
    def B_closed(self):           
        print "B's hand = blank"
        self.parent.parent.hand_B.move='closed'
    def B_OK(self):           
        print "B is ready"
        self.parent.parent.player_B.signal='OK'
    def B_spoken(self):
        print "B has announced his move"
        self.parent.parent.player_B.signal='spoken'
    def B_busy(self):           
        print "B is doing something"
        self.parent.parent.player_B.signal='active'

############### The Referee ###############

# Liar's Gameplay

    def ref_A_first_lie(self):
        print "Referee tells A to announce first"
        self.parent.parent.referee.signal='A_first_lie'

    def ref_B_first_lie(self):
        print "Referee tells B to announce first"
        self.parent.parent.referee.signal='B_first_lie'        

    def ref_A_second_lie(self):
        print "Referee tells A to announce second"
        self.parent.parent.referee.signal='A_second_lie'

    def ref_B_second_lie(self):
        print "Referee tells B to announce second"
        self.parent.parent.referee.signal='B_second_lie'        

# Actual Gameplay

    def ref_go(self):           
        print "Referee says 'go'"
        self.parent.parent.referee.signal='go'
        
    def ref_wait(self):           
        print "The referee is waiting"
        self.parent.parent.referee.signal='wait'

    def ref_proceed(self):
        print "Let's play again"
        self.parent.parent.referee.signal='proceed'

# Rule set definitions

    def A_win(self):
        print "Score Update"
        self.parent.parent.referee.signal='A_wins'        
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        A=A+1
        C=C+1
        print "A;", A, "B;", B, "Round;", C
        self.parent.parent.score_A.score=A
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) # make string and store
        if C==10:
             f.write('%d,%d,%d\n'%(C,A,B)) # make string and store
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'
             
    def B_win(self):
        print "Score Update"
        self.parent.parent.referee.signal='B_wins'        
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        B=B+1
        C=C+1
        print "A;", A, "B;", B, "Round;", C
        self.parent.parent.score_B.score=B
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) 
        if C==10:
             f.write('%d,%d,%d\n'%(C,A,B)) 
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'
             
    def tie(self):
        print "Score Update"
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        C=C+1
        print "A;", A, "B;", B, "Round;", C
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) 
        if C==10:
             f.write('%d,%d,%d\n'%(C,A,B)) 
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'

    def terminate(self):
        print "Game Over"
        if C==10:
            focus.set('terminate')

###########################################
### Making Agents : The Referee
###########################################

class Ref(ACTR):
    production_time=0.01
    focus=Buffer()
    motor=MotorModule()

# Basic Gameplay - force A to go first

    def init():
        print "Version 1"
        focus.set('prime_game')

    def prime(focus='prime_game'):
        print "Start!"
        motor.ref_A_first_lie()
        focus.set('state:A_first_lie')

# In case of a tie, the first liar is chosen at random
# Normally in a tie the first liar loses their rank and the
# second liar goes first, but I don't feel like screwing around
# with the ref's memory system

    def proceed(focus='proceed game:?game'):
# the cut off for after having done the set number of rounds will go here
# some kind of "if C < 100 then continue; if C=100 then termminate"
        motor.ref_proceed()
        focus.set('game:?game')

    def Make_A_first(focus='state:tie',
                     player_B='signal:OK',
                     player_A='signal:OK'):
        print "Because of a tie, the referee chooses player A to go first"
        focus.set('state:A_first_lie')

    def Make_B_first(focus='state:tie',
                     player_B='signal:OK',
                     player_A='signal:OK'):
        print "Because of a tie, the referee chooses player B to go first"
        focus.set('state:B_first_lie')

# The Referee initiates the announcing

    def A_first_lie(focus='state:A_first_lie',
                 player_B='signal:OK',
                 player_A='signal:OK'):
        print "A will announce their move first"
        motor.ref_A_first_lie()
        focus.set('state:B_second_lie')
        
    def B_first_lie(focus='state:B_first_lie',
                 player_B='signal:OK',
                 player_A='signal:OK'):
        print "B will announce their move first"
        motor.ref_B_first_lie()
        focus.set('state:A_second_lie') 

    def A_second_lie(focus='state:A_second_lie',
                 player_B='signal:spoken',
                 player_A='signal:OK'):
        print "A will announce their move second"
        motor.ref_A_second_lie()
        focus.set('state:start_game')

    def B_second_lie(focus='state:B_second_lie',
                 player_B='signal:OK',
                 player_A='signal:spoken'):
        print "B will announce their move second"
        motor.ref_B_second_lie()
        focus.set('state:start_game')        

# The referee waits until A and B signal they are ready, then initiates the throw

    def start_game(focus='state:start_game',
           player_B='signal:spoken',
           player_A='signal:spoken'):
        motor.ref_go()
        focus.set('state:evaluate')

# while A and B are busy throwing their move, the ref is set to "wait"

# Game evaluations - ties    

    def evalPP(focus='state:evaluate',
               hand_B='move:paper', hand_A='move:paper',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:tie')
        print "It's a tie"
        motor.tie()

    def evalRR(focus='state:evaluate',
               hand_B='move:rock', hand_A='move:rock',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:tie')
        print "It's a tie"
        motor.tie()

    def evalSS(focus='state:evaluate',
               hand_B='move:scissors', hand_A='move:scissors',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:tie')
        print "It's a tie"
        motor.tie()

# Game evaluations - A wins

    def evalRP(focus='state:evaluate',
               hand_B='move:rock', hand_A='move:paper',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:A_first')
        print "A wins"
        motor.A_win()

    def evalSR(focus='state:evaluate',
               hand_B='move:scissors', hand_A='move:rock',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:A_first')
        print "A wins"
        motor.A_win()

    def evalPS(focus='state:evaluate',
               hand_B='move:paper', hand_A='move:scissors',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:A_first')
        print "A wins"
        motor.A_win()
        
# Game evaluations - B wins
        
    def evalPR(focus='state:evaluate',
               hand_B='move:paper', hand_A='move:rock',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:B_first')
        print "B wins"
        motor.B_win()
        
    def evalRS(focus='state:evaluate',
               hand_B='move:rock', hand_A='move:scissors',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:B_first')
        print "B wins"
        motor.B_win()

    def evalSP(focus='state:evaluate',
               hand_B='move:scissors', hand_A='move:paper',
               player_B='signal:OK', player_A='signal:OK'):
        focus.set('proceed state:B_first')
        print "B wins"
        motor.B_win()
        
###########################################
### Making Agents : Player A
###########################################
        
class Lag1player(ACTR):  ######## Player A lag1
    focus=Buffer()
    motor=MotorModule()

    DMbuffer=Buffer()                               # latency controls the relationship between activation and recall
    DM=Memory(DMbuffer,latency=1,threshold=-14)     # activation must be above threshold - can be set to none     
            
    dm_n=DMNoise(DM,noise=1.25,baseNoise=0.0)       # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=.5,limit=None)       # turn on for DM subsymbolic processing

    def init():
        print "A is present"    #testing line
        focus.set('primed')

    def primed(focus='primed'):
        focus.set('state:request dlag1:unknown dlag2:unknown swlag1:unknown swlag2:unknown')

    def proceed(focus='state:proceed dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1', referee='signal:proceed'):
        motor.A_closed()
        motor.A_OK()
        focus.set('state:request lag1:?lag0 lag2:?lag1 swlag1:?swlag0 swlag2:?swlag1')


###########################################
# Player A Lies First
###########################################

    def guess_request(focus='state:request dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2',
                      referee='signal:A_first_lie'):
        motor.A_busy()
        print "A is making a guess"
        DM.request('dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')
        focus.set('state:retrieve dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')

## Guess Based on Previous Two Moves
## dlag = DO-lag; the actions of the other player's previous move(s)
        
    def guess_retrieved(focus='state:retrieve dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2',
                        DMbuffer='dlag0:?dlag0'):
        focus.set('state:decide_move dlag0:?dlag0 dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')
        print "Matching guess retrieved"        
#        DMbuffer.clear()

## Random Guessing ###########
        
    def guess_paper(focus='state:retrieve dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2',
                    DMbuffer=None, DM='error:True'):
        print "No match; make a guess"        
        focus.set('state:decide_move dlag0:paper dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')

        
    def guess_rock(focus='state:retrieve dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2',
                   DMbuffer=None, DM='error:True'):
        print "No match; make a guess"        
        focus.set('state:decide_move dlag0:rock dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')

        
    def guess_scissors(focus='state:retrieve dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2',
                       DMbuffer=None, DM='error:True'):
        print "No match; make a guess"        
        focus.set('state:decide_move dlag0:scissors dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2')

# DO-lag2 is dropped here because the decision is already made, and it will
# just be overwritten later anyway

    def decide_move(focus='state:decide_move dlag0:?dlag0 dlag1:?dlag1 dlag2:?dlag2 swlag1:?swlag1 swlag2:?swlag2'):
        print "Player A will play;"
        print dlag0        
        focus.set('state:strategy_recall dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2')
        
## Choose a Strategy ############

# If someone announces "rock" and plays "rock", that's a "match", if they
# played "scissors" that's an "under" (i.e. their play loses to their
# announced move), if they played "paper" that's an "over" match (i.e. what
# they played wins over what they announced).

# Matching patterns are based on one's own winning and losing strategies.
# I have no idea how people actually play, so I'm making this up.
# Here I'm claiming that first people make the decision of what they're
# going to play, then follow it up by choosing the match strategy that
# tends to win.  It's equally possible that people will play by first
# announcing their move based on... unknown, then choosing a match pattern
# of their move relative to what they announced.  I dunno.

    def strategy_recall(focus='state:strategy_recall dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2'):
#        DM.request('swlag1:?swlag1 swlag2:?swlag2')
        print "Recalling past successful strategies"
        focus.set('state:strategy dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2')

    def strategy_found(focus='state:strategy dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2',
                        DMbuffer='swlag0:?swlag0'):
        print "Best strategy found"
        focus.set('state:decide_both dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1 swlag2:?swlag2')

# If no matching strategies, choose one at random
# swlag = self-win-lag; the matching patterns of past winning strategies

    def guess_match(focus='state:strategy dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2',
                       DMbuffer=None, DM='error:True'):
        print "No clear strategy; make a guess"        
        focus.set('state:decide_both dlag0:?dlag0 dlag1:?dlag1 swlag0:match swlag1:?swlag1 swlag2:?swlag2')

    def guess_over(focus='state:strategy dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2',
                       DMbuffer=None, DM='error:True'):
        print "No clear strategy; make a guess"        
        focus.set('state:decide_both dlag0:?dlag0 dlag1:?dlag1 swlag0:over swlag1:?swlag1 swlag2:?swlag2')

    def guess_under(focus='state:strategy dlag0:?dlag0 dlag1:?dlag1 swlag1:?swlag1 swlag2:?swlag2',
                       DMbuffer=None, DM='error:True'):
        print "No clear strategy; make a guess"        
        focus.set('state:decide_both dlag0:?dlag0 dlag1:?dlag1 swlag0:under swlag1:?swlag1 swlag2:?swlag2')

# Consolodate all strategies.  As with DO-lag2, the SELF-WIN-lag2 will be dropped

    def decide_both(focus='state:decide_both dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1 swlag2:?swlag2'):
        print "Player A will play;"
        print dlag0
        print "And player A's strategy will be;"
        print swlag0
        focus.set('state:analyze dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1')

## Analyze Strategy ##############

    def match_paper(focus='state:analyze dlag0:paper dlag1:?dlag1 swlag0:match swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:paper')

    def over_paper(focus='state:analyze dlag0:rock dlag1:?dlag1 swlag0:over swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:rock')

    def under_paper(focus='state:analyze dlag0:scissors dlag1:?dlag1 swlag0:under swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:scissors')

    def match_rock(focus='state:analyze dlag0:rock dlag1:?dlag1 swlag0:match swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:rock')

    def over_rock(focus='state:analyze dlag0:scissors dlag1:?dlag1 swlag0:over swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:scissors')

    def under_rock(focus='state:analyze dlag0:paper dlag1:?dlag1 swlag0:under swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:paper')

    def match_scissors(focus='state:analyze dlag0:scissors dlag1:?dlag1 swlag0:match swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:scissors')

    def over_scissors(focus='state:analyze dlag0:paper dlag1:?dlag1 swlag0:over swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:paper')

    def under_scissors(focus='state:analyze dlag0:rock dlag1:?dlag1 swlag0:under swlag1:?swlag1'):
        motor.A_closed()
        motor.A_say_paper()
        motor.A_spoken()
        focus.set('state:play decision:rock')

## make the action #########        

    def play_paper(focus='state:play decision:paper dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1', referee='signal:go'):
        motor.A_paper()
        motor.A_OK()
        focus.set('state:proceed dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1')

    def play_rock(focus='state:play decision:rock dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1', referee='signal:go'):
        motor.A_rock()
        motor.A_OK()
        focus.set('state:proceed dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1')

    def play_scissors(focus='state:play decision:scissors dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1', referee='signal:go'):
        motor.A_scissors()
        motor.A_OK()
        focus.set('state:proceed dlag0:?dlag0 dlag1:?dlag1 swlag0:?swlag0 swlag1:?swlag1')

## store result and start again ################



##
##
##
### Players only update their schema when they win
##    def win_state(focus='state:evaluate', referee='signal:A_wins'):
##        DM.request('swlag0:?swlag0 swlag1:?swlag1')
##        focus.set('state:learn')
##
##    def win_learn(focus='state:learn swlag0:?swlag0 swlag1:?swlag1'):
##        DM.add
##
##    
##        
##        
##    def lose_no_learn(focus='state:evaluate', referee='signal:B_wins'):
##        focus.set('state:hand dlag1:?dlag1')
##
##    def store_result(focus='state:hand dlag1:?dlag1',
##                     hand_B='move:!closed?dlag0'):
##        print "store result"
##        DM.add('lag0:?dlag0 dlag1:?dlag1')
##        print "shift do-lags"
##        focus.set('state:request dlag1:?dlag0')
##        motor.OK_A()

###########################################
### Making Agents : Player B
###########################################

# For now, Player B does all actions at random.  Eventually I hope to program both A
# and B - ideally with different strategies to see if one of them consistently wins
# more often - but for now I just want to get this off the ground.
        
class Lag2player(ACTR):  ######## Player A lag1
    focus=Buffer()
    motor=MotorModule()

    DMbuffer=Buffer()                               # latency controls the relationship between activation and recall
    DM=Memory(DMbuffer,latency=1,threshold=-14)     # activation must be above threshold - can be set to none     
            
    dm_n=DMNoise(DM,noise=1.25,baseNoise=0.0)       # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=.5,limit=None)       # turn on for DM subsymbolic processing

    def init():
        print "B is present"    #testing line
        focus.set('primed')

    def primed(focus='primed', referee='signal:A_first_lie'):     # Normally, this is where recall actions would happen, for now
        print "B is waiting"
        focus.set('state:request')  # it's a phantom step that does nothing

    def guess_request(focus='state:request', referee='signal:B_second_lie'):
        motor.B_busy()
        print "B is making a guess"
        focus.set('state:say_whatever')

## Random Guessing ###########

# Note: B is totally just doing whatever at random in this first version
# Also note that the "B has spoken" line isn't here - this is purely for ease of coding
        
    def guess_paper(focus='state:say_whatever'):
        motor.B_say_paper()
        print "Whatever, dude. I'll do paper."
        motor.B_spoken()
        focus.set('state:play')
        
    def guess_rock(focus='state:say_whatever'):
        motor.B_say_rock()
        print "Whatever, dude. I'll do rock."
        motor.B_spoken()
        focus.set('state:play')
        
    def guess_scissors(focus='state:say_whatever'):
        motor.B_say_scissors()
        print "Whatever, dude. I'll do scissors."
        motor.B_spoken()
        focus.set('state:play')

## Random Action ############

    def play_paper(focus='state:play', referee='signal:go'):
        motor.B_paper()
        motor.B_OK()
        focus.set('state:evaluate')

    def play_rock(focus='state:play', referee='signal:go'):
        motor.B_rock()
        motor.B_OK()
        focus.set('state:evaluate')

    def play_scissors(focus='state:play', referee='signal:go'):
        motor.B_scissors()
        motor.B_OK()
        focus.set('state:evaluate')


#for i in range(100):
#        f = open('newLg1t-14n125_Lg2t1n28.txt', 'a')
john=Ref()
tim=Lag1player()
tom=Lag2player()
octagon=MyEnvironment()
octagon.agent=john
octagon.agent=tim
octagon.agent=tom
ccm.log_everything(octagon) 
#        log=ccm.log(html=True)
octagon.run() 
ccm.finished()
#        f.close()


   
