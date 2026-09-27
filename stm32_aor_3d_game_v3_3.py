#!/usr/bin/env python3
"""STM32-AOR 3D Game v3
Pygame + PyOpenGL prototype.

Install: pip install pygame PyOpenGL numpy
Run: python3 stm32_aor_3d_game_v3.py

Controls:
 W/S speed, A/D steering, SPACE brake, C camera, H HUD, R restart, ESC quit.
During challenges type the answer and press ENTER.
"""
import math, random, time, sys
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE
from OpenGL.GL import *
from OpenGL.GLU import *

W,H=1280,720
R=0.035
L=0.141
VMAX=0.65
OMAX=2.8
WORLD_X,WORLD_Z=22.0,70.0

class Romi:
    def __init__(self): self.reset()
    def reset(self):
        self.x,self.z,self.theta=0.0,-30.0,0.0
        self.v,self.omega=0.0,0.0
        self.omega_l,self.omega_r=0.0,0.0
        self.steering_command=0.0
        self.wheel_l=self.wheel_r=0.0
        self.distance=0.0
    def update(self,throttle,steer,dt):
        self.steering_command=steer
        tv=throttle*VMAX; to=steer*OMAX
        a=min(1,6*dt); b=min(1,8*dt)
        self.v += (tv-self.v)*a
        self.omega += (to-self.omega)*b
        self.omega_r=(self.v+L*self.omega/2)/R
        self.omega_l=(self.v-L*self.omega/2)/R
        self.x += self.v*math.sin(self.theta)*dt
        self.z += self.v*math.cos(self.theta)*dt
        self.theta += self.omega*dt
        self.wheel_l += self.omega_l*dt
        self.wheel_r += self.omega_r*dt
        self.distance += abs(self.v)*dt
        self.x=max(-WORLD_X+1,min(WORLD_X-1,self.x))

class Obj:
    def __init__(self,x,z,kind='obstacle',flash=False):
        self.x,self.z,self.kind,self.flash=x,z,kind,flash
        self.active=True; self.passed=False; self.phase=random.random()*6.28

QUESTIONS=[
("Which sensors measure dL, dF and dR?",["VL53L0X","Encoders","IMU","GPS"],0,"The three VL53L0X ToF sensors provide the left, front and right distances."),
("What is the STM32-AOR MLP architecture?",["3-8-16-2","3-16-3","8-16-2","3-4-4-1"],0,"The network has 3 inputs, hidden layers of 8 and 16 neurons, and 2 outputs."),
("What are the MLP outputs?",["v_d and omega_d","dL and dR","PWM_L and PWM_R","x and y"],0,"The network produces desired linear and angular velocity."),
("Which task provides the fast safety layer?",["SafetyTask","AITask","SensorTask","RenderTask"],0,"SafetyTask independently checks dangerous conditions and can override commands."),
("What should happen when dF is below d_stop?",["Stop or constrain the command","Increase speed","Ignore dF","Disable sensors"],0,"The safety logic can force or constrain the drive command when an obstacle is too close."),
("Why use INT8 inference on STM32?",["Lower memory/compute cost","It removes sensors","It always increases model size","It removes safety logic"],0,"Quantization makes embedded inference smaller and computationally efficient."),
]
EXPL=[
("Explain why differential-drive turning changes the two wheel speeds.",["differential","wheel","left","right","omega"]),
("Explain why SafetyTask is separate from the neural network.",["safety","override","sensor","danger","independent"]),
("Explain what dL, dF and dR represent.",["left","front","right","distance"]),
]

class MotorSound:
    def __init__(self):
        self.ok=False
        try:
            if not pygame.mixer.get_init(): pygame.mixer.init(44100,-16,2,512)
            self.chL=pygame.mixer.Channel(4); self.chR=pygame.mixer.Channel(5)
            self.sL=self.make(145); self.sR=self.make(158)
            self.chL.play(self.sL,-1); self.chR.play(self.sR,-1)
            self.chL.set_volume(0,0); self.chR.set_volume(0,0); self.ok=True
        except Exception: pass
    def make(self,f):
        import array
        n=44100; buf=array.array('h')
        for i in range(n):
            t=i/44100
            y=.42*math.sin(2*math.pi*f*t)+.22*math.sin(2*math.pi*2*f*t)+.12*math.sin(2*math.pi*5*f*t)
            y+=random.uniform(-.025,.025)
            buf.extend([int(max(-1,min(1,y))*4500)]*2)
        return pygame.mixer.Sound(buffer=buf.tobytes())
    def update(self,wl,wr):
        if not self.ok:return
        a=min(abs(wl)/18,1); b=min(abs(wr)/18,1)
        vl=.22*a*a if a>.02 else 0; vr=.22*b*b if b>.02 else 0
        self.chL.set_volume(vl,vl*.25); self.chR.set_volume(vr*.25,vr)
    def stop(self):
        if self.ok:self.chL.stop(); self.chR.stop()

def cube(x,y,z):
    x/=2;y/=2;z/=2
    glBegin(GL_QUADS)
    for n,vs in [((0,1,0),[(-x,y,-z),(x,y,-z),(x,y,z),(-x,y,z)]),((0,-1,0),[(-x,-y,z),(x,-y,z),(x,-y,-z),(-x,-y,-z)]),((0,0,1),[(-x,-y,z),(-x,y,z),(x,y,z),(x,-y,z)]),((0,0,-1),[(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,-z)]),((1,0,0),[(x,-y,-z),(x,y,-z),(x,y,z),(x,-y,z)]),((-1,0,0),[(-x,-y,z),(-x,y,z),(-x,y,-z),(-x,-y,-z)])]:
        glNormal3f(*n)
        for v in vs:glVertex3f(*v)
    glEnd()

def draw_world(g):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT); glLoadIdentity()
    r=g.robot
    if g.cinematic:
        bx=r.x-math.sin(r.theta)*7; bz=r.z-math.cos(r.theta)*7
        tx=r.x+math.sin(r.theta)*3; tz=r.z+math.cos(r.theta)*3
        gluLookAt(bx,4.5,bz,tx,.4,tz,0,1,0)
    else: gluLookAt(r.x-math.sin(r.theta)*8,7,r.z-math.cos(r.theta)*8,r.x,0,r.z,0,1,0)
    # ground and road
    glColor3f(.20,.42,.20); glPushMatrix(); glTranslatef(0,-.05,0); cube(44,.1,140); glPopMatrix()
    glColor3f(.15,.15,.16); glPushMatrix(); glTranslatef(0,.01,0); cube(8,.03,140); glPopMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(.9,.75,.2)
    for z in range(-65,70,5):
        glPushMatrix(); glTranslatef(0,.04,z); cube(.12,.02,2.2); glPopMatrix()
    glEnable(GL_LIGHTING)
    # houses / trees
    for x,z in [(-8,-15),(8,-5),(-8,10),(8,22),(-8,37),(8,52),(-8,64),(8,68)]:
        glPushMatrix(); glTranslatef(x,1,z); glColor3f(.62,.48,.35); cube(4,2,4); glTranslatef(0,1.45,0); glColor3f(.35,.12,.08)
        glBegin(GL_TRIANGLES); glVertex3f(-2.3,0,-2);glVertex3f(2.3,0,-2);glVertex3f(0,1.6,0);glVertex3f(2.3,0,2);glVertex3f(-2.3,0,2);glVertex3f(0,1.6,0);glEnd(); glPopMatrix()
    for x,z in [(-5,-8),(5,5),(-5,28),(5,43),(-5,58),(5,67)]:
        glPushMatrix(); glTranslatef(x,1,z); glColor3f(.3,.15,.06); cube(.4,2,.4); glTranslatef(0,1.5,0); glColor3f(.08,.38,.12); q=gluNewQuadric();gluSphere(q,1,12,8);gluDeleteQuadric(q);glPopMatrix()
    # holes
    for x,z,rad in g.holes:
        glColor3f(.03,.03,.03); glPushMatrix();glTranslatef(x,.025,z);glBegin(GL_TRIANGLE_FAN);glVertex3f(0,0,0)
        for i in range(41):
            a=2*math.pi*i/40;glVertex3f(rad*math.cos(a),0,rad*math.sin(a))
        glEnd();glPopMatrix()
    # objects
    for o in g.objects:
        if not o.active:continue
        glPushMatrix();glTranslatef(o.x,.45,o.z)
        if o.kind=='animal':
            glColor3f(.55,.30,.12);glPushMatrix();glScalef(1.2,.6,.6);cube(1,1,1);glPopMatrix();glTranslatef(0,.25,.55);q=gluNewQuadric();gluSphere(q,.35,12,8);gluDeleteQuadric(q)
        else:
            p=.5+.5*math.sin(time.time()*8+o.phase) if o.flash else 0
            glColor3f(.9,.15+.45*p,.04) if o.flash else glColor3f(.2,.45,.7);cube(.9,.9,.9)
        glPopMatrix()
    draw_romi(r)

def draw_romi(r):
    glPushMatrix();glTranslatef(r.x,.25,r.z);glRotatef(math.degrees(r.theta),0,1,0)
    glColor3f(.78,.79,.81);glPushMatrix();glScalef(1,.42,1.35);cube(1,1,1);glPopMatrix()
    glColor3f(.16,.18,.20);glPushMatrix();glTranslatef(0,.25,.05);glScalef(.72,.2,.82);cube(1,1,1);glPopMatrix()
    glDisable(GL_LIGHTING);glColor3f(.1,.65,.75)
    for sx in [-.3,0,.3]:glPushMatrix();glTranslatef(sx,.23,.68);cube(.1,.08,.05);glPopMatrix()
    glEnable(GL_LIGHTING)
    for side,ang in [(-1,r.wheel_l),(1,r.wheel_r)]:
        glPushMatrix();glTranslatef(side*.64,-.02,0);glRotatef(90,0,0,1);glRotatef(math.degrees(ang),1,0,0);glColor3f(.035,.035,.04);q=gluNewQuadric();gluCylinder(q,.20,.20,.12,16,2);gluDisk(q,0,.20,16,1);gluDeleteQuadric(q);glPopMatrix()
    glPopMatrix()

def setup_gl():
    glViewport(0,0,W,H);glMatrixMode(GL_PROJECTION);glLoadIdentity();gluPerspective(58,W/H,.05,250);glMatrixMode(GL_MODELVIEW)
    glClearColor(.07,.11,.15,1);glEnable(GL_DEPTH_TEST);glEnable(GL_LIGHTING);glEnable(GL_LIGHT0);glEnable(GL_COLOR_MATERIAL);glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0,GL_POSITION,(0,14,5,1));glLightfv(GL_LIGHT0,GL_DIFFUSE,(1,1,1,1));glLightfv(GL_LIGHT0,GL_AMBIENT,(.25,.25,.25,1))
    glDisable(GL_CULL_FACE) # prevents the earlier black-triangle artifact

def text(screen_font,text,x,y,size=1,color=(245,245,245)):
    # OpenGL's texture origin is opposite to Pygame's 2-D surface origin.
    # Flip the rendered surface once, then use normal UVs so the question
    # is displayed upright rather than upside-down/inverted.
    s=screen_font.render(text,True,color)
    s=pygame.transform.flip(s,False,True)
    raw=pygame.image.tostring(s,'RGBA',False); tw,th=s.get_size()
    tex=glGenTextures(1);glBindTexture(GL_TEXTURE_2D,tex);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,tw,th,0,GL_RGBA,GL_UNSIGNED_BYTE,raw);glBindTexture(GL_TEXTURE_2D,0)
    glEnable(GL_BLEND);glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);glEnable(GL_TEXTURE_2D);glBindTexture(GL_TEXTURE_2D,tex);glPixelStorei(GL_UNPACK_ALIGNMENT,1);glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE);glColor3f(1,1,1);ww,hh=tw*size,th*size
    glBegin(GL_QUADS);glTexCoord2f(0,1);glVertex2f(x,y);glTexCoord2f(1,1);glVertex2f(x+ww,y);glTexCoord2f(1,0);glVertex2f(x+ww,y+hh);glTexCoord2f(0,0);glVertex2f(x,y+hh);glEnd();glBindTexture(GL_TEXTURE_2D,0);glDisable(GL_TEXTURE_2D);glDisable(GL_BLEND);glDeleteTextures([tex])

def hud(g):
    glMatrixMode(GL_PROJECTION);glPushMatrix();glLoadIdentity();glOrtho(0,W,H,0,-1,1);glMatrixMode(GL_MODELVIEW);glPushMatrix();glLoadIdentity();glDisable(GL_DEPTH_TEST);glDisable(GL_LIGHTING)
    glEnable(GL_BLEND);glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);glColor4f(.02,.03,.04,.8);glBegin(GL_QUADS);glVertex2f(15,15);glVertex2f(450,15);glVertex2f(500,190);glVertex2f(15,190);glEnd();glDisable(GL_BLEND)
    f=g.font
    text(f,f'SCORE: {g.score:.1f}',28,27);text(f,f'v = {g.robot.v:+.3f} m/s   omega = {g.robot.omega:+.3f}',28,55);text(f,f'omega_L = {g.robot.omega_l:+.2f} rad/s',28,82,color=(130,210,255));text(f,f'omega_R = {g.robot.omega_r:+.2f} rad/s',28,109,color=(255,190,120));text(f,f'steering = {g.robot.steering_command:+.1f}   (A left / D right)',28,136,color=(220,220,220));text(f,f'distance = {g.robot.distance:.1f} m',28,163)
    if g.show_hud:text(g.small,'AUTO-CRUISE  |  W/S speed  A/D steering  SPACE brake  C camera  H HUD  R restart',20,H-32)
    if g.message_timer>0:text(g.big,g.message,(W-g.big.size(g.message)[0])//2,180,1,(255,230,110))
    if g.state in ('QUIZ','EXPLAIN','CALC'): challenge(g)
    if g.state in ('WIN','GAMEOVER'):
        glEnable(GL_BLEND);glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);glColor4f(.02,.03,.04,.94);glBegin(GL_QUADS);glVertex2f(260,220);glVertex2f(W-260,220);glVertex2f(W-260,500);glVertex2f(260,500);glEnd();glDisable(GL_BLEND)
        title='LEVEL COMPLETE' if g.state=='WIN' else 'GAME OVER'; sub='Press R to restart'
        text(g.big,title,(W-g.big.size(title)[0])//2,290);text(g.font,sub,(W-g.font.size(sub)[0])//2,365)
    glEnable(GL_LIGHTING);glEnable(GL_DEPTH_TEST);glMatrixMode(GL_MODELVIEW);glPopMatrix();glMatrixMode(GL_PROJECTION);glPopMatrix();glMatrixMode(GL_MODELVIEW)

def challenge(g):
    glEnable(GL_BLEND);glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);glColor4f(.02,.03,.05,.97);glBegin(GL_QUADS);glVertex2f(140,175);glVertex2f(W-140,175);glVertex2f(W-140,575);glVertex2f(140,575);glEnd();glDisable(GL_BLEND)
    y=205
    if g.state=='QUIZ':
        text(g.big,'STM32-AOR KNOWLEDGE CHECK',180,y,color=(255,220,100));y+=55;text(g.font,g.q[0],180,y);y+=45
        for i,a in enumerate(g.q[1]):text(g.font,f'{i+1}. {a}',200,y);y+=38
        text(g.font,'Type 1-4 and press ENTER.',180,y+10);y+=40
    elif g.state=='EXPLAIN':
        text(g.big,'ENGINEERING EXPLANATION',180,y,color=(255,220,100));y+=55;text(g.font,g.e[0],180,y);y+=55;text(g.font,'Explain it in your own words, then press ENTER.',180,y);y+=45
    else:
        v,o=g.calc;text(g.big,'WHEEL-KINEMATICS CHALLENGE',180,y,color=(255,220,100));y+=55;text(g.font,f'Given v={v:.2f} m/s and omega={o:+.2f} rad/s:',180,y);y+=45;text(g.font,'enter omega_L and omega_R separated by a space.',180,y);y+=45
    y += 18
    text(g.font,'> '+g.answer,180,y,color=(150,230,255))

class Game:
    def __init__(self):
        self.font=pygame.font.SysFont('DejaVu Sans',22,bold=True);self.big=pygame.font.SysFont('DejaVu Sans',30,bold=True);self.small=pygame.font.SysFont('DejaVu Sans',17);self.reset()
    def reset(self):
        self.robot=Romi();self.score=0;self.state='PLAYING';self.cinematic=True;self.show_hud=True;self.answer='';self.message='';self.message_timer=0;self.next_event=11;self.qindex=0;self.auto_cruise=True
        self.objects=[];random.seed(17)
        for z in range(-18,65,7):self.objects.append(Obj(random.uniform(-2.4,2.4),z,'obstacle',random.random()<.28))
        for x,z in [(-4,6),(4,20),(-4,36),(4,54)]:self.objects.append(Obj(x,z,'animal'))
        self.holes=[(-4,2,1.1),(4,17,1.0),(-4,32,1.15),(4,49,1.0)]
        self.sound=MotorSound()
    def say(self,s,t=2):self.message=s;self.message_timer=t
    def start_event(self):
        m=self.qindex%3;self.qindex+=1;self.answer=''
        if m==0:self.state='QUIZ';self.q=random.choice(QUESTIONS)
        elif m==1:self.state='EXPLAIN';self.e=random.choice(EXPL);self.e[0]
        else:self.state='CALC';self.calc=(random.choice([.2,.3,.4]),random.choice([-1.2,.8,1.5]))
    def submit(self):
        if self.state=='QUIZ':
            try:ok=int(self.answer.strip())-1==self.q[2]
            except:ok=False
            self.score+=8 if ok else -4;self.say('+8 Correct' if ok else '-4 Incorrect');self.state='PLAYING';self.next_event=self.robot.distance+13
        elif self.state=='EXPLAIN':
            t=self.answer.lower();hits=sum(k in t for k in self.e[1]);ok=hits>=2;self.score+=10 if ok else -5;self.say('+10 Explanation accepted' if ok else '-5 Explanation needs improvement');self.state='PLAYING';self.next_event=self.robot.distance+13
        else:
            v,o=self.calc;el=(v-L*o/2)/R;er=(v+L*o/2)/R
            try:a=[float(x) for x in self.answer.replace(',',' ').split()];ok=len(a)>=2 and abs(a[0]-el)<.8 and abs(a[1]-er)<.8
            except:ok=False
            self.score+=12 if ok else -6;self.say('+12 Calculation correct' if ok else f'-6 Expected L={el:.2f}, R={er:.2f}',2.8);self.state='PLAYING';self.next_event=self.robot.distance+15
    def update(self,dt,keys):
        if self.message_timer>0:self.message_timer-=dt
        if self.state!='PLAYING':self.sound.update(0,0);return
        th=(0.42 if self.auto_cruise else 0.0)+(1.0 if keys[pygame.K_w] else 0.0)-(0.65 if keys[pygame.K_s] else 0.0);st=(1 if keys[pygame.K_d] else 0)-(1 if keys[pygame.K_a] else 0)
        if keys[pygame.K_SPACE]:th=st=0
        self.robot.update(th,st,dt);self.score+=.025*(abs(self.robot.v)/VMAX+abs(self.robot.omega)/OMAX)*dt;self.sound.update(self.robot.omega_l,self.robot.omega_r)
        for o in self.objects:
            if not o.active:continue
            d=math.hypot(o.x-self.robot.x,o.z-self.robot.z)
            if d<(.8 if o.kind=='animal' else .7):o.active=False;self.score+=-25 if o.kind=='animal' else -15;self.say('-25 Animal collision' if o.kind=='animal' else '-15 Obstacle collision');continue
            if not o.passed and o.z<self.robot.z-.8 and abs(o.x-self.robot.x)<2.5 and o.kind=='obstacle':o.passed=True;pts=4 if o.flash else 1;self.score+=pts;self.say(f'+{pts} Flashing obstacle passed' if o.flash else '+1 Obstacle passed',1.3)
        for x,z,rad in self.holes:
            if math.hypot(self.robot.x-x,self.robot.z-z)<rad+.35:self.score-=8*dt;self.robot.v*=max(0,1-3*dt)
        if self.robot.distance>=self.next_event:self.start_event()
        if self.robot.z>WORLD_Z-4:self.state='WIN';self.say('LEVEL COMPLETE',10)
        if self.score<-100:self.state='GAMEOVER'

def main():
    pygame.init();pygame.display.set_caption('STM32-AOR 3D Game v3');pygame.display.set_mode((W,H),DOUBLEBUF|OPENGL);setup_gl();clock=pygame.time.Clock();g=Game();run=True
    while run:
        dt=min(clock.tick(60)/1000,.04)
        for e in pygame.event.get():
            if e.type==QUIT:run=False
            elif e.type==KEYDOWN:
                if e.key==K_ESCAPE:run=False
                elif e.key==pygame.K_r:g.reset()
                elif e.key==pygame.K_c:g.cinematic=not g.cinematic
                elif e.key==pygame.K_h:g.show_hud=not g.show_hud
                elif g.state in ('QUIZ','EXPLAIN','CALC'):
                    if e.key==pygame.K_BACKSPACE:g.answer=g.answer[:-1]
                    elif e.key==pygame.K_RETURN:g.submit()
                    elif e.unicode and e.unicode.isprintable():g.answer+=e.unicode
        g.update(dt,pygame.key.get_pressed());draw_world(g);hud(g);pygame.display.flip()
    g.sound.stop();pygame.quit()
if __name__=='__main__':main()
