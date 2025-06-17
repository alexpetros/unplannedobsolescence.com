+++
title = "The Server Doesn't Render Anything"
description = ""
date = 2025-06-17

[extra]
hidden = true
+++


When I advise people on how they should structure a web service, I always start from the same place:
make a server that responds to HTTP requests with HTML text.
[That is the most durable, cost-effective, and user-friendly way to build a web service](@/blog/hard-page-load/index.md).
Most web services should be built this way absent an excellent reason not to.

Upon hearing this, present-day web developers often reply "oh, you like server-side rendering," to which I usually wince and answer "more or less."
You have to pick your battles when chipping away at a decade of mis-education.
At least people know what I'm talking about.

But "server-side rendering" is a horrible term.
It implies that the server is not just doing *more* work, but doing *hard* work, work that's best left to the experts.
None of this is true.
You, too, can do server-side "rendering," with essentially no effort, in whatever programming language you prefer.

Once you understand that, you'll start to see the web the way I do: as the simplest, easiest, and most powerful interface for computation ever created.

## HTML is just text

Wherever you can print text, you can make HTML.

Here's an example in Python, which extends Python's built-in HTTP server so that it responds to every GET request with the same text:
`<h1>Python webpage!</h1>`


```python
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBPAGE = "<h1>Python webpage!</h1>\n"

class HTMLServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(WEBPAGE))

webServer = HTTPServer(("localhost", 8080), HTMLServer)
print("Server running at http://localhost:8080")
webServer.serve_forever()
```

