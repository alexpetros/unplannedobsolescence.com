+++
title = "Why Insist on a Word"
description = "On picking your pedantry battles."
date = 2025-02-03
+++

A central concept to HTML, and hypertext theory more generally, is something called Representational State Transfer, a.k.a. REST.
Over at htmx, a lot of the [writing we do](https://htmx.org/essays) is based on REST theory.

[REST is a widely misunderstood term](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/),
and if you point that out to people, you will be told, repeatedly and sometimes quite irately: who cares?
REST has a new meaning now—use words the way people understand them and spare us the lecture.

<!-- more -->

That criticism is compelling—who among us isn't a little [descriptivist](https://en.wikipedia.org/wiki/Linguistic_description) at heart—but sometimes the original, more precise meaning of a word is necessary to communicate something that the more common meaning can't capture.
To move hypertext forward, we have to build on the best work of our predecessors in the field, and that's impossible to do without engaging with what they said and how they said it.

So here's what REST is, and why it matters that we call it that.

<aside>
A lot of my readers are also htmx blog readers, which has lots of REST explainers.
Feel free to <a href="#rest-is-an-intellectual-heritage">skip to the next section</a> if you already feel comfortable with the concept.
</aside>

## One more (short) REST explainer

REST stands for "Representational State Transfer."
It's an academic term from [Roy Fielding's PhD dissertation](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm), describing the fundamental constraints that, in Fielding's view, made the World Wide Web a successful distributed system.
Web browsers don't _always_ follow his constraints ([Fielding is not a fan of cookies](https://ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm#sec_6_3_4_2)), but for the most part they do, and the thesis explains why that works.

Here are the main constraints that make the web RESTful:

* A client-server architecture
* Stateless requests; the client sends all relevant information each time
* The server can specify whether a response is cacheable
* The client and server communicate using a uniform interface

The first three are pretty intuitive.
The last one is craaaaazzyyyyy.
It means that the server can't control which client you're going to use to talk to it, so it has to describe its interface using some standard grammar.
On the web, that's HTML.

<aside>
As a counter-example: think about how games like League of Legends work.
You download a client application (the game) on your computer, and that client connects to the LoL servers.
The creator of the game controls both the server and the client used to connect to it.
See also: apps on your phone.
</aside>

That probably seems natural to you now, because HTML exists and it works, but at the time it was revolutionary to imagine that not only would one markup language would be sufficient to describe completely different applications—like banking or mapping or email—but that the server would describe what the user is allowed to do, from scratch, on *every single network request*.

Let's re-use the bank account example from ["How Did REST Come To Mean The Opposite of REST?"](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/#the-crux-of-rest-the-uniform-interface-hateoas) by Carson Gross.

```html
<!DOCTYPE html>
<title>Alex's Bank Account</title>

<div>Account number: 12345</div>
<div>Balance: $100.00 USD</div>
<div>Links:
    <a href="/accounts/12345/deposits">deposits</a>
    <a href="/accounts/12345/withdrawals">withdrawals</a>
    <a href="/accounts/12345/transfers">transfers</a>
</div>
```

That's the HTML page for a bank account.
The browser, upon receiving that, will render the following:

<iframe src="./bank-account.html" width=300 height=200>
</iframe>

Notice how the API response describes __the current state__ (your bank balance) and __what actions the user can take to alter that state__ (the links) in a format that the user can understand and interact with.
If you click on one of those links, it will show you a new page, with new data, and new actions.

