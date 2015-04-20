Why Python and Go is the Future
=======

When comparing languages, it’s easy to compare each one’s features and capabilities on paper.

Lost in this comparison is what you gain as a collaborative team by the efficiency and maintainability of a language favoring simplicity over cleverness.

Restrictions like enforced whitespace as part of the code logic, and in most cases, only one way to do something, mean that most Python projects are easily understood and similarly constructed, regardless of who originally wrote it.

Code is about understanding what the code says, how it fits into the bigger picture, and knowing the estimation and effect of each additionally feature or fix.

Python is almost like pseudocode.

Like english. It makes sense immediately. The characters and expressions used sometimes mathematical, but logic behind the meaning clear.

Go can be used to replace existing Python projects which work just fine in 90% of cases, but you've grown to a scale in which the 10% becomes difficult to reliably service.

There are no classes in Go. This might seem crazy for an enterprise ready language, but this is by language design choice, not language immaturity.

Instead of classes in Go, you have interfaces and structs. Structs are collections of strongly declared types, which can also include interfaces. Interfaces are a collection of structs or methods.

Go by design, encourages a composition pattern approach rather than an elegant class inheritance hierarchy. 

Instead of thinking about all the different types of cars a vehicle can be, design your vehicle so it can be easily used in ways you didn't think of - such as a bike.

This forces you to design methods and functionality so that your methods do one and one thing only.

Unix environments follow the philosophy of doing one thing only and one thing well. This allows the use of individual commands which do one thing, to be chained together with other commands through pipes "|" accepting each other's intputs and outputs until the final result is returned.

The road of software project estimation and often meanders when over confidence on how easy you think a solution is, encounters something in which your original design did not anticipate. Maybe this special case can be accounted for easily, but other times, it may require a complete change in the underlying design.

Being able to rapidly discover what those edge cases are, and being able to modify your project to account for it, rather than having to refactor an initially elegant but often times overly-complex class hierarchy, allows you to focus on rapidly iterating and figure out ‘what works’ right now.

Like a simple command, if your software library, method, or program just does 'one thing and one thing well', it can easily be utilized without the implementor having to be aware of the underlying details.

Go is a strongly type language. This means that variables in Go must be declared as to what type they are. In an interpretated dynamic language like Python, the type is assumed to be the type of the first value you assigned to it, so you do not repeat yourself, and can crank out a feature without to much plumbing.

At first, it seems the extra step of strongly typing things is unnecessary and annoying, but eventually at a certain project scale, if you don't use strong typing, there’s probably going to be some code somewhere at a random place that checks type and casts it into something else or branches off if a conditional is met. 

Describing the structures that your method accepts as input and the type of result it will always return, forces you to think visually how all the individual structures of your program fit together like lego blocks with clearly defined edges and sizes that when used properly together, click and hold firmly in place. 

Think of python is the malleable, soft clay that you mold your idea with. You work out the final form from adjustment after adjustment. Your business logic is defined. The edge cases found. You can then quickly see if your finished product will have outside approval and fullfill a need.

If it’s discovered that the tool needs to be more durable, then use Go to cast your soft figurine, into a granite statue that can withstand the test of time.

Things like auto multi core threading on threads which are many times more memory proficient and performant than Python’s can be greatly beneficial at a certain scale. Near C like performance. Passing variables by pointers rather than by copying the values. These things add up exponentially when performance and scale matter.

Being able to compile your program and deploy it by simply copying the binary over and running it, is a huge relief compared to the virtual / system environment jungle of a sizable multi project dynamically interpreted application deploy.

While the languages themselves might be different, both follow a similar design philosophy of simplicity and practicality. The cross over between the two feels natural. The mental cost switching context between the two, cheap.

Knowing them both very well allows you to fullfill two very important and distinct stages of a product: Rapidly implement an idea to test the market, and once the 10% edge cases crop up when certain scales are reached, implement the performance critical parts in Go as needed.
