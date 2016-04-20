#################### ham cheese production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Boudoire(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    bowtie=ccm.Model(isa='tie',location='on_hook')
    eaudetoilette=ccm.Model(isa='cologne',location='on_shelf')
    muscoil=ccm.Model(isa='cologne',location='on_shelf')
    razor=ccm.Model(isa='razor',location='on_shelf')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def do_shave(self):
        yield 90
        print "I am now clean shaven"
        self.parent.parent.razor.location='on_neck'        
    def tidy_shave(self):
        yield 1
        print "Put away the razor"
        self.parent.parent.razor.location='on_shelf'
    def do_bowtie(self):
        yield 20
        print "Tie a bowtie"
        self.parent.parent.bowtie.location='on_neck'
    def do_eau(self):     
        yield 2
        print "Dab eau de toilette"
        self.parent.parent.eaudetoilette.location='on_neck'
    def do_musc(self):     
        yield 2
        print "Dab musc oil"
        self.parent.parent.muscoil.location='on_neck'
        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('rough')

    def shave(focus='rough'):
        print "I'll just have a quick shave"
        motor.do_shave()
        focus.set('tidy')

    def tidy(focus='tidy', razor='location:on_neck'):
        print "I need to clean up now"
        motor.tidy_shave()
        focus.set('tie')

    def bowtie(focus='tie', bowtie='location:on_hook', razor='location:on_shelf'):
        print "I will put on a bowtie today"     
        focus.set('cologne')
        motor.do_bowtie()


    def eau(focus='cologne', bowtie='location:on_neck', eaudetoilette='location:on_shelf'):
        print "I will wear eau de toilette today"
        focus.set('stop')
        motor.do_eau()

    def musc(focus='cologne', bowtie='location:on_neck', muscoil='location:on_shelf'):
        print "I will wear musc today"
        focus.set('stop')
        motor.do_musc()

    def stop_production(focus='stop', muscoil='location:on_neck'):
        print "I am fancy and read to go out."
        self.stop()

    def stop_production(focus='stop', eaudetoilette='location:on_neck'):
        print "I am classy and read to go out."
        self.stop()


Reginald=MyAgent()
env=Boudoire()
env.agent=Reginald 
ccm.log_everything(env)

env.run()
ccm.finished()
