################ boudoire production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):       
    scissors=ccm.Model(isa='scissors',location='on_counter')
    comb=ccm.Model(isa='comb',location='on_counter')
    clippers=ccm.Model(isa='clippers',location='on_counter')
    razor=ccm.Model(isa='razor',location='on_counter')
# Because one of the agents' locations is a part of the environment...
    Reginald=ccm.Model(isa='Reginald')

    Reg_voice=ccm.Model(isa='voice')    
    Bea_voice=ccm.Model(isa='voice')

class MotorModule(ccm.Model):
    def sit(self):
        print "I will sit in the barber's chair"
        self.parent.parent.location='in_chair'
# Actions of haircut
    def do_shave(self):
        print "A close shave"
        self.parent.parent.razor.location='on_neck'
    def do_clean(self):
        print "A natural hairline"
        self.parent.parent.razor.location='on_nape'
    def do_comb(self):
        print "Comb the hair until arranged"
        self.parent.parent.comb.location='on_hair_top'
    def do_trim(self):
        print "Trim the tips to the desired length"
        self.parent.parent.scissors.location='on_hair_top'
    def do_sides(self):
        print "Trim the sides to the desired length"
        self.parent.parent.clippers.location='on_hair_sides'
    def do_back(self):
        print "Trim the back to the desired length"
        self.parent.parent.clippers.location='on_hair_back'
    def do_crown(self):
        print "Trim the crown to the desired length"
        self.parent.parent.scissors.location='on_hair_top'
    def do_fade(self):
        print "Fade the sides into the top and crown"
        self.parent.parent.scissors.location='on_hair_sides'
# Resetting the environment for next step
    def arrange_scissors(self):
        print "Put the scissors in the Barbasol"
        self.parent.parent.scissors.location='on_counter'
    def arrange_clippers(self):
        print "Put the clippers on the hook"
        self.parent.parent.clippers.location='on_counter'
    def arrange_comb(self):
        print "Put the comb in the Barbasol"
        self.parent.parent.comb.location='on_counter'
    def arrange_razor(self):
        print "Wipe the razor and place it on the counter"
        self.parent.parent.razor.location='on_counter'

# Speaking
    def Reg_answer(self, message):       # create a sound object
        yield 2
        print "Reginald is speaking"
        self.parent.parent.Reg_voice.message='message'

    def Bea_ask(self, message):
        yield 2
        print "Beasly is asking"
        self.parent.parent.Bea_voice.message='message'

    def Bea_speak(self, message):
        yield 2
        print "Beasly is speaking"
        self.parent.parent.Bea_voice.message='message'

# Agent = Reginald        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()
  

# Note re: this haircut; the lengths are set to always be:
#   Top > Crown > Back >= Sides
# Therefore, the minimal length, assuming the sides will never be shaved, are;
#   4 > 3 > {2,1} >= 1
# I had originally planned on throwing in a random number thing to randomly
# generate hairdos, but I'm not strong with the python.  So I figured I'd screw
# that noise until later when I'm better.

    def init():
        focus.set('sit_in_chair')

    def sit_in_chair(focus='sit_in_chair'):
        motor.sit()
        focus.set('wait')
        print "aa'

    def want_shave(focus='wait', Bea_voice='message:req_shave'):
        motor.Reg_answer(message='no_shave')
        print "wants a shave"
        focus.set('wait')

    def want_shave(focus='wait', Bea_voice='message:req_shave'):
        motor.Reg_answer(message='shave')
        print "does not want a shave"
        focus.set('wait')

    def want_top(focus='req_top'):
        motor.Reg_answer()
        print "The top will be..."
        print 6
        focus.set('ask_back')

    def want_back(focus='req_back'):
        motor.Reg_answer()
        print "The back will be..."
        print 3
        focus.set('ask_sides')

    def want_sides(focus='req_sides'):
        motor.Reg_answer()
        print "The sides will be..."
        print 2
        focus.set('ask_fade')

    def want_fade(focus='req_fade'):
        motor.Reg_answer()
        print "Thank-you;"
        print "Yes"
        focus.set('start_cut')

    def complete(focus='complete'):
        motor.Reg_answer()
        print "Thank-you, Beasly"
        focus.set('end')

