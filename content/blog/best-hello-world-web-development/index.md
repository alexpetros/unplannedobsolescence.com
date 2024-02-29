+++
title = "The Best \"Hello World\" in Web Development"
description = "PHP is still one of the best ways to get started on the web."
date = 2024-02-29
+++

## The Classic Hello World
Here's how you make a webpage that says "Hello World" in PHP:

```php
Hello World
```

Name that file `index.php` and you're set. Awesome. <a href="./hello-world-v1.html">Version 1</a> of our website looks like this:

<iframe title="Hello World Page" width=300 height=200 src="./hello-world-v1.html">
</iframe>

Okay, we can do a little better. Let's add the HTML doctype and `<title>` element to make it a [legal HTML5 page](http://lofi.limo/blog/write-html-right), an `<h1>` header to give the "Hello World" some heft, and a `<p>` paragraph to tell our visitor where they are.

```php
<!DOCTYPE html>
<title>Hello, World!</title>
<h1>Hello, World!</h1>
<p>Welcome to Alex's website :)</p>
```

This is a complete webpage! If you host this single file at one of the many places available to host PHP code, it will show that webpage to everyone who visits your website. Here's <a href="./hello-world-v2.html">Version 2</a>:

<iframe title="Hello World Page" width=300 height=200 src="./hello-world-v2.html">
</iframe>

Now let's make [Version 3](./hello-world-v3.html) comic sans! And baby blue! We just have to add a style tag:

```php
<!DOCTYPE html>
<title>Hello, World!</title>
<style>
body {
  background-color: lightblue;
  font-family: "Comic Sans MS", "Comic Sans", cursive;
}
</style>
<h1>Hello, World!</h1>
<p>Welcome to Alex's website :)</p>
```

<iframe title="Hello World Page" width=300 height=200 src="./hello-world-v3.html">
</iframe>

Already our webpage has a little bit of personality, and we've spent just a couple minutes on it. At each step we could see the website in a browser, and keep adding to it. We haven't even used any PHP yet—all this is plain old HTML, which is much easier to understand than PHP.

This is the best "Hello World" in web development, and possibly all of programming.
## Contemporary Hello Worlds