This would be [even simpler](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application) with [flask](https://flask.palletsprojects.com), but I'm trying to make a point here by using a basic server without any dependencies.
There's no magic that makes HTML text become HTML code.
We didn't even set the [`Content-Type`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type) header to `text/html`.

<aside>It's good to set the Content-Type header, though, so the browser doesn't have to guess.</aside>

Run that script and then try interacting with the server via `curl`.
You'll see that it's just text.

```
$ curl localhost:8080
<h1>Python webpage!</h1>
```

What if we open `http://localhost:8080` in a browser?
Instead of showing plain text, the browser will render that HTML into something more dynamic.
The `<h1>` tags are gone and the remaining text is big and bold.

<iframe srcdoc="<h1>Python webpage!</h1>"></iframe>


To incorporate color and a fun font, like we did in ["The Best 'Hello World' in Web Development,"](@/blog/best-hello-world-web-development/index.md) simply add a `<style>` tag to the string.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBPAGE = """
<style>
body {
  background-color: lightblue;
  font-family: 'Comic Sans MS', cursive;
}
</style>
<h1>Python webpage!</h1>
"""

# Server code omitted for clarity

```

Now `curl`ing the endpoint will show the additional style tag, and the browser will render the HTML with a nice blue background and a comic sans font.

<iframe srcdoc="<style>body { background-color: lightblue; font-family: 'Comic Sans MS', cursive; }</style><h1>Python webpage!</h1>"></iframe>

## The browser does the rendering

Did you notice that I used the word "render" twice in the previous section?
Both times to refer to actions the browser took, namely the transformation of this text—

```
<style>
body {
  background-color: lightblue;
  font-family: 'Comic Sans MS', cursive;
}
<h1>Python webpage!</h1>
```

—into a webpage.

<iframe srcdoc="<style>body { background-color: lightblue; font-family: 'Comic Sans MS', cursive; }</style><h1>Python webpage!</h1>"></iframe>

Even something as "simple" as rendering header text on a blue background is a very complicated process.
[Chapter 3](https://browser.engineering/text.html) of Panchekha & Harrelson's excellent book, <a href="https://browser.engineering/"><cite>Web Browser Engineering</cite></a>, has a basic introduction to the steps involved.
Let's drop in on the part where they talk about [measuring text](https://browser.engineering/text.html#measuring-text):

> Remember that `bi_times` is size-16 Times: why does `font.metrics` report that it is actually 19 pixels tall?
> Well, first of all, a size of 16 means 16 points, which are defined as 72nds of an inch, not 16 pixels, which your monitor probably has around 100 of per inch.
> Those 16 points measure not the individual letters but the metal blocks the letters were once carved from, so the letters themselves must be less than 16 points.
> In fact, different size-16 fonts have letters of varying heights.

Okay.

Just getting a couple letters on the page requires layout math that most web developers have never even considered.
All this is learn-able (that's what the book is for), but web rendering is astoundingly complex.
Imagine trying to implement [kerning](https://en.wikipedia.org/wiki/Kerning);
instead, you get it for free.

The reason not to call HTML text generation "rendering" is because rendering really *is* a difficult, complicated problem, it's just not one the website author ever has to think about.
The experts have taken care of it and put the required software in every person's pocket.

All the website author has to do is print text surrounded by tags—no math required.

## Expressing data as HTML

What is the appropriate framing for this concept, if not "server-side rendering?"
It's text generation, yes, but more precisely: we are expressing our data as HTML text.
Not only is this technique universally available without specialized tools, it's kind of fun!

```python
boroughs = [
  "The Bronx",
  "Manhattan",
  "Brooklyn",
  "Queens",
  "Staten Island"
]

# Using simple string operations,
# we can express this list as HTML
LIST = "<li>".join(boroughs)
WEBPAGE = "<h1>NYC Boroughs</h1><ul><li>" + LIST + "<ul>"

```

<aside>Notice that I didn't include the closing &lt;/li&gt; tags. HTML doesn't actually require that you close list items, an affordance which is often discouraged but makes list items much easier to generate programatically.</aside>

Manipulating strings is Coding 101.
Learn a couple HTML elements and you can use basic string operations to build an interactive view of whatever your code accomplishes.
The resulting text isn't very pretty outside the browser, but inside the browser, it gets the job done.

```html
<h1>NYC Boroughs</h1><ul><li>The Bronx<li>Manhattan<li>Staten Island<li>Brooklyn<li>Queens</ul>
```

<iframe style="height: 250px" srcdoc="<h1>NYC Boroughs</h1><ul><li>The Bronx<li>Manhattan<li>Staten Island<li>Brooklyn<li>Queens</ul>"></iframe>

You could, of course, choose to express the same dataset as JSON, using the same techniques.

```python
boroughs = [
  "The Bronx",
  "Manhattan",
  "Brooklyn",
  "Queens",
  "Staten Island"
]

LIST = '","'.join(boroughs)
WEBPAGE = '{ "nyc_boroughs": ["' + LIST + '"] }'

# Server code omitted for clarity
```

Although, this doesn't really accomplish all that much, because [JSON doesn't have hypermedia controls](@/blog/why-insist-on-a-word/index.md#one-more-short-rest-explainer).
But it's at least possible, if you need quick and dirty JSON output and don't have access to a JSON library for some reason.

<aside>Obviously you should use python's JSON module for this task, but I have occasionally done stuff like this for personal scripts in bash or awk. It's good to remember you can!</aside>

```json
{ "nyc_boroughs": ["The Bronx","Manhattan","Brooklyn","Queens","Staten Island" ] }
```

The point is not that you should (necessarily) be generating HTML or JSON via string manipulation, it's they both operate at similar levels of difficulty and abstraction;
I object to the term "server-side rendering" because it implies otherwise.

To start "server-side rendering" all you have to do is format your data as HTML, and return that from the server.

## So what do we call this?

My preferred term is "HTML APIs."
Developers are familiar with JSON APIs, and an HTML API works exactly the same way, only it returns HTML, instead of JSON.
"HTML responses" works too.

(HTML APIs are also REST APIs, but if you say "REST APIs" then you'll have to send your coworkers [a second article](@/blog/why-insist-on-a-word/index.md), so save that one for later.)

A lot of people get hung up on the idea that HTML can't be an API (Application Programming Interface), because HTML is meant to be read by humans and APIs are meant to be read by computer software.
But that isn't *quite* true.

Take a look at the NYC Boroughs list in both JSON and HTML, side-by-side.

```html,name=HTML
<h1>NYC Boroughs</h1>
<ul>
  <li>The Bronx
  <li>Manhattan
  <li>Staten Island
  <li>Brooklyn
  <li>Queens
</ul>
```

```json,name=JSON
{
  "nyc_boroughs": [
    "The Bronx",
    "Manhattan",
    "Brooklyn",
    "Queens",
    "Staten Island"
  ]
}
```

Neither of these is actually intended to be read by the end-user. The end-user is supposed to see a formatted list!

<iframe style="height: 250px" srcdoc="<h1>NYC Boroughs</h1><ul><li>The Bronx<li>Manhattan<li>Staten Island<li>Brooklyn<li>Queens</ul>"></iframe>

HTML is a hypermedia format, so it contains structured data *and* a standard interface that the browser can render.
JSON APIs only encode the data; they lack the representation.
Using an HTML API doesn't move complexity from the client to the server—it eliminates the less-useful JSON representation altogether.


From this perspective, the HTML API is a software-to-software communication protocol:
the software that the server is talking to is the **user's browser**, instead of a client-side JavaScript application.
The user's browser reads the HTML API, and renders it as a Graphical User Interface (GUI).

## Making real websites

This is comically basic stuff, but you have to understand: a decade of developers were taught that when you want to make a real website, you need to install React.
The message was that websites are hard, and React is taking care of the hard parts for you.
Serious developers use React.

Websites are not hard.
There are many pitfalls to building a dynamic web service with logins, databases, user-generated content, and all that—this is a profession, after all—but the website part, the expression of your server's data as an interface in the user's browser, is quite easy.
You really can do it with almost no specialized tools.

It's important to understand this.
Not because of gimmicks like building a `<ul>` with string joins, but because it enables you to deploy simpler tools to accomplish more powerful things.

<aside>The gimmicks are fun too.</aside>

Instead of React, try HTML APIs with a [template engine](https://htmx.org/essays/template-fragments/#known-template-fragment-implementations).
They're [universally available](https://htmx.org/essays/hypermedia-on-whatever-youd-like/) (often with semantics that fit your [favorite](https://github.com/nektro/zig-pek) [niche](https://aantron.github.io/dream/#templates) [language](https://edicl.github.io/html-template/)),
have [helpful affordances](https://htmx.org/essays/template-fragments/) for API code re-use,
and are equipped with [secure defaults for user-generated content](https://htmx.org/essays/web-security-basics-with-htmx/#always-use-an-auto-escaping-template-engine).
And the dramatically simpler technology is dramatically easier to debug.

After all, they're basically just doing string joins.

# Notes

* In experience, React advocates are quite defensive about the idea that anyone has ever suggested React was necessary for use-cases where a simple `<form>` would do.
I don't want to tilt at strawmen, so I'll just say that I'm aware of that perspective, and I don't think it's true.
* All the examples in this blog are static text, but if you want interactivity: `<a>`, `<button>`, `<script>`, and so on.
* People who learned web development prior to ~2016 have no trouble with this concept. I usually just say "it's like Rails," or "it's Java Server Pages."
