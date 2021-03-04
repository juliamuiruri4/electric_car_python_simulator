#!/usr/bin/env python
# coding: utf-8

# In[1]:


def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)# parking process is suspended
        
        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration) # driving process is suspended


# In[2]:


import simpy
env = simpy.Environment()
env.process(car(env))


# In[3]:


env.run(until=20)


# In[3]:


#Lets assume that the car from our last example magically became an electric vehicle. Electric vehicles usually take a
#lot of time charging their batteries after a trip. They have to wait until their battery is charged before they can start
#driving again.

class Car(object): #Creating a class 'Car'. N/B: Car is the environment
    def __init__(self, env):
        self.env = env #declare car as an actual environment
       
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())
        
    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We yield the process that process() returns
            # to wait for it to finish
            
            yield self.env.process(self.charge(charge_duration))
        
            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)
    
    def charge(self, duration):
        yield self.env.timeout(duration)


# In[4]:


#Starting the simulation is straightforward again: 
#We create an environment, one (or more) cars and finally call run().
import simpy
env = simpy.Environment()
car = Car(env)
env.run(until=15)


# In[5]:


#Interrupting Another Process.
#Imagine, you don’t want to wait until your electric vehicle is fully charged but want to interrupt the 
#charging process and just start driving instead.
#SimPy allows you to interrupt a running process by calling its interrupt() method:

def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()


# In[6]:


#Executing Interrupting Another Process.

class Car(object): #Creating a class 'Car'
    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())
        
    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            
              # We may get interrupted while charging the battery
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                # When we received an interrupt, we stop charging and
                # switch to the "driving" state
                print('Was interrupted. Hope, the battery is full enough ...')
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)      
      
     
    def charge(self, duration):
        yield self.env.timeout(duration)


# In[7]:


#Running interruption Simulation
env = simpy.Environment()
car = Car(env)
env.process(driver(env, car))
env.run(until=15)


# In[ ]:




