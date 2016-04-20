##################### Boudoire SOS Checking Model #####################

# In this model, our agent Reginald is in a hurry and looking for cufflinks
# to wear with his fancy shirt.  He randomly grabs one of three shapes of
# cufflink, then looks for a match among the remaining five.

import ccm  
log=ccm.log(html=True)  

from ccm.lib.actr import *  

class Accessory_drawer(ccm.Model):
  diamond1=ccm.Model(isa='cufflink',location='in_drawer',feature1='diamond',salience=0.5)
  diamond2=ccm.Model(isa='cufflink',location='in_drawer',feature1='diamond',salience=0.5)
  circle1=ccm.Model(isa='cufflink',location='in_drawer',feature1='circle',salience=0.5)
  circle2=ccm.Model(isa='cufflink',location='in_drawer',feature1='circle',salience=0.5)  
  square1=ccm.Model(isa='cufflink',location='in_drawer',feature1='square',salience=0.5)
  square2=ccm.Model(isa='cufflink',location='in_drawer',feature1='square',salience=0.5)  

class MotorModule(ccm.Model):
  def hold_square(self):
    print "Take out the square cufflink"
    self.parent.parent.square1.location='hand'

  def hold_circle(self):
    print "Take out the circular cufflink"
    self.parent.parent.square1.location='hand'

  def hold_diamond(self):
    print "Take out the diamond cufflink"
    self.parent.parent.square1.location='hand'    

class MyAgent(ACTR):  
  focus_buffer=Buffer() 
  visual_buffer=Buffer() 
  vision_module=SOSVision(visual_buffer,delay=0)
  DMbuffer=Buffer()
  DM=Memory(DMbuffer)
  motor=MotorModule()
   
 ################ procedural production system ###################### 
   
  def init(): 
    focus_buffer.set('choose') 

  def choose(focus_buffer='choose'):
    print "I'm in a hurry, I don't care which cufflinks I wear."
    focus_buffer.set('grab')

# The agent randomly grabs one of the six cufflinks
  def grab_square(focus_buffer='grab'):
    print "Ok, I'll wear the square ones."
    DM.add('feature1:square')
    motor.hold_square()
    focus_buffer.set('search')

  def grab_circle(focus_buffer='grab'):
    print "Ok, I'll wear the circular ones."
    DM.add('feature1:circle')
    motor.hold_circle()
    focus_buffer.set('search')

  def grab_diamond(focus_buffer='grab'):
    print "Ok, I'll wear the diamond-shaped ones."
    DM.add('feature1:diamond')
    motor.hold_diamond()
    focus_buffer.set('search')    

# The agent takes note of what he's matching

  def search(focus_buffer='search'):
    DM.request('feature1:?')
    focus_buffer.set('look')

# The agent starts looking for the matching one of the remaining five
  def find(focus_buffer='look'):
    vision_module.request('isa:cufflink location:in_drawer') 
    focus_buffer.set('find_cufflink') 
    print "I am looking for the matching cufflink" 
 
  def found(focus_buffer='find_cufflink',visual_buffer='isa:cufflink location:in_drawer feature1:?feature1'): 
    print "I found a cufflink. It is a"
    print feature1
    focus_buffer.set('check ?feature1')
    visual_buffer.clear

# The cufflink they grabbed either matches or does not     
  def square_yes(focus_buffer='check square'):    
    print "I found a match."
    motor.hold_square()
    focus_buffer.set('button') 
    visual_buffer.clear 

  def square_no(focus_buffer='check square', DMbuffer='feature1:!square'):
    print "This isn't a match"
    focus_buffer.set('search')
    visual_buffer.clear

  def circle_yes(focus_buffer='check circle', DMbuffer='feature1:circle'):    
    print "I found a match."
    motor.hold_circle()    
    focus_buffer.set('button')
    visual_buffer.clear 

  def circle_no(focus_buffer='check circle', DMbuffer='feature1:!circle'):
    print "This isn't a match"
    focus_buffer.set('search')
    visual_buffer.clear 

  def diam_yes(focus_buffer='check diamond', DMbuffer='feature1:diamond'):    
    print "I found a match."
    motor.hold_diamond()
    focus_buffer.set('button')
    visual_buffer.clear     

  def diam_no(focus_buffer='check diamond', DMbuffer='feature1:!diamond'):
    print "This isn't a match"
    focus_buffer.set('search')
    visual_buffer.clear 

  def not_found(focus_buffer='check ?feature1',visual_buffer=None):
    print "Where is a cufflink?"
    focus_buffer.set('search')
    visual_buffer.clear
 
  def stop(focus_buffer='button'):
    print "I will button up my cuffs and looks snazzy now."
    focus_buffer.set('stop')
    
Reginald=MyAgent() 
env=Accessory_drawer() 
env.agent=Reginald  
ccm.log_everything(env) 
 
env.run() 
ccm.finished() 
