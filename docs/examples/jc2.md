---
title:   Johnson Counter 
layout:  wide_article
summary.md: |
    * modelling a counter
    * writing a test bench for the counter and simulating it
    * automatic conversion to Verilog
---

Introduction
============

On this page we will present the design of a reversable 4 bit Johnson counter.
A Johnson counter has a special structure that permits glitch-free decoding.

This example is originally from the Xilinx ISE design environment. If you wish,
you can [ download the free version](http://www.xilinx.com/ise/logic_design_prod/webpack.htm) of the Xilinx
ISE to review the original design and use it as a reference.

Specification
=============

A Johnson counter basically consists of a circular shift register with an invertor in the loop.

The specification of the counter operation is as follows:

The counter is triggered on the rising edge of the clock (clk). 
A low pulse on the goLeft input will cause the counter to start 
shifting left from its current state. A low pulse on the goRight
input will cause the counter to start shifting right from its 
current state. A low pulse on the stop input will cause the 
counter to hold its current state until goLeft or goRight is pulsed.
After power-up, the counter is stopped with all outputs low (LEDs lit).

MyHDL code
==========

The MyHDL code for this design looks as follows.

```python

from myhdl import *

ACTIVE = 0
DirType = enum('RIGHT', 'LEFT')

def jc2(goLeft, goRight, stop, clk, q):
    
    """ A bi-directional 4-bit Johnson counter with stop control.

    I/O pins:
    --------
    clk      : input free-running slow clock 
    goLeft   : input signal to shift left (active-low switch)
    goRight    : input signal to shift right (active-low switch)
    stop     : input signal to stop counting (active-low switch)
    q        : 4-bit counter output (active-low LEDs; q[0] is right-most)

    """

    dir = Signal(DirType.LEFT)
    run = Signal(False)

    @always(clk.posedge)
    def logic():
        # direction
        if goRight == ACTIVE:
            dir.next = DirType.RIGHT
            run.next = True
        elif goLeft == ACTIVE:
            dir.next = DirType.LEFT
            run.next = True
        # stop
        if stop == ACTIVE:
            run.next = False
        # counter action
        if run:
            if dir == DirType.LEFT:
                q.next[4:1] = q[3:]
                q.next[0] = not q[3]
            else:
                q.next[3:] = q[4:1]
                q.next[3] = not q[0]

    return logic
```

We use an enumerated type for the direction state `dir`. We prefer this for
clarity when the encoding is not specified.

Test bench
==========

The following is a test bench for a basic verification of the design.

```python
from myhdl import *

ACTIVE, INACTIVE = bool(0), bool(1)

from jc2 import jc2

def test(jc2):
    
    goLeft, goRight, stop, clk = [Signal(INACTIVE) for i in range(4)]
    q = Signal(intbv(0)[4:])
    
    @always(delay(10))
    def clkgen():
        clk.next = not clk

    jc2_inst = jc2(goLeft, goRight, stop, clk, q)

    @instance
    def stimulus():
        for i in range(3):
            yield clk.negedge
        for sig, nrcycles in ((goLeft, 10), (stop, 3), (goRight, 10)):
            sig.next = ACTIVE
            yield clk.negedge
            sig.next = INACTIVE
            for i in range(nrcycles-1):
                yield clk.negedge
        raise StopSimulation

    @instance
    def monitor():
        print "goLeft goRight stop clk q"
        print "-------------------------"
        while True:
            yield clk.negedge
            yield delay(1)
            print "%d %d %d" % (goLeft, goRight, stop) ,
            yield clk.posedge
            print "C",
            yield delay(1)
            print bin(q, 4)

    return clkgen, jc2_inst, stimulus, monitor

sim = Simulation(test(jc2))
sim.run()
```

We use a number of decorated functions to create a clock generator, a stimulus
generator, and a response monitor, together with an instance of the design
under test. Such a setup is quite typical.

When we simulate this test bench, the output is as follows:

```
$ python test_jc2.py
goLeft goRight stop clk q
-------------------------
1 1 1 C 0000
1 1 1 C 0000
0 1 1 C 0000
1 1 1 C 0001
1 1 1 C 0011
1 1 1 C 0111
1 1 1 C 1111
1 1 1 C 1110
1 1 1 C 1100
1 1 1 C 1000
1 1 1 C 0000
1 1 1 C 0001
1 1 0 C 0011
1 1 1 C 0011
1 1 1 C 0011
1 0 1 C 0011
1 1 1 C 0001
1 1 1 C 0000
1 1 1 C 1000
1 1 1 C 1100
1 1 1 C 1110
1 1 1 C 1111
1 1 1 C 0111
1 1 1 C 0011
1 1 1 C 0001
```

You can see the basic operation of the Johnson counter in action.

The presented test bench is rather basic. It is fine to get a quick idea about
the design behavior, but it is inadequate as a verification tool. First, some
corner case are not verified, such as the simultaneous occurence of some of the
input signals. Also, it relies on visual inspection which is prone to human
error  and not suited for regression testing.

A better approach would be to write a self-checking test bench that checks
Johnson counter properties automatically, plus a number of directed and random
tests to cover corner cases. In addition, such a test bench should be written
using a unit test framework such as Python's `unittest` package, to facilitate
test writing and to make it part of a regression test suite. Consult the MyHDL
manual for more info on such techniques.

Automatic conversion to Verilog
===============================

A working MyHDL design intended for implementation can be converted to Verilog
automatically, using the `toVerilog` function. Remember: there is no point in
converting when the design doesn't work. The simulation will catch much more
errors than the converter. In MyHDL, like in Python, the run-time rules.

Conversion to Verilog can be done with code like the following:

```python
def convert(jc2):
    left, right, stop, clk = [Signal(INACTIVE) for i in range(4)]
    q = Signal(intbv(0)[4:])
    toVerilog(jc2, left, right, stop, clk, q)

convert(jc2)
```

As you see, conversion works on an instantiated, elaborated design.

The resulting Verilog code is as follows:

```verilog
module jc2 (
    goLeft,
    goRight,
    stop,
    clk,
    q
);

input goLeft;
input goRight;
input stop;
input clk;
output [3:0] q;
reg [3:0] q;

reg run;
reg [0:0] dir;


always @(posedge clk) begin: _jc2_logic
    if ((goRight == 0)) begin
        dir <= 1'b0;
        run <= 1;
    end
    else if ((goLeft == 0)) begin
        dir <= 1'b1;
        run <= 1;
    end
    if ((stop == 0)) begin
        run <= 0;
    end
    if (run) begin
        // synthesis parallel_case full_case
        casez (dir)
            1'b1: begin
                q[4-1:1] <= q[3-1:0];
                q[0] <= (!q[3]);
            end
            default: begin
                q[3-1:0] <= q[4-1:1];
                q[3] <= (!q[0]);
            end
        endcase
    end
end

endmodule
```

The tests to the `dir` variable in the MyHDL code are mapped to a Verilog
`case` statement. This is because the Verilog convertor handles comparisons to
enumerated type items in a special way. The goal is to describe finite state
machines efficiently. For example, it is possible to specify a different
encoding using the `encoding` attribute of the enumerated type. The choices are
`binary` (the default), `one_hot`, and `one_cold`. Of course, with only 2
states like in this case, this functionality is not relevant. But in general,
it is an additional advantage of the use of enumerated types.

Alternative design
==================

This is not yet the end of the story.

The original design in the Xilinx ISE distribution contains 3 views: Abel,
Verilog, and VHDL. Interestingly, the Verilog and VHDL views are inconsistent:
they have a different behavior. In Verilog terminology, the Verilog view uses
blocking assignments only, while the VHDL view uses non-blocking (= signal)
assignments only. The VHDL view seems to be consistent with the Abel view and
with the supplied test vectors, so it has been the basis of the design that has
been discussed so far. However, it is interesting to investigate what the
implications of the Verilog view would be on the MyHDL code. Actually, the role
of blocking and non-blocking assignments in Verilog is poorly understood, and I
believe MyHDL can help to clarify the issues. (The reason is that MyHDL, like
VHDL but unlike Verilog, makes a clear difference between signals and
variables).

Consider how long it takes before a control input change influences the counter
output. In the discussed design, it takes two clock edges: one edge to set the
state registers `dir` and `run`, and one edge to see the influence of the state
registers on the count. You can verify this behavior from the test bench
output. (Note that inputs are sampled before the clock edge, and outputs after
the clock edge).

Now suppose we would prefer to influence the count output after a single clock
edge. Can this be done? The answer is positive: however, to support that we
will need to use variables instead of signals for the state registers `dir` and
`run`. 

The modified MyHDL code looks as follows:

```python
from myhdl import *

ACTIVE = 0
DirType = enum('RIGHT', 'LEFT')

def jc2_alt(goLeft, goRight, stop, clk, q):
    
    """ A bi-directional 4-bit Johnson counter with stop control.

    I/O pins:
    --------

    clk      : input free-running clock 
    goLeft   : input signal to shift left (active-low switch)
    goRight  : input signal to shift right (active-low switch)
    stop     : input signal to stop counting (active-low switch)
    q        : 4-bit counter output (active-low LEDs; q[0] is right-most)

    """

    @instance
    def logic():
        dir = DirType.LEFT
        run = False
        while True:
            yield clk.posedge
            # direction
            if goRight == ACTIVE:
                dir = DirType.RIGHT
                run = True
            elif goLeft == ACTIVE:
                dir = DirType.LEFT
                run = True
            # stop
            if stop == ACTIVE:
                run = False
            # counter action
            if run:
                if dir == DirType.LEFT:
                    q.next[4:1] = q[3:]
                    q.next[0] = not q[3]
                else:
                    q.next[3:] = q[4:1]
                    q.next[3] = not q[0]

    return logic
```

The `instance` decorator is used to create the `logic` generator from the
corresponding generator function. The main functionality of that function is
wrapped in a `while True` loop to keep the generator alive "forever". The first
statement in the loop is a `yield` statement that specifies the sensitivity to
the clock edge. Variables `dir` and `run` are local state variables, that keep
their previous value through each iteration of the `while` loop.

You may wonder why we couldn't use the `always` decorator with a clock edge
argument as before. The reason is that in that case, the decorated function is
a classic (= non-generator) function that would be called on every clock edge.
However, local variables loose their value whenever a function returns, so they
cannot hold state. Therefore, we need to use a more general approach and code
the desired behavior explicitly in a generator function.

This example is more subtle and complex than it may seem at first sight. As
said before, variables `dir` and `run` are state variables and will therefore
require a flip-flop in an implementation. However, they are also used
"combinatorially": when they change, they may influence the counter operation
"in the same clock cycle", that is, before the flip-flop output changes. This
is perfectly fine behavior and no problem for synthesis tools, but it tends to
confuse a lot of designers. This coding style is also a favourite theme of this
author :-) ( --- *[Jan Decaluwe](jan@jandecaluwe.com)*). 

To verify whether we now have the desired behavior, we can run the original
test bench on the alternative design:

```
Alternative design
------------------
goLeft goRight stop clk q
-------------------------
1 1 1 C 0000
1 1 1 C 0000
0 1 1 C 0001
1 1 1 C 0011
1 1 1 C 0111
1 1 1 C 1111
1 1 1 C 1110

1 1 1 C 1100
1 1 1 C 1000
1 1 1 C 0000
1 1 1 C 0001
1 1 1 C 0011
1 1 0 C 0011
1 1 1 C 0011
1 1 1 C 0011
1 0 1 C 0001
1 1 1 C 0000
1 1 1 C 1000
1 1 1 C 1100
1 1 1 C 1110
1 1 1 C 1111
1 1 1 C 0111
1 1 1 C 0011
1 1 1 C 0001
1 1 1 C 0000
```

If you compare this output with the previous one, you will see that the counter
response to a control input change is now indeed one clock cycle earlier.

Like before, we can convert the MyHDL code automatically to Verilog:

```verilog
module jc2_alt (
    goLeft,
    goRight,
    stop,
    clk,
    q
);

input goLeft;
input goRight;
input stop;
input clk;
output [3:0] q;
reg [3:0] q;



always @(posedge clk) begin: _jc2_alt_logic
    reg run;
    reg [1-1:0] dir;
    if ((goRight == 0)) begin
        dir = 1'b0;
        run = 1;
    end
    else if ((goLeft == 0)) begin
        dir = 1'b1;
        run = 1;
    end
    if ((stop == 0)) begin
        run = 0;
    end
    if (run) begin
        // synthesis parallel_case full_case
        casez (dir)
            1'b1: begin
                q[4-1:1] <= q[3-1:0];
                q[0] <= (!q[3]);
            end
            default: begin
                q[3-1:0] <= q[4-1:1];
                q[3] <= (!q[0]);
            end
        endcase
    end
end

endmodule
```

Verilog's always block is more general than the MyHDL `always` decorator,
because you cannot use local state variables with the latter. However, even
though the MyHDL code for the alternative design doesn't use the `always`
decorator, the convertor is smart enough to see that it can still use it in the
Verilog code in this case.

Note that blocking and non-blocking assignments are mixed in the always block.
This is necessary to match the behavior of the alternative MyHDL design. In the
Verilog world, you may encounter rules that forbid such a coding style. Such
rules are typically created by designers that prefer to focus on "thinking
hardware" instead of thinking in terms of code, even when synthesis tools are
perfectly able to create efficient hardware from that code. The best you can do
with such rules is to ignore them.
