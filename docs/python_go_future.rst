Why Python and Go is the Future
=======

When comparing languages, it’s easy to compare each one’s features and capabilities on paper.

Lost in this comparison is what you gain as a collaborative team by the efficiency and maintainability of a language favoring simplicity and practicality over cleverness and possibilities.

Restrictions like enforced whitespace as part of the code logic, and in most cases, only one way to do something, mean that most Python projects are easily understood and similarly constructed, regardless of who originally wrote it.

Code is about understanding what the code says, how it's piece fits into the larger puzzle, and knowing the estimation and effect of each addition or correction.

Python is almost like pseudocode.

Like english, it makes sense immediately. The characters and expressions used sometimes mathematical, but logic behind the meaning clear.

Go can be used to replace existing Python projects which work just fine in 90% of cases, but you've grown to a scale in which the 10% becomes difficult to reliably service.

There are no classes in Go. This might seem crazy for an enterprise ready language, but this is by language design choice, not language immaturity.

Instead of classes in Go, you have interfaces and structs. Structs are collections of strongly declared types, which can also include interfaces. Interfaces are a collection of structs, or a method doing one thing.

Go by design, encourages a composition pattern approach to object oriented programming rather than an initially elegant, but often times eventually complex, class inheritance hierarchy. 

Instead of thinking about all the different types of cars a vehicle can be, design your vehicle so it can be easily used in ways you didn't think of - such as a bike. Instead of defining a base class with an engine and what your idea of 'vehicle' means, design 'vehicle' to mean a collection of individual parts assembled together that serve a specific purpose.

Design 'engine' as a method to propel an object forward, rather than a combustable motor.

This forces you to design methods and functionality so that your methods do one and one thing only.

Unix environments follow the philosophy of doing one thing only and one thing well. This allows the use of individual commands which do one thing, to be chained together with other commands through pipes "|" accepting each other's inputs and outputs until the final result is returned.

The road of software project estimation often meanders when over confidence on how easy you think a solution is, encounters a road block in which your original design did not anticipate. Maybe this special case can be accounted for easily, but other times, it may require a complete change in the underlying design.

Being able to rapidly discover what those edge cases are, and being able to modify your project to account for it, rather than having to refactor a complex class hierarchy, allows you to focus on rapidly iterating and figure out ‘what works’ right now.

Like a simple command, if your software library, method, or program just does 'one thing and one thing well', it can easily be utilized without the implementor having to be aware of the underlying details.

Go is a strongly type language. This means that variables in Go must be declared as to what type they are. In an interpreted dynamic language like Python, the type is assumed to be the type of the first value you assigned to it, so you do not repeat yourself, and can crank out a feature without to much plumbing.

At first, it seems the extra step of strongly typing things is unnecessary and annoying. However, once a project grows to a certain size, there’s probably going to be some code somewhere at a random place that checks type and casts it into something else, or gnarly conditional branches in the code based off of handling different data structure types.

Describing the structures that your method accepts as input and the type of result it will always return, forces you to think visually how all the individual structures of your program fit together - like lego blocks with clearly defined edges that click and hold firmly in place. 

Visualize the data structure that should be returned for a new method first, and work backwards from there to figure out the implementation details.

Things like auto multi core distribution for threads which are many times more memory efficient and performant than python threads, true concurrency, near C like performance, and passing variables by pointers rather than by copying the values result in exponential performance gains once you hit a certain scale.

While a few milliseconds may seem insiginficate, at 30,000 writes / requests to a database or service per second, those few milliseconds add up.

A real world example: http://highscalability.com/blog/2014/5/7/update-on-disqus-its-still-about-realtime-but-go-demolishes.html

If you are a python / ruby / node web dev, you are familiar with the clown fiesta that is maintaining large amounts of dependencies between different environments.

In Go, you simply type in go [program-name-here] and a binary is compiled for you to run on any operating system. The deployment method is to simply to copy / download the binary and run.

While the languages themselves might be different, both follow a similar design philosophy of simplicity and practicality. The cross over between the two feels natural. The mental cost switching context between them, cheap.

Knowing them both very well allows you to fulfill two very important and distinct stages of a product: Rapidly implement an idea to test the market adoption, and once the 10% edge cases crop up when certain scales are reached, implement the performance critical parts in Go where needed.