The thing that first got me interested in PHP in the first place is a comment that Ruby on Rails creator [David Heinemeier Hansson made on the "CoRecursive" podcast](https://corecursive.com/045-david-heinemeier-hansson-software-contrarian/), about PHP's influence on Rails:

> \[...] the other inspiration, which was from PHP, where you literally could do a one line thing that said, “Print hello world,” and it would show a web page. It would show Hello World on a web page. You just drop that file into the correct folder, and you were on the web \[...] I think to this day still unsurpassed ease of Hello World.

He's right—this is an unsurpassed ease of Hello World. It is certainly not surpassed by Ruby on Rails, the ["Getting Started" guide](https://guides.rubyonrails.org/getting_started.html) for which not only requires installing ruby, SQLite, and Rails itself, but also has you run an initialization command (`rails new blog`) that creates a [genuinely shocking number of files and directories](view-source:https://guides.rubyonrails.org/getting_started.html#creating-the-blog-application):

```
$ rails new blog 2>&1 >/dev/null
$ tree -L 2 blog
blog
├── Dockerfile
├── Gemfile
├── Gemfile.lock
├── README.md
├── Rakefile
├── app
│   ├── assets
│   ├── channels
│   ├── controllers
│   ├── helpers
│   ├── javascript
│   ├── jobs
│   ├── mailers
│   ├── models
│   └── views
├── bin
│   ├── bundle
│   ├── docker-entrypoint
│   ├── importmap
│   ├── rails
│   ├── rake
│   └── setup
├── config
│   ├── application.rb
│   ├── boot.rb
│   ├── cable.yml
│   ├── credentials.yml.enc
│   ├── database.yml
│   ├── environment.rb
│   ├── environments
│   ├── importmap.rb
│   ├── initializers
│   ├── locales
│   ├── master.key
│   ├── puma.rb
│   ├── routes.rb
│   └── storage.yml
├── config.ru
├── db
│   └── seeds.rb
├── lib
│   ├── assets
│   └── tasks
├── log
│   └── development.log
├── public
│   ├── 404.html
│   ├── 422.html
│   ├── 500.html
│   ├── apple-touch-icon-precomposed.png
│   ├── apple-touch-icon.png
│   ├── favicon.ico
│   └── robots.txt
├── storage
├── test
│   ├── application_system_test_case.rb
│   ├── channels
│   ├── controllers
│   ├── fixtures
│   ├── helpers
│   ├── integration
│   ├── mailers
│   ├── models
│   ├── system
│   └── test_helper.rb
├── tmp
│   ├── cache
│   ├── local_secret.txt
│   ├── pids
│   └── storage
└── vendor
    └── javascript

38 directories, 35 files
```

Of course, Rails is doing a lot of stuff for you! It's setting up a unit test framework, a blog content folder, a database schema, whatever `credentials.yml.enc` is,  and so on. If I wanted all of that, then Rails might be the way to go. But right now I want to make a webpage that says "Hello World" and start adding content to it; I should not have to figure out what a `Gemfile` is to do that.

As a reminder, here's the directory structure for our "Hello World" in PHP:

```
$ tree -L 2 php-project
php-project
└── index.php

1 directory, 1 file
```

My goal here isn't to rip on Ruby on Rails—although, is a Dockerfile really necessary when you're just "Getting Started"?—but to highlight a problem that is shared by basically every general-purpose programming language: using Ruby for web development requires a discomfiting amount of scaffolding.

Over in the Python ecosystem, one of the first web development frameworks you will encounter is [flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/), which is a much lighter-weight framework than Rails. In flask, you can also get the "Hello World" down to one file, sort of:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World"
```

Even here, there are a ton of concepts to wrap your head around: you have to understand basic coding constructs like "functions" and "imports", as well as Python's syntax for describing these things; you have to figure out how to install Python, how to install Python packages like `flask`, and how to run Python environment management tool like `venv` (a truly bizarre kludge that Python developers insist isn't that big of a deal but is absolutely insane if you come from any other modern programming environment); I know we said one file earlier, but if you want this work on a server you're going to have to document that you installed flask, using a file like `requirements.txt`; when you start to add more content you're going to have to figure out how to do multiline strings; and what's going with the inscrutable `app = Flask(__name__)`?

If any of these concepts aren't arranged properly—in your head and in your file—your server will display nothing.

By contrast, you don't have to know a *thing* about PHP to start writing PHP code. Hell, you barely have to know the command line. If you can manage to install and run a PHP server this file will simply display in your browser.

And the file itself:

```php
Hello World
```

You didn't have to think about dependencies, or routing, or `import`, or language constructs, or any of that stuff. You're just running PHP. And you're on the web.

## The Importance of Time-To-Hello-World

The Time-To-Hello-World test is about the time between when you have an idea and when you are able to see the seed of its expression. That time is crucial—it's when your idea is in its most mortal state.

Years before my friend [Morry](https://wttdotm.com/) really knew how to code, he was able to kludge together enough PHP of make a website that tells you whether your IP address has 69 in it. It basically looks like this:

```php
<!DOCTYPE html>
<title>Does my IP address have 69 in it?</title>
<h1>Does my IP address have 69 in it?</h1>
<?php
if(strpos($_SERVER['REMOTE_ADDR'], '69') !== false) {
  echo "Nice";
} else{
  echo "Not Nice";
}
?>
```

You may or may not find that to be a compelling work of art, but it would not exist if spinning up Flask boilerplate were a requirement to do it. And he had taken a CS course in basic Python; the experience of making a *website* in PHP was just that much better. This turned out to be the first in a long line of internet art projects, some of which [we made together](https://wemakeinter.net/) and some of which [he did on his own](https://github.com/wttdotm?tab=repositories).

[doesmyipaddresshave69init.com](https://doesmyipaddresshave69init.com/) is a dumb idea for a website. But sometimes dumb ideas evolve into good ideas, or they teach you something that's later used to make a good idea, or they just make you chuckle. Or none of the above. The best thing about websites is that you don't have to justify them to anyone—you can just make them. And PHP is still the fastest way to make a ["dynamic"](https://blog.wesleyac.com/posts/no-static-websites) website.

I recently made a little [invoice generator with a local browser interface](https://github.com/alexpetros/invoice-generator) for my freelance business. It works great! It's got a homepage with a list of my generated invoices, a `/new.php` route for making a new one, and `/invoices/generated/{invoice_id}` routes to view each invoice in a printable format.

I don't find the boilerplate required to make a [RESTful web service](https://intercoolerjs.org/2016/01/18/rescuing-rest.html) in NodeJS especially onerous—I have a pretty good system for it at this point. But PHP brings the time-to-hello-world down tremendously. I just don't think this would have gotten off the ground if I had to setup ExpressJS, copy my router boilerplate, make 2 files for each route (the template and the javascript that serves it), and do all the other things I do to structure web-apps in Node. Instead, I got all that stuff built-in with vanilla PHP, and that will presumably work for as long as PHP does. I didn't even have to touch [the package manager](https://getcomposer.org/).

 A lot of people have the attitude that writing vanilla code (and vanilla PHP especially) is never okay because you need secure-by-default frameworks to ensure that you don't make any security mistakes. It clearly true that if you are building professional software you should be aware of [the web security model](https://htmx.org/essays/web-security-basics-with-htmx) and make informed decisions about the security model of your application; not everyone is building professional software.



Relatedly, one route to becoming is a software professional is to have a delightful experience as a software amateur.

I believe that more people should use the internet not just as consumers, but as creators (not of *content* but of *internet*). There is a lot of creativity on the web that can be unlocked by making web development more accessible to artists, enthusiasts, hobbyists, and non-web developers of all types. The softer the learning curve of getting online, the more people will build, share, play, and create there.

Softening the learning curve means making the common things easy and not introducing too many concepts until you hit the point where you need them. Beginners and experts alike benefit.

# Notes

*Thanks to [Nathaniel Sabanski](https://github.com/gnat) and [Al Sweigart](https://inventwithpython.com/) for their feedback on a draft of this blog.*

- My example invoice generator is not meant to be put online, so it doesn't escape text to prevent XSS attacks, or do the other [web security basics](https://htmx.org/essays/web-security-basics-with-htmx).
- Admittedly, some of PHP's design decisions really lend themselves to insecure code. For starters, they really need [a short echo tag](https://www.php.net/manual/en/language.basic-syntax.phptags.php) that auto-escapes.
- I'm probably not going to start doing professional work in PHP—the language is interesting but too kludgy, and the value of the defaults diminishes as a greater percentage of the code becomes business logic—but I am definitely going to do more web art in PHP. I especially like how compact and shareable it can be, which has tremendous value for certain types of code.
- PHP is also missing a bunch of stuff that I consider really important, that makes pre-processing your requests close to mandatory. Big ones for me in include removing the `.php` file extension from the URL, and PUT/DELETE support.
- Yes, I'm aware of well-known opinion-haver David Heinemeier Hansson's other opinions. Some of them are right and some of them are wrong.
- More languages should have a "thing" that they are "for." Maybe I'll write about how awk rekindled my love for programming next.
