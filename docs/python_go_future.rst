Why python and go is the future
=======

When comparing languages, it’s easy to compare each one’s features and capabilities on paper.

Lost in this comparison are what you gain as a collaborative team by the simplicity and maintainability of a language favoring simplicity over cleverness.

Restrictions like enforced whitespace as part of the code logic, and in most cases, only one way to do something, mean that most Python projects are easily understood and similarly constructed, regardless of who originally wrote it.

Code is about understanding what the code says, how it fits into the bigger picture, and knowing the estimation and effect of each additionally feature or fix.

Python is almost like pseudocode.

Like english. It makes sense immediately. The characters and expressions used sometimes mathematical, but logic behind the meaning clear.

Go can be used to replace existing Python projects which work just fine in 90% of cases, but you've grown to a scale in which the 10% becomes difficult to reliably service.

There are no classes in Go. This might seem crazy for an enterprise ready language, but this is by language design choice, not language immaturity.

Instead of classes in Go, you have interfaces and structs. Structs are collections of strongly declared types, which can also include interfaces, and interfaces are a collections of structs or methods

Go by design, encourages a composition pattern approach rather than an elegant class inheritance hierarchy. 

Instead of thinking about all the different types of cars a vehicle can be, design your vehicle so it can also be easily used as a bike.

This forces you to design methods and functionality so that your methods do one and one thing only.

Unix environments follow the philosophy of doing one thing only and one thing well, allows the use of individual commands which do one thing, to be chained together accepting each other's intputs and outputs until the final result is given.

The meandering road of software project estimation and the over confidence on how easy you think a solution is, seems to always miss the special case in which something happens or was not considered. 

Being able to rapidly discover what those edge cases are, and being able to modify your project to account for it, rather than having to refactor your class hierarchy, allows you to focus on rapidly iterating and figure out ‘what works’.

Your library does 'just this one thing' and can easily be utilized without the implementor having to be aware of any heiarchy.

Go is a strongly type language. This means that variables in Go must be declared as to what type they are, and in Python, the type is assumed to be the type of the first value you assigned to it, so you do not repeat yourself.

At first, it seems the extra step of strongly typing things is unnecessary and annoying, but eventually at a certain scale, if you use a dynamic language such as Python or Javascript, there’s probably going to be some code somewhere at a randomly place that checks type and casts it into something else or branches off if a conditional is met.

Describing the structures that your method accepts as input and the type of result it will always return, forces you to think visually how all the individual structures of your program fit together like lego blocks with clearly defined edges and sizes. 

Python is the malleable, soft clay that you mold your idea with. You work out the final form adjustment after adjustment. You can then quickly see if your finished product will have outside approval and fullfill a need.

If it’s discovered that the tool needs to be more durable, then use Go to cast the same form in granite.

Things like auto multi core threading on threads which are many times more memory proficient and performant than Python’s can be greatly beneficial at a certain scale.

Being able to compile your program, and deploy it by simply copying the binary over and running it, is a huge relief compared to the virtual / system environment jungle of a sizable multi project interpreted language deploy.

While the languages themselves might be different, both follow a similar design philosophy of simplicity and practicality. The cross over between the two feels natural. The mental context switching cost cheap.

Knowing them both very well allows you to fullfill two different stages of a startup: Rapidly implement an idea to test the market, and once the 10% edge cases crop up when certain scales are reached, implement the performance critical parts in Go as needed.
