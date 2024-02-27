+++
title = "The Best \"Hello World\" in Web Development"
description = "PHP is still one of the best ways to get started on the web."
date = 2024-02-29
+++

Here's how you make a webpage that says "Hello World" in PHP:

```php
Hello World
```

Name that file `index.php` and you're set. Awesome.

Although browsers will display this file just fine, we should also probably add the HTML doctype and `<title>` element, to make it a [legal HTML5 page](http://lofi.limo/blog/write-html-right), and maybe toss in an `<h1>` to give the "Hello World" some heft.

```php
<!DOCTYPE html>
<title>Hello World</title>
<h1>Hello World</h1>
```

This is a complete webpage! If you host this single file at one of the many places available to host PHP code, it will show that webpage to everyone who visits your website.

This is the best "Hello World" in web development, and possibly all of programming.
## Contemporary Hello Worlds

The thing that first got me interested in PHP in the first place is a comment that Ruby on Rails creator (and well-known opinion-haver) [David Heinemeier Hansson made on the "CoRecursive" podcast](https://corecursive.com/045-david-heinemeier-hansson-software-contrarian/), about PHP's influence on Rails:

> \[...] the other inspiration, which was from PHP, where you literally could do a one line thing that said, “Print hello world,” and it would show a web page. It would show Hello World on a web page. You just drop that file into the correct folder, and you were on the web \[...] I think to this day still unsurpassed ease of Hello World.

He's right—this is an unsurpassed ease of Hello World. It is certainly not surpassed by Ruby on Rails, the ["Getting Started" guide](https://guides.rubyonrails.org/getting_started.html) for which not only requires installing ruby, SQLite, and rails itself, but also has you run an initialization command (`rails new blog`) that creates a genuinely [shocking number of files and directories](view-source:https://guides.rubyonrails.org/getting_started.html#creating-the-blog-application):

<details>
<summary>The files and directories created by Ruby on Rails' new blog command</summary>
<table><thead>
<tr>
<th>File/Folder</th>
<th>Purpose</th>
</tr>
</thead><tbody>
<tr>
<td>app/</td>
<td>Contains the controllers, models, views, helpers, mailers, channels, jobs, and assets for your application. You'll focus on this folder for the remainder of this guide.</td>
</tr>
<tr>
<td>bin/</td>
<td>Contains the <code>rails</code> script that starts your app and can contain other scripts you use to set up, update, deploy, or run your application.</td>
</tr>
<tr>
<td>config/</td>
<td>Contains configuration for your application's routes, database, and more. This is covered in more detail in <a href="[configuring.html](view-source:https://guides.rubyonrails.org/configuring.html)">Configuring Rails Applications</a>.</td>
</tr>
<tr>
<td>config.ru</td>
<td>Rack configuration for Rack-based servers used to start the application. For more information about Rack, see the <a href="[https://rack.github.io/](view-source:https://rack.github.io/)">Rack website</a>.</td>
</tr>
<tr>
<td>db/</td>
<td>Contains your current database schema, as well as the database migrations.</td>
</tr>
<tr>
<td>Dockerfile</td>
<td>Configuration file for Docker.</td>
</tr>
<tr>
<td>Gemfile<br>Gemfile.lock</td>
<td>These files allow you to specify what gem dependencies are needed for your Rails application. These files are used by the Bundler gem. For more information about Bundler, see the <a href="[https://bundler.io](view-source:https://bundler.io/)">Bundler website</a>.</td>
</tr>
<tr>
<td>lib/</td>
<td>Extended modules for your application.</td>
</tr>
<tr>
<td>log/</td>
<td>Application log files.</td>
</tr>
<tr>
<td>public/</td>
<td>Contains static files and compiled assets. When your app is running, this directory will be exposed as-is.</td>
</tr>
<tr>
<td>Rakefile</td>
<td>This file locates and loads tasks that can be run from the command line. The task definitions are defined throughout the components of Rails. Rather than changing <code>Rakefile</code>, you should add your own tasks by adding files to the <code>lib/tasks</code> directory of your application.</td>
</tr>
<tr>
<td>README.md</td>
<td>This is a brief instruction manual for your application. You should edit this file to tell others what your application does, how to set it up, and so on.</td>
</tr>
<tr>
<td>storage/</td>
<td>Active Storage files for Disk Service. This is covered in <a href="[active_storage_overview.html](view-source:https://guides.rubyonrails.org/active_storage_overview.html)">Active Storage Overview</a>.</td>
</tr>
<tr>
<td>test/</td>
<td>Unit tests, fixtures, and other test apparatus. These are covered in <a href="[testing.html](view-source:https://guides.rubyonrails.org/testing.html)">Testing Rails Applications</a>.</td>
</tr>
<tr>
<td>tmp/</td>
<td>Temporary files (like cache and pid files).</td>
</tr>
<tr>
<td>vendor/</td>
<td>A place for all third-party code. In a typical Rails application this includes vendored gems.</td>
</tr>
<tr>
<td>.dockerignore</td>
<td>This file tells Docker which files it should not copy into the container.</td>
</tr>
<tr>
<td>.gitattributes</td>
<td>This file defines metadata for specific paths in a git repository. This metadata can be used by git and other tools to enhance their behavior. See the <a href="[https://git-scm.com/docs/gitattributes](view-source:https://git-scm.com/docs/gitattributes)">gitattributes documentation</a> for more information.</td>
</tr>
<tr>
<td>.gitignore</td>
<td>This file tells git which files (or patterns) it should ignore. See <a href="[https://help.github.com/articles/ignoring-files](view-source:https://help.github.com/articles/ignoring-files)">GitHub - Ignoring files</a> for more information about ignoring files.</td>
</tr>
<tr>
<td>.ruby-version</td>
<td>This file contains the default Ruby version.</td>
</tr>
</tbody></table>
</details>

Of course, Rails is doing a lot of stuff for you! It's setting up a unit test framework, a blogging, framework, a database schema, and so on. If I wanted all of that, then Rails might be the way to go. But right now what I want to do is make a webpage that says "Hello World" and I should not have to figure out what a `Gemfile` is to do that.

As a reminder, here's the directory structure for our "Hello World" in PHP:

| File        | Description       |
| ----------- | ----------------- |
| index.php | The webpage file. |

My goal here isn't to rip on Ruby on Rails—although, is a Dockerfile really necessary when you're just "Getting Started"?—but to highlight a problem that is shared by basically every general-purpose programming language: using Ruby for web development requires a discomfiting amount of scaffolding.

Over in the Python ecosystem, one of the first ways you will encounter to make a website is with  [flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/), which is a much lighter-weight framework than Rails. In flask, you can also get the "Hello World" down to one file, sort of:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World"
```

Even here, there are a ton of concepts to wrap your head around. You have to understand a bunch of basic coding constructs like "functions" and "imports", as well as Python's syntax for describing these things. To run this code have to figure out how to install Python, how to install Python packages like `flask`, and how to run Python environment management tool like `venv` (a truly bizarre kludge that Python developers insist isn't that big of a deal but is absolutely insane if you come from any other modern programming environment). I know we said one file earlier, but if you want this work on anyone else's computer you're also going to have to document that you installed flask, using a file like `requirements.txt`. And what's going with the inscrutable `app = Flask(__name__)`?

If any of these concepts aren't arranged properly—in your head and in your file—your server will display nothing.

By contrast, you don't have to know a *thing* about PHP to start writing PHP code. Hell, you barely have to know the command line. If you can manage to install and run a PHP server this file will simply display in your browser.

And the file itself:

```php
Hello World
```

You didn't have to think about dependencies, or routing, or `import`, or language constructs, or any of that stuff. You're just running PHP. And you're on the web.

## What we talk about when we talk about Hello World

The time-to-Hello-World test is about the time between when you have an idea and when you are able to see the seed of its expression. That time is crucial—it's when your idea is in its most mortal state.

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

"Does my IP address have 69 in it?" is a dumb idea for a website. But sometimes dumb ideas evolve into good ideas, or they teach you something that's later used in service of a good idea, or they just make you chuckle. Or none of the above. The best thing about websites is that you don't have to justify them to anyone—you can just make them. And PHP is still the fastest way to make a ["dynamic"](https://blog.wesleyac.com/posts/no-static-websites) website.

I recently made a little [invoice generator with a local browser interface](https://github.com/alexpetros/invoice-generator) for my freelance business. It works great! It's got a homepage with a list of my generated invoices, a `/new.php` route for making a new one, and `/invoices/generated/{invoice_id}` routes to view each invoice in a printable format.

I don't find the boilerplate required to make a [RESTful web service](https://intercoolerjs.org/2016/01/18/rescuing-rest.html) in NodeJS especially onerous—I have a pretty good system for it at this point. But PHP brings the time-to-hello-world down tremendously. I just don't think this would have gotten off the ground if I had to setup ExpressJS, copy my `express.router()` setup, make 2 files for each route (the template and the javascript that serves it), and do all the other things I do to structure webapps in Node. Instead, I got all that stuff built-in with vanilla PHP, and that will presumably work for as long as PHP does. I didn't even have to touch [composer](https://getcomposer.org/).

I believe that more people should use the internet not just as consumers, but as creators (not of *content* but of *internet*). There is a lot of creativity on the web that can be unlocked by making web development more accessible to artists, enthusiasts, hobbyists, and non-web developers of all types. Softening the learning curve means making the common things easy and not introducing too many concepts until you hit the point where you need them. That's essential for beginners and experts alike.

# Notes
- My example invoice generator is not meant to be put online, so it doesn't escape text to prevent XSS attacks, or do the other [web security basics](https://htmx.org/essays/web-security-basics-with-htmx/).
- A lot of people have the attitude that writing vanilla code (and vanilla PHP especially) is never okay because you need secure-by-default frameworks to ensure that you don't make any security mistakes. It clearly true that if you are building professional software you should be aware of web security issues and make informed decisions about the security model of your application; not everyone is building professional software.
- Relatedly, one route to becoming is a software professional is to have a delightful experience as a software amateur.
- All that having been said, some of PHP's design decisions really lend themselves to insecure code. For starters, they really need [a short echo tag](https://www.php.net/manual/en/language.basic-syntax.phptags.php) that auto-escapes.
- I'm probably not going to start doing professional work in PHP—the language is interesting but too kludgy, and the value of the defaults diminishes as a greater percentage of the code becomes business logic—but I am definitely going to do more web art in PHP. I especially like how compact and shareable it can be, which has tremendous value for certain types of code.
- PHP is also missing a bunch of stuff that I consider really important, that makes pre-processing your requests close to mandatory. Big ones for me in include removing the `.php` file extension from the URL, and PUT/DELETE support.
- More languages should have a "thing" that they are "for." Maybe I'll write about how awk rekindled my love for programming next.