class MyAgent2(ACTR):    
    focus=Buffer()
    motor=MotorModule()


 # Beasly is a barber, and as he asks questions the answers will be integrated into
 # declarative memory.  Unfortunately, we haven't learned how to learn things from
 # the environment yet. So when Reginald answers, I'll just take it as read for the
 # moment that Beasly learned what the lengths are and will remember them later.

    def inti():
        focus.set('in_shop')

    def req_shave(focus='in_shop', Reginald='location:in_chair'):
        motor.Bea_ask(message='req_shave') 
        print "Do you want a shave, first?"
        focus.set('req_shave')

    def do_shave(focus='do_shave'):
        motor.Bea_speak()
        print "I will shave you, now"
        motor.do_shave()
        focus.set('ask_top')

    def ask_top(focus='ask_top'):
        motor.Bea_ask()
        print "How long do you want the top?"
        focus.set('req_top')

    def ask_back(focus='ask_back'):
        motor.Bea_ask()
        print "How long do you want the back?"
        focus.set('req_back')

    def ask_sides(focus='ask_sides'):
        motor.Bea_ask()
        print "Do you want the sides and back the same?"
        focus.set('req_sides')
    
    def ask_fade(focus='ask_fade'):
        motor.Bea_ask()
        print "Should I fade it, or keep a line?"
        focus.set('req_fade')

    def start_cut(focus='start_cut'):
        motor.do_comb()
        print "First I tidy"
        motor.arrange_comb()
        focus.set('start_clippers')

    def start_clippers(focus='start_clippers'):
        motor.do_back()
        print "Start at the bottom center"
        focus.set('continue_clippers')

    def continue_clippers(focus='continue_clippers'):
        motor.do_sides()
        print "Work from the centre outwards"
        motor.arrange_clippers()
        focus.set('front_backward')

    def front_backward(focus='front_backward'):
        motor.do_trim()
        print "Cut the length of the fringe and match backwards"
        focus.set('back_forward')

# Nobody actually tells their barber how to do their crown - or it's rare, anyway.
# The barber has to figure it out from what you ask of the top and sides.
# The step of calculating the appropriate length will go here, once I know how.

    def back_forward(focus='back_forward'):
        motor.do_crown()
        print "Match the crown to the back and top, then match forward"
        focus.set('dofade')

# Once I figure out how to take input from the environment into an agent's DM,
# where an agent can learn and recall later, I'll code two separate steps; one
# for "do fade", and one for "skip fade", depending on what Reginald wants.

    def do_fade(focus='dofade'):
        motor.do_fade()
        print "Blend the sides into the top"
        focus.set('spot_check')

    def spot_check(focus='spot_check'):
        print "I will clean up any stray hairs"
        motor.do_trim()
        motor.do_crown()
        motor.do_fade()
        motor.arrange_scissors()
        motor.do_sides()
        motor.do_back()
        motor.arrange_clippers()
        focus.set('finishing_touch')
# I know that normally, these would all be separate steps, but I don't yet know how
# to do "do it as needed".

    def finishing_touch(focus='finishing_touch'):
        motor.do_clean()
        motor.arrange_razor()
        focus.set('stylehair')

    def stylehair(focus='stylehair'):
        print "Arrange the newly coiffed hair into a style"
        motor.do_comb()
        motor.arrange_comb()
        focus.set('done')

    def done(focus='done'):
        motor.Bea_speak()
        print "All done, sir"
        focus.set('complete')

    def stop_production(focus='end'):
        self.stop()
       

Reginald=MyAgent()
Beasly=MyAgent2()
barbershop=MyEnvironment()
barbershop.agent=Reginald
barbershop.agent=Beasly

ccm.log_everything(barbershop)

barbershop.run()
ccm.finished()
