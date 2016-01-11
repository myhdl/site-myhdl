---
title:   Flip-flops and Latches 
layout:  article
summary.md: | 
    * modelling and simulating small sequential devices
    * waveform viewing
    * automatic conversion to Verilog
---

Introduction
============

On this page you will find a number of MyHDL descriptions of flip-flops and
latches.

Typically, you wouldn't describe flip-flops and latches as individual modules.
Rather, they can be inferred from higher-level  RTL description by a synthesis
tool. However, as these circuits are small and widely known, they are well
suited to explain basic MyHDL usage and to compare MyHDL with other solutions.

D flip-flop
===========

Specification
-------------

The basic D flip-flop is a sequential device that transfers the value of the
`d` input to the `q` output on every rising edge of the clock `clk`.

Description
-----------
Here is the description of a D flip-flop in MyHDL:

```python
from myhdl import *

def dff(q, d, clk):

    @always(clk.posedge)
    def logic():
        q.next = d

    return logic
```

Simulation
----------

Let's write a small test bench to simulate the design:

```python
from random import randrange

def test_dff():
    
    q, d, clk = [Signal(bool(0)) for i in range(3)]
    
    dff_inst = dff(q, d, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        d.next = randrange(2)

    return dff_inst, clkgen, stimulus


def simulate(timesteps):
    tb = traceSignals(test_dff)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(2000)

```

Function `test_dff` creates an instance of the D flip-flop, and adds a clock
generator and a random stimulus generator around it.

Function `simulate` simulates the test bench. Note how the MyHDL function
`traceSignals` is used to create the test bench instance (instead of calling
`test_dff` directly). As a result, a signal trace file will be created during
simulation. This file can be inspecting in a waveform viewer. As a verification
method, inspecting waveforms has its drawbacks, but it can be very effective to
debug small designs.

Here's a screen shot of the simulation waveforms:

<img src="test_dff.jpg" class="img-responsive" alt="test_dff waveforms">

Automatic conversion to Verilog
-------------------------------

With MyHDL's `toVerilog` function, a D flip-flop instance can be converted to
Verilog code:

```python
def convert():
    q, d, clk = [Signal(bool(0)) for i in range(3)]
    toVerilog(dff, q, d, clk)

convert()

```

This is the resulting Verilog code:

```verilog
module dff (
    q,
    d,
    clk
);

output q;
reg q;
input d;
input clk;

always @(posedge clk) begin: _dff_logic
    q <= d;
end

endmodule
```

D flip-flop with asynchronous reset
===================================

Specification
-------------

One of the most useful sequential building blocks is a D flip-flop with an
additional asynchronous reset pin. When the reset is not active, it operates as
a basic D flip-flop as in the previous section. When the reset pin is active,
the output is held to zero. Typically, the reset pin is active low.

Description
-----------

Here is the description:

```python
from myhdl import *

def dffa(q, d, clk, rst):

    @always(clk.posedge, rst.negedge)
    def logic():
        if rst == 0:
            q.next = 0
        else:
            q.next = d

    return logic

```

Simulation
----------

Here is a test bench for the design:

```python
from random import randrange

def test_dffa():
    
    q, d, clk, rst = [Signal(bool(0)) for i in range(4)]
    
    dffa_inst = dffa(q, d, clk, rst)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        d.next = randrange(2)

    @instance
    def rstgen():
        yield delay(5)
        rst.next = 1
        while True:
            yield delay(randrange(500, 1000))
            rst.next = 0
            yield delay(randrange(80, 140))
            rst.next = 1

    return dffa_inst, clkgen, stimulus, rstgen

def simulate(timesteps):
    tb = traceSignals(test_dffa)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(20000)
```

Compared to the test bench for the basic D flip-flop, there is an additional
reset generator, that generates reset pulses at random moments and with a
random duration.

Here is a screen shot of the waveforms:

<img src="test_dffa.jpg" class="img-responsive" alt="test_dffa waveforms">

Automatic conversion to Verilog
-------------------------------

The design can be converted to Verilog as follows:

```python
def convert():
    q, d, clk, rst = [Signal(bool(0)) for i in range(4)]
    toVerilog(dffa, q, d, clk, rst)
 
convert()
```
 
The result looks like this:

```verilog
module dffa (
    q,
    d,
    clk,
    rst
);

output q;
reg q;
input d;
input clk;
input rst;


always @(posedge clk or negedge rst) begin: _dffa_logic
    if ((rst == 0)) begin
        q <= 0;
    end
    else begin
        q <= d;
    end
end

endmodule
```

Latch
=====

Specification
-------------

A basic latch is a sequential device with an input, and output and a control
gate pin. When the gate is open, the output follows the input combinatorially.
When it is closed, the output keeps its value.

Description
-----------

The following code describes a latch:

```python
from myhdl import *

def latch(q, d, g):

    @always_comb
    def logic():
        if g == 1:
            q.next = d

    return logic
```

Note the usage of the `always_comb` decorator. This is somewhat of a misnomer.
(The name comes from a similar construct in SystemVerilog). It doesn't mean the
generator describes a circuit that is necessarily combinatorial, but merely
that it triggers whenever one of the input signals changes.

Simulation
----------

Here is a test bench to simulate the latch:

```python
from random import randrange

def test_latch():
    
    q, d, g = [Signal(bool(0)) for i in range(3)]
    
    latch_inst = latch(q, d, g)

    @always(delay(7))
    def dgen():
        d.next = randrange(2)

    @always(delay(41))
    def ggen():
        g.next = randrange(2)


    return latch_inst, dgen, ggen

def simulate(timesteps):
    tb = traceSignals(test_latch)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(20000)
```

In addition to the latch instance, the test bench creates a random data
generator for the input and for the controlling gate.

Here is a screen shot of the simulation waveforms:

<img src="test_latch.jpg" class="img-responsive" alt="test_latch waveforms">

Automatic conversion to Verilog
-------------------------------

We can convert the design as follows:

```python
def convert():
    q, d, g = [Signal(bool(0)) for i in range(3)]
    toVerilog(latch, q, d, g)
 
convert()
```

Here is the result:

```verilog
module latch (
    q,
    d,
    g
);

output q;
reg q;
input d;
input g;

always @(d, g) begin: _latch_logic
    if ((g == 1)) begin
        q <= d;
    end
end

endmodule
```

Note that when the `toVerilog` function converts the `always_comb` decorator,
it infers which signals are used as inputs to the `always` block
