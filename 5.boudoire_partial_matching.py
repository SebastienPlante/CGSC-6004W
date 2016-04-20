#################### Boudoire Partial Matching/Forgetting Model ###################

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    pass

#####
# Reginald is getting dressed in the morning
# Alas, he is slightly colourblind and has difficulties
# telling his shades of purple apart. If/when Reginald
# makes an error, he tries again. It will cycle through
# until he finds the correct tie.  However, sometimes
# when he tries again, he doesn't notice he got the wrong one.


class MyAgent(ACTR):
    focus=Buffer()

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=0.05,threshold=1)
    
    dm_n=DMNoise(DM,noise=0.6,baseNoise=0.0)         # turn on some noise to allow errors
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)   

    dm_spread=DMSpreading(DM,focus)                  
    dm_spread.strength=2                             
    dm_spread.weight[focus]=.5                    
                                                     

    partial=Partial(DM,strength=1.0,limit=-1.0)        # turn on partial matching
    partial.similarity('tie1','tie2',-0.5)
    partial.similarity('tie1','tie3',-0.2)
    partial.similarity('tie2','tie3',-0.7)

    def init():
        DM.add('tie:tie1 colour:aubergine')
        DM.add('tie:tie2 colour:mauve')
        DM.add('tie:tie3 colour:lilac') 
        focus.set('get_dressed')
        
    def bread_bottom(focus='get_dressed'):   
        print "Come now, Reginald!Get your day started!"
        focus.set('shirt')    

    def shirt(focus='shirt'):        
        print "I will choose a plum shirt today."  
        focus.set('collar')

    def collar(focus='collar'):
        print "I will button a white collar onto the shirt."
        focus.set('cuffs')

    def cuffs(focus='cuffs'):
        print "Choose white cuffs to match the collar."
        focus.set('decide_tie')
               
    def choose_tie(focus='decide_tie'):
        print "With a plum shirt I should wear an appropriate tie."
        print "Aubergine is the best colour"
        DM.request('tie:tie1 tie:?colour')
        focus.set('consider_tie')

    def fetch(focus='consider_tie', DMbuffer='tie:? colour:?colour'):
        print "I will wear this tie, it is"
        print colour
        focus.set('tie_it')

    def confused(focus='consider_tie', DMbuffer=None, DM='error:True'):
        print "I will wear this tie, it is"
        print "Oh dear... these colours are too similar. Try again."
        focus.set('decide_tie')
                                        
    def tie_it(focus='tie_it'):
        print "Tie a full windsor knot."
        print "I am now a snappy gentleman."
        focus.set('stop')

    def stop_production(focus='stop'):
        self.stop()

reg=MyAgent()                              # name the agent
boudoire=MyEnvironment()                     # name the environment
boudoire.agent=reg                           # put the agent in the environment
ccm.log_everything(boudoire)                 # print out what happens in the environment

boudoire.run()                               # run the environment
ccm.finished()                             # stop the environment