No client-side state is necessary, because [all the state is in the HTML you just got](https://htmx.org/essays/hateoas/).
Make a new request and get new state, all represented as hypertext: that's Representational State Transfer.
Opa!

This is in contrast with a JSON API (commonly, incorrectly, called RESTful), which is not self-describing:

```json
{
    "account_number": 12345,
    "balance": {
        "currency": "usd",
        "value": 100.00
     },
     "status": "good"
}
```

Why isn't that self-describing?
Well, here's what the browser will render if you send that.

<iframe src="./json-api.json" width=300 height=200>
</iframe>

The client (the browser) doesn't know what to do with any of that information.
It's just data—it doesn't encode any actions.
Not only is the client now responsible for turning this data into something the user can interact with, it's no longer resilient to the API changing;
if an API changes, the client also has to change to handle it.

Contrast that with the HTML response, where the HTML could change and the browser would simply render the new HTML into something humans are capable of interacting with, no questions asked.
That's what it means for the API to be self-describing.

<aside>
A lot of people also really don't like calling HTML responses "APIs," because it's meant to be consumed by humans, not computers.
I'm actually a lot more sympathetic to this confusion, but that's how it's used in the literature and I don't have a better term for it at this time.
</aside>


## REST is an intellectual heritage

In the year 2000, Roy Fielding publishes his dissertation.
In the year 2022, Carson Gross writes a blog post about how no one understands Roy Fielding's dissertation.
What happens in the intervening 22 years?

Well, lots of people write APIs (like the JSON example above) that aren't RESTful but call them REST.
This prompts Fielding to [write the following on his blog](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven), in 2008:

> I am getting frustrated by the number of people calling any HTTP-based interface a REST API. [...]
> What needs to be done to make the REST architectural style clear on the notion that hypertext is a constraint?
In other words, if the engine of application state (and hence the API) is not being driven by hypertext, then it cannot be RESTful and cannot be a REST API.
Period. Is there some broken manual somewhere that needs to be fixed?

I don't know, Roy, maybe there is a broken manual.
Maybe you needed to explain this somewhere other than _a PhD dissertation_, a famously non-approachable format.

Fielding [publishes a response to this criticism](https://roy.gbiv.com/untangled/2008/specialization) just four days later:

> So, when you find it hard to understand what I have written, please don’t think of it as talking above your head or just too philosophical to be worth your time. I am writing this way because I think the subject deserves a particular form of precision. Instead, take the time to look up the terms. Think of it as an opportunity to learn something new, not because I said so, but because it will do you some personal good to better understand the depth of our field. Not just the details of what I wrote, but the background knowledge implied by all the strange terms that I used to write it.
>
> Others will try to decipher what I have written in ways that are more direct or applicable to some practical concern of today. I probably won’t, because I am too busy grappling with the next topic, preparing for a conference, writing another standard, traveling to some distant place, or just doing the little things that let me feel I have [...] earned my paycheck.

Two things stick out to me about this excerpt.
The first is that it is wildly pompous.
The second is that it is correct.

Now, obviously, it is ridiculous to complain that no one understands you and also explicitly disavow the work of explaining it at a more approachable level.
But if he is in fact speaking exclusively to hypermedia experts, then he's right that using the terms precisely is necessary to convey those concepts correctly.

Fielding concludes:
> Fortunately, there are more than enough people who are specialist enough to understand what I have written (even when they disagree with it) and care enough about the subject to explain it to others in more concrete terms.

And he's right, that happened too.
Leonard Richardson incorporated the ideas from Fielding's thesis into a talk called ["Justice Will Take Us Millions Of Intricate Moves,"](https://www.crummy.com/writing/speaking/2008-QCon/) which broke the ideas down into "a formal vocabulary for talking about what you get when you put HTTP, URIs, and HTML together".
Martin Fowler saw that talk and explained it in a blog post, formalizing the ["Richardson Maturity Model."](https://martinfowler.com/articles/richardsonMaturityModel.html)
Carson Gross read Fowler's blog and used the Richardson Maturity Model to explain [how REST came to mean the opposite of REST](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/).

If we decided that REST was a lost cause, and chose some other term to describe that set of ideas, not only would we have to re-explain a bunch of things, we'd deny our successors access to the intellectual heritage that produced the knowledge we're trying to build on.
How are we supposed to stand on the shoulders of giants whose names we don't know?

## REST is worth building on

The HTML we have today works well enough to build rich, interconnected information systems, with basic interactive elements.
And REST remains very useful for evaluating the quality of those systems.

<aside>
Generally speaking, reliable web applications stick as closely to hypertext APIs as possible, because self-description is inherently more resilient than coupling.

</aside>

But the web has evolved to require more complex interactivity.
I firmly believe it is possible to build that with architectures that are just as sturdy as plain old Web 1.0 sites are.
Doing so just requires improving on HTML, and improving on REST.

For instance, REST has [little to say](https://alexanderpetros.com/triptych/form-http-methods#ref-27) about the purpose of HTTP methods like "put" and "post."
But I think HTTP methods are <em>very</em> important, because
[adding additional HTTP methods lets you describe additional actions on the same resource](https://alexanderpetros.com/triptych/form-http-methods#application-server-permissions).
That makes it possible to build more complex applications with simple URL schemas, adding to the self-descriptive power of the hypertext while preserving REST's core constraints.

So I'm working on that.
I'm reading the web specs, the theses, and the blog posts of the great web thinkers, learning what they learned, and trying to add on to it.
I think that I live in the generation where it becomes possible to use those principles to make [web services as durable as bridges](@/talks/building-the-hundred-year-web-service.md).
We'll see.

But if I'm wrong, well, at least I'm using words that make my work easier to find in the future, whenever the time is right.

*Thanks to Carson Gross for his feedback on a draft of this article.*

# Notes

* It genuinely makes me laugh how many times Carson has written a REST explainer
([2016](https://intercoolerjs.org/2016/01/18/rescuing-rest.html),
[2020](https://intercoolerjs.org/2020/01/14/taking-html-seriously),
[2021](https://htmx.org/essays/rest-explained/),
[2022](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/),
[2023](https://htmx.org/essays/hateoas/)).
* "REST was good idea but it doesn't work in practice" is a very funny talking point to me because RESTful web practices were wildly successful.
It's the web!
REST is literally just regular websites.
REST has a lot of room to improve as an accessible set of guidelines for evaluating the efficacy of distributed hypertext systems, but that's what I'm trying to change.
* I do believe, unfortunately, that the [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html) impedes our ability to move forward with REST, since it blesses JSON APIs with a sort of "mostly REST" status (Level 2) that is not terribly useful (it's just a JSON API); all of the interesting properties of *representational* state transfer come with the hypermedia representation (Level 3).
Fowler more or less acknowledges this in the conclusion.


