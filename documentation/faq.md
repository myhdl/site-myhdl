---
title:   FAQ 
layout:  article
---

Modeling
========

What is the default width of an `intbv`?
----------------------------------------

By default, an `intbv` object has an "indefinite" bit width. Although this is a novel concept compared to traditional HDL modeling, it corresponds to the natural way to think about integers and their 2's complement representation. Consider:

```python
>>> from myhdl import intbv
>>> a = intbv(5)
>>> a[75] = 1
>>> a
intbv(37778931862957161709573L)
>>> a[77:74]
intbv(2L)
```

This illustrates that you can index and slice an `intbv` object with arbitrary indices, without having to declare a bit width at object construction time.

The default is fine for modeling at a very high level. Other applications require a defined bit width, and this is supported by the `intbv` class also.

How do I define the width of an `intbv`?
--------------------------------------

To define the bit width of an `intbv` object, you have two options.

The first method is an indirect one that specifies the acceptable value range using the `min` and `max` parameters. For example:

```python
a = intbv(0, min=-24, max=75)
```

As always in Python, the minimum value is inclusive, but the maximum value is exclusive. Note how this method stresses the "integer" nature of an `intbv`.

The second method defines the bit width directly, as follows:

```python
a = intbv(0)[8:]
```

This works because when you take a slice from an intbv, the returned object is a new `intbv` with a bit width `w` corresponding to the slicing range. The min and max value are set to `0` and `2**w` respectively. Note that the object returned by a slice is always positive, as in Verilog.

The range of acceptable values of an `intbv` object is checked at simulation runtime. This is an interesting application of defining a bit width. Another application is implementation-oriented modeling, such as code that needs to be converted automatically to synthesizable Verilog.

How can I model wrap-around behaviour?
---------------------------------------

In HDLs such as Verilog and VHDL, the bit vectors have wrap-around behaviour. This means that when the result of a numeric operation would exceed the bit width, the higher order bits are dropped automatically. In effect, the operations are done modulo the power of 2 of the bit width.

MyHDL's `intbv` object is much like an integer. Therefore, it doesn't have this wrap-around behavior. If needed, it has to be described explicitly.

The most straightforward way to describe wrap-around behavior is with an if-then-else. For example:

```python
if count < N:
    count.next = count + 1
else:
    count.next = 0
```

This may seem a little verbose compared to automatic wrap-around, but in many cases there is no overhead. Often, something else will have to be done depending on the condition (such as setting a control signal) so you can directly add that in the code. Moreover, the wrap-around condition is not limited to powers of 2.

To describe wrap-around behaviour with a one-liner, you can use the modulo operation:

```python
count.next = (count + 1) % N
```

Conversion to Verilog and VHDL
==============================

How can I use third-party modules?
----------------------------------

You can use
[user-defined code](http://www.myhdl.org/en/latest/manual/conversion.html#user-defined-code)
to replace a MyHDL module by a corresponding instantiation.

Why is the conversion output non-hierarchical?
----------------------------------------------

The conversion output is non-hierarchical because conversion works
on a design instance elaborated by the Python interpreter. This
process flattens out all hierarchy.

You can generate hierarchical designs by some additional work,
in particular by converting lower level modules and using
user-defined instantiation code at a higher level. This
technique is explained
[here](http://www.myhdl.org/en/latest/manual/conversion.html#handling-hierarchy).



Co-simulation
=============


How can I run co-simulation on Windows?
---------------------------------------

The implementation of co-simulation in MyHDL relies on unix-style interprocess communication. Therefore, unlike the rest of MyHDL, you cannot use co-simulation on Windows natively.

To run co-simulation on Windows, use a unix-like environment for Windows, such as cygwin. You will have to compile all co-simulation tools in that environment. This includes Python itself, the HDL simulator, and the PLI module.

Users have reported co-simulation success on Windows using cygwin and the Verilog simulators Icarus and Cver.

