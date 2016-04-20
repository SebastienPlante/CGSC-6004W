#################### boudoire production DM model ###################


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# create an environment

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent


class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    

## NOTE ##
#Though I do realize that scrubbing and shaving are far more complicated than this and this model as-is is
#perhaps not a proper implimentation of ACT-R planning, this model is just meant to practice the later model
#recalling, so I'm cool with it if you are.  Plus, this is just practice and learning at this point.

    
    def init():
        DM.add('cologne:Eau_de_Toilette')              # put a chunk into DM
        DM.add('cologne:Musc_Oil')
        focus.set('stubble')
        
    def chin_scratch(focus='stubble'):   
        print "I need to clean myself up."         
        focus.set('cleansing_scrub')

    def wash(focus='cleansing_scrub'):                          
        print "I have washed my face with hot, soapy water"     
        focus.set('hot_foam')                                   

    def foam(focus='hot_foam'):
        print "I have applied hot foam to my face"
        focus.set('get_razor')

    def shave(focus='get_razor'):
        print "I have scraped this unnaturally sharp piece of brittle steel across my skin"
        focus.set('cleanse')

    def cleanse(focus='cleanse'):
        print "I have rubbed stinging alcohol into my fresh microcuts"
        focus.set('smellies')

    def aftershave(focus='smellies'):
        print "Looking for nice smellies..."
        DM.request('cologne:?')                # retrieve a chunk from DM into the DM buffer
        focus.set('smellies_search')         # ? means that slot can match any content

    def dab(focus='smellies_search', DMbuffer='cologne:?cologne'):  # match to DMbuffer as well
        print "I believe I have..."                                 # put slot 2 value in ?condiment
        print cologne             
        print "I will dab this on my neck"
        focus.set('apply_bowtie')

    def finish(focus='apply_bowtie'):
        print "I am done with shaving"
        print "I will now switch to putting on my bowtie"
        focus.set('stop')   

    def stop_production(focus='stop'):
        self.stop()


reginald=MyAgent()                         # name the agent
boudoire=MyEnvironment()                   # name the environment
boudoire.agent=reginald                    # put the agent in the environment
ccm.log_everything(boudoire)               # print out what happens in the environment

boudoire.run()                             # run the environment
ccm.finished()                             # stop the environment
