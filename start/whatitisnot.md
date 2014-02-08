---
title:   What MyHDL is not 
layout:  article
---

Introduction
============

There are [many good reasons](:why) to consider MyHDL. However, to use it
effectively, it is important to have realistic expectations. The easiest way to
achieve this is perhaps to describe what MyHDL is *not*. 

Not a way to turn arbitrary Python into silicon
===============================================

Arbitrary Python into silicon, that sounds like a dream, right? And it is :-)
Don't expect this from MyHDL.

To convert MyHDL code into hardware, you will have to learn about
[synthesis](http://en.wikipedia.org/wiki/Logic_synthesis), and especially about
the modeling constraints that it imposes. These constraints are significant,
and therefore synthesizable code may be suprisingly low-level to newcomers.

Not a radically new approach
============================

The mainstream Hardware Description Languages are Verilog and VHDL. MyHDL was
not created because these languages do everything wrong. Quite the contrary.

According to the analysis of MyHDL's creator, the promise of HDL-based design
has not been fulfilled *despite* the fact that Verilog and VHDL do many things
right. MyHDL tries to lower the barrier to entry and improve on certain
language features that make the task more difficult than necessary. 

The most important MyHDL design choice is to implement it as a Python library
instead of as a separate language. This makes it available to a much broader
public, and opens the way to modern software development techniques such as
test-driven design (TDD).

However, fundamentally MyHDL is based on the same event-driven paradigm as
Verilog and VHDL. This has proven to be the winning solution for HDL design.

Not a synthesis tool
====================

MyHDL alone is not sufficient to convert code into a hardware implementation.
In other words, it is not a synthesis tool.

However, MyHDL contains a convertor tool that you can use to convert
synthesizable MyHDL code into equivalent Verilog or VHDL code. From there on,
you can use standard synthesis tools to get to an implementation. Synthesis
tools are available from EDA vendors and FPGA vendors. Some synthesis tools
from FPGA vendors are cheap or even free.

Although the convertor in MyHDL is not a synthesis tool, it automates a number
of tasks which are harder to do in Verilog or VHDL directly.

Not an IP block library
=======================

The term *IP* (Intellectual Property) is used in the context of hardware design
to refer to hardware blocks that are designed to be easily reusable in other
designs.

MyHDL does not contain IP blocks. What it provides is the raw material to
design them. Actually, MyHDL is the ideal platform for IP block development,
because of its powerful Python foundation, and because it provides a path into
both Verilog and VHDL design flows with a single development effort.

Not only for implementation
===========================

MyHDL is very effective to describe a hardware implementation. The
corresponding abstraction level is called *RTL* (Register Transfer Level).
Typically, RTL code is converted into hardware implementation by a *synthesis*
tool. Another name for RTL is therefore synthesizable code.

However, MyHDL is not an RTL-only language. This point is frequently
misunderstood, even though it is also valid for mainstream HDLs such as Verilog
and VHDL.

MyHDL is a library for general event-driven modeling and simulation of hardware
systems. There are many reasons why it can be useful to model at a higher level
of abstraction than RTL. For example, you can use MyHDL to verify architectural
features, such as system throughput, latency and buffer sizes. You can also
write high level models for specialized technology-dependent cores that are not
going through synthesis. Last but not least, you can use MyHDL to write test
benches that verify a system model or a synthesizable description.

RTL is just a specific and restrictive way to use MyHDL's modeling capabilities
with the goal to create synthesizable code.

Not well suited for timing simulation
=====================================

MyHDL's delay model is simple, which is fine for RTL and higher levels of
abstraction. These are the levels where MyHDL is strong.

However, MyHDL's timing model is not suited for accurate timing simulations,
which are typically useful at the gate level. For such simulations, it is
advisable to use industry standard Verilog or VHDL simulators, which are
optimized for the task. Moreover, gate level simulation libraries are typically
available in those formats from silicon vendors. In a MyHDL-based design flow,
this methodology is logical, because all tasks below RTL are part of the
"back-end". The synthesis tool will create a gate level net list in Verilog or
VHDL format.

MyHDL can still play a significant role in gate-level simulations, thanks to
its co-simulation capabilities. This means that you can reuse all MyHDL test
benches that were developed for RTL verification to control gate level
simulations.
