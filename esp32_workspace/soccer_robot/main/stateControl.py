import math
import GoToGoal
import speedEstimator

class Inputs():
    ''' State machine inputs '''

    x = 0              # x-position of the robot
    y = 0              # y-position of the robot
    theta = 0          # robot orientation
    dt = 0             # time delta between the last execution (used by the PID)
    radius=0
    L = 0              # distance between the wheels
    array_of_goals=0

class Outputs():
    ''' State machine outputs '''

    left_motor = 0     # left motor output (0..1)
    right_motor = 0    # right motor ouput (0..1)
    
class State():
    ''' When creating a new state, extend this class '''

    def run(self, input, output):
        pass
    
    def entry(self, input, output):
        pass
    
    def exit(self, input, output):
        pass

######################################
# States
######################################

class InitSt(State):
    name = "Init"

    def __init__(self):
        pass
        
    def run(self, input, output):
        return GoToGoalSt.name
    
class GoToGoalSt(State):
    '''
        Go to Goal State - Robot go to a specific goal autonomously. The goal change
        every state entry.
    '''
    name = "GoToGoal"
    next_goal = 0
    shoot = -1
    
    def entry(self, input, output):
        # Set goal and next goal (in the next entry)
        array_of_goals = input.array_of_goals
        print(array_of_goals)
        self.goal = array_of_goals[GoToGoalSt.next_goal]
        if(self.goal==0):
            GoToGoalSt.shoot = GoToGoalSt.shoot+1
        GoToGoalSt.next_goal =(GoToGoalSt.next_goal+1)%len(array_of_goals)
        
            
        print("GoToGoal state", self.goal, GoToGoalSt.next_goal)
        
        # Initiate rate limit variable (assume that the robot is always stopped when
        # entering autonomous mode)
        self.leftPrevCmd = 0
        self.rightPrevCmd = 0
        
        # Create an instance of the PID controller
        self.controller = GoToGoal.GoToGoal()
        
    def limit(self, value, downLimit, upLimit):
        return upLimit if value >= upLimit else downLimit if value <= downLimit else value

    def rateLimit(self, value, ctrlVar, upLimit, downLimit):
        ctrlVar = self.limit(value, (downLimit + ctrlVar),(upLimit + ctrlVar))
        return ctrlVar
    
    def run(self, input, output):
        next_state = GoToGoalSt.name
        
        # Run controller
        w = self.controller.step(self.goal[0], self.goal[1], input.x, input.y, input.theta, input.dt)
        
        # Estimate the motor outpus with fixed speed of 50
        left, right = speedEstimator.uni_to_diff(5, w, input.radius,input.radius,input.L)
        
        # Apply rate limits to the speed and make sure it is between 0 and 1
        print('Motor commands from PID: left, right', left, right)

        if left > right:
            left2 = left/left
            right2 = right/left
        else:
            left2 = left/right
            right2 = right/right
        
        print('left 2, right 2', left2, right2)
        
        if(GoToGoalSt.shoot==1):
            left3 = self.rateLimit(left2, self.leftPrevCmd, 0.2, -0.2)
            right3 = self.rateLimit(right2, self.rightPrevCmd, 0.2, -0.2)
            left3 = left3 if left3 >=0.1 else 0.1
            right3 = right3 if right3 >= 0.1 else 0.1
            
            
            self.leftPrevCmd = left3
            self.rightPrevCmd = right3
            print("left3, right 3", left3, right3)
            output_left = left3*100
            output_right = right3*100
            
            # Make sure ouputs are not negative (robot can not reverse yet)
            left2 = left2 if left2 >= 0 else 0
            right2 = right2 if right2 >=0 else 0
            output.left_motor = output_left
            output.right_motor = output_right
            print('GoToGoal outputs:', output.left_motor, output.right_motor)
        else:
            left3 = self.rateLimit(left2, self.leftPrevCmd, 0.2, -0.2)
            right3 = self.rateLimit(right2, self.rightPrevCmd, 0.2, -0.2)
            left3 = left3 if left3 >=0.1 else 0.1
            right3 = right3 if right3 >= 0.1 else 0.1
            
            
            self.leftPrevCmd = left3
            self.rightPrevCmd = right3
            print("left3, right 3", left3, right3)
            output_left = left3*30
            output_right = right3*30
            
            # Make sure ouputs are not negative (robot can not reverse yet)
            left2 = left2 if left2 >= 0 else 0
            right2 = right2 if right2 >=0 else 0
            output.left_motor = output_left
            output.right_motor = output_right
            print('GoToGoal outputs:', output.left_motor, output.right_motor)
        
        # Check if it is in the goal. If yes, change state
        if (abs(input.x - self.goal[0]) < 3 and
            abs(input.y - self.goal[1]) < 3):
            next_state = AtTheGoalSt.name
            
    
        
        return next_state
    
class AtTheGoalSt(State):
    '''
        At the Goal state
    '''
    name = "AtTheGoal"
    
    def entry(self, input, output):
        print("AtTheGoal state")
        output.left_motor = 0
        output.right_motor = 0
    
    def run(self, input, output):
        next_state = GoToGoalSt.name
        
        output.left_motor = 0
        output.right_motor = 0
        
        return  next_state

        
    
class stateControl():
    '''
        Main class to constrol the state
    '''
    def __init__(self):
        self.states = {
        InitSt.name: InitSt(),
        GoToGoalSt.name: GoToGoalSt(),
        AtTheGoalSt.name: AtTheGoalSt()}
        
        self.input = Inputs()
        self.output = Outputs()
        self.currentState = InitSt.name
        self.states[self.currentState].entry(self.input, self.output)
        
    def step(self):
        next_state = self.states[self.currentState].run(self.input, self.output)
        
        if (next_state != self.currentState):
            self.states[self.currentState].exit(self.input, self.output)
            self.currentState = next_state
            self.states[self.currentState].entry(self.input, self.output)