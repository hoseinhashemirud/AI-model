### C1
**where** reviews/2026-09-09w-content-review.qmd/C1 <br>
the quantization is 1/200 not 1/100. the state would be $x=[0.4,\ 0.125,\ 0.5]^T$ rather than $x=[0.8,\ 0.25,\ 1.0]^T$ so the $y=[+0.7,0.25]^T$ $\rightarrow$ and it should turn to the right. 
The motor commands would be: $u_s=0.7 , u_v=0.25$, as $v_l=u_v*(1+u_s)$ and $v_r=u_v*(1-u_s)$ $\rightarrow$ $v_l=0.425,v_r=0.075$ $\rightarrow$ left motor 42.5% and right motor 7.5% is on and the robot turns right. It means the push on the right wheel is less.<br>
**status**: should be corrected and added formulas of speed of right and left motor.

### C2
**where** reviews/2026-09-09w-content-review.qmd/C2<br>
the quantization rate is $1/200$ and $1.1*200=220$ cm that is outside the assumed 200 cm maximum.
$d_{normalized}=d_{measured}/200$, it is just supposed to show that when the robot is moving the sensor reading will be changed.  
The corrected format is: $$[0.80,\ 0.25,\ 1.00] \rightarrow [-0.65,\ 0.20] \rightarrow [0.60,\ 0.35,\ 0.95]$$
There is another thing here should be corrected:<br>
- AI Model: $s_t \rightarrow a_t$<br>
- Environment: $(s_t, a_t) \rightarrow s_{t+1}$ <br>
$s_{t+1}=f_{environment}(s_t, a_t)$<br>
**status**: should be corrected the number and formula.

### C3
**where** reviews/2026-09-09w-content-review.qmd/C3<br>
The steering command ($u_s$) is in [-1,1] so that the steering-wheel can be turned to the right at the interval [0,1] and to the left at the interval [-1,0]. for instant, if the steering command is -0.86 that means the steering-wheel -0.86* Pi-Number (Rad) is rotated to the left.-negative sign means turn to the left-
Besides, desired speed($u_v$) produced by the neural network is in [0,1]. For instance if it is 0.6 the desired speed command is 0.6 m/sec and the value is 0.6*(maximum speed).<br>
**status**: should be added to the notes/03-formal-model.

### W1
**where** reviews/2026-09-09w-content-review.qmd/W1<br>
All of the 3 pages are one topic.
The words on the tope of the pages like "for example" will be edited to make a coherent writing.<br>
**status**: should be edited and assign one topic to all of 3 pages of notes/01-ai-model.qmd, notes/02-agent-and-environment.qmd and notes/03-formal-model.qmd.

### W2
**where** reviews/2026-09-09w-content-review.qmd/W2<br>
"It is a realistic example of an AI agent running directly on a microcontroller" should be altered to "A realistic example of an AI agent running directly on a microcontroller will be given here."<br>
**status**: text should be changed.

### W3
**where** reviews/2026-09-09w-content-review.qmd/W3<br>
The picture will be explained in the text.<br>
**status**: comment on the text should be added and a 100KB image should be loaded  instead.

### W4
**where** reviews/2026-09-09w-content-review.qmd/W4<br>
The second title in notes/01-ai-model.qmd should be change to "The environment".<br>
**status**: the subtitle should be corrected. any related sentences should be conveyed.

### W5
**where** reviews/2026-09-09w-content-review.qmd/W5<br>
**status**: the paranthesis should be eliminated from the text format.


### Gaps
**where** reviews/2026-09-09w-content-review.qmd/Gaps<br>
**status**: some materials should be added as they are suggested by reviews/2026-09-09w-content-review.qmd/Gaps.





