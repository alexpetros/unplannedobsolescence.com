+++
title = "Behavior Belongs in the HTML"
description = "Some thoughts on doing the right thing now that we've tried everything else."
date = 2023-12-11
+++

When you click the button below, it's going to show you a little message.

<button onclick="alert('I was clicked!')">Click me</button>

Showing a pop-up when the user clicks a button isn't something the button supports on its own; you
have to code it. There are two ways to attach custom functionality to an HTML element: inline, or
using an event listener.

This is how you'd do it with an inline handler:

```html
<button onclick="alert('I was clicked!')">Click me</button>
```

And this is how you'd do it with an event listener:
```html
<button>Click me</button>

<script>
const btn = document.querySelector("button")

btn.addEventListener("click", () => {
  alert('I was clicked!')
})
</script>
```

If you've never thought about this before, your likely reaction is that the first example (inline)
seems better. It takes up way less space and puts all the relevant information right on the button.
Not so, according to the experts. The MDN Web Docs have this to say about
[using inline event handlers](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#inline_event_handlers_%E2%80%94_dont_use_these):

>  You can find HTML attribute equivalents for many of the event handler properties; however, you
>  shouldn't use these — they are considered bad practice. It might seem easy to use an event
>  handler attribute if you are doing something really quick, but they quickly become unmanageable
>  and inefficient.

Or, in case that wasn't clear enough:
> **You should never use the HTML event handler attributes** — those are outdated, and using them is bad
> practice. (emphasis theirs)

This is, in my polite opinion, completely wrong. The novices are right on this one. MDN is a
tremendous resource, and I understand why they recommend the second form, but combating this
particular ideology is essential to rehabilitating HTML's full functionality, and building durable
applications with it. I'll explain.

## \<form\> and function

MDN does not want you to use inline event handlers because they don't want you to mix form (HTML)
and function (JS). This is a programming principle called [Separation of
Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns#HTML,_CSS,_JavaScript) and the
HTML/CSS/JS split is a textbook example of it. From Wikipedia (at the time of this writing):

> HTML is mainly used for organization of webpage content, CSS is used for definition of
> content presentation style, and JS defines how the content interacts and behaves with the user.

Separation of Concerns is a great principle, but I think the drew the line in the wrong place. In
this conception of the web page, HTML is essentially the scaffolding that you dress up with CSS (for
style) and JS (for interactivity). But HTML is inherently interactive, too. It's sufficiently
interactive to power billion-dollar businesses without a single line of JavaScript.

Let's say you want to set up a text box and a search button so that people can search the web.
You'd start with an `<input type=text>` for the text box, and a `<button>` to search.

```html
<div>
  <input type=text name=q>
  <button>Search</button>
</div>
```

On the page it looks like this:
<div>
  <input type=text>
  <button>Search</button>
</div>

That button doesn't do anything; the text goes nowhere. But if you replace the `<div>` with a
`<form>`, like so:

```html
<form method=/search action=GET>
  <input type=text name=q>
  <button>Search</button>
</form>
```

then clicking the button submits your input as a query, and navigates to the result. So if you're on
`http://example.com` and the text box has `cats` in it, clicking submit will navigate you to
`http://example.com/search?q=cats`. The Google homepage [worked exactly like
this](https://web.archive.org/web/20040426014304/http://www.google.com/) for a very long time.

HTML defined that functionality in its entirety. The page does something interactive—it makes a
network request using your input, when you click the button—and no JavaScript was involved. It's
easy to read, semantic, and will work in every web browser forever. Most importantly, it
demonstrates that the entire concept of "HTML defines the layout, JS defines the functionality" is
definitionally incorrect.

## Enhancing the semantics
The problem with doing everything this way is that the functionality of HTML is extraordinarily
limited, and to augment that functionality we need JavaScript. Form validation is a great example.

This form is a lot like the previous one, only now it asks for an email address of at least 8
characters:

```html
<form>
  <input type="email" id="mail" name="mail" required minlength="8" />
  <button>Submit</button>
</form>
```

That will get the job done, sort of. It will keep the user from submitting something that is too
short, or doesn't look like an email, but it won't let you customize how the user is informed about
the requirements of the email address. This form, adapted for clarity from the MDN page on [form
validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation#validating_forms_using_javascript),
demonstrates how to do that:

```html
<form novalidate>
  <input type="email" id="mail" name="mail" required minlength="8" />
  <span class="error" aria-live="polite"></span>
  <button>Submit</button>
</form>
```

Now there is a `<span>` that starts off empty, but will be populated with an error message if the
email is invalid. There's also a `novalidate` attribute on the form that tells the browser not to do
HTML's built-in validation because we're going to do it all ourselves in JavaScript. And here is the
JavaScript that decides what the message is going to be, and adds it to the span.

```js
const form = document.querySelector("form");
const email = document.getElementById("mail");
const emailError = document.querySelector("#mail + span.error");

email.addEventListener("input", (event) => {

  if (email.validity.valid) {
    emailError.textContent = "";
    emailError.className = "error";
  } else {
    showError();
  }
});

form.addEventListener("submit", (event) => {
  if (!email.validity.valid) {
    showError();
    event.preventDefault();
  }
});

function showError() {
  if (email.validity.valueMissing) {
    emailError.textContent = "You need to enter an email address.";
  } else if (email.validity.typeMismatch) {
    emailError.textContent = "Entered value needs to be an email address.";
  } else if (email.validity.tooShort) {
    emailError.textContent = `Email should be at least ${email.minLength} characters; you entered ${email.value.length}.`;
  }

  emailError.className = "error active";
}
```

That code enhances the HTML so that it does the following things:

* If the user submits an invalid email, show them an error message
* If the email was empty, show "You need to enter an email address."
* If the email was too short, show "Email should be at least 8 characters; you entered X" (where X
  is the number of characters they entered)
* If the email was not an email, show "Entered value needs to be an email address."
* When the user starts typing, remove the error message

All those things aren't built into HTML, which is why you have to write them in JavaScript. A lot of
JavaScript. But what if they were? Hypothetically, you could design the following interface in the
HTML itself:

```html
<form>
  <input type="email"
         name="mail"
         required
         minlength="8"
         message-target="#email-error"
         value-missing-message="You need to enter an email address."
         type-mismatch-message="Entered value needs to be an email address."
         too-short-message="Email should be at least ${email.minLength} characters; you entered ${email.value.length}."
  >
  <span id=email-error></span>
  <button>Submit</button>
</form>
```

Instead of adding new messages in JavaScript, you write them on the input itself. That's better, for
a couple reasons:
* The code is legible. Where is the "input too short" message defined? In `too-short-messsage`.
* The [behavior is local](https://htmx.org/essays/locality-of-behaviour/). It's impossible *not* to
  see that someone changed the message, and where they did it.
* The logic can be trivially re-used on different inputs
* The interface automatically implements the [aria-live](https://w3c.github.io/aria/#aria-live)
  designation that is appropriate for a validation message (in this case, `polite`)

In some sense these are all the same advantage: they give HTML richer semantics.

Hopefully you're howling at your computer screen about this. "You didn't solve anything! Doing
validation is complex and you just magic wanded it away by designing a perfect interface for it."
Yes. Exactly. That is what interfaces are supposed to do. Better semantics make it possible for the
programmer to describe what the element does, and for someone else to take care of the details for
them.

I'm not saying you're not going to have to write JavaScript—[someone's got to write
JavaScript](https://www.youtube.com/watch?v=co4EsnwAM1Q&t=110s)—but if we start writing our
JavaScript libraries to enrich HTML's semantics, rather than replace them, we might get a lot more
mileage out of both.

Keep in mind that, at this stage, the custom semantics I'm using are still purely theoretical.
We'll talk about forwards compatibility, `data-` attributes, and all the hard details in a moment.
The first task is to acknowledge that HTML, as a *hyper*text markup language, is inherently
functional: the "hyper" denotes all the extra functionality, like links and forms, that we add to
the text. You need to [take HTML
seriously](https://intercoolerjs.org/2020/01/14/taking-html-seriously) to build good interfaces for
it.

Once we do that, the task ahead is to figure out how best to augment its limited semantics with our
own. That part is hard.

## Back to reality
Okay, so if we want to enrich HTML's semantics, what are the right ways to do it?

The main concern here is that as HTML is both a living standard and a mercilessly backwards
compatible one (it's a remarkable accomplishment that [the first website
ever](http://info.cern.ch/hypertext/WWW/TheProject.html) is still online and displays perfectly on
modern web browsers). So if I add `too-short-messsage` to my input element, and then a couple years
in the future [WHATWG](https://whatwg.org/) adds a new `too-short-messsage` attribute, the page will
start to break in unexpected ways.

[Microformats](https://microformats.org/) are a very old standard that still gets some use today,
perhaps most notably as part of the [Webmentions specification](https://www.w3.org/TR/webmention/).
They let you add add properties as class declarations, like this:

```html
<a class="p-name u-url" href="https://alexpetros.com">Alex Petros</a>
```

Something parsing the webpage will know that this link isn't just a random link, it's a link with my
name as the text (`p-name`), and that person's home page as the URL (`u-url`). This is nifty but
very limited. You could not implement a custom message using class names like this.

HTML solves this problem by reserving the `data-` prefix for [custom
attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*). This works
fine, and some custom attribute libraries like [Turbo](https://turbo.hotwired.dev/) embrace it. Take
this example from [their
documentation](https://turbo.hotwired.dev/handbook/drive#requiring-confirmation-for-a-visit), which
uses the `data-turbo-method` attribute to change a link's method from GET to DELETE (I make no
claims about whether that's a thing you *should* do):

```html
<a href="/articles/54" data-turbo-method="delete">Delete the article</a>
```

And that works! That will never get overwritten by future updates to the HTML standard. If you want
to write your whole attribute library that way, you can.

If I sound a little ambivalent about it, it's because I think everything about `data-*` attributes,
from their name to [the examples people
use](https://hacks.mozilla.org/2012/10/using-data-attributes-in-javascript-and-css/), suggests that
they are meant to store data, not behavior. You can of course just barrel ahead and extend HTML with
it, but the name and the verbosity really does discourage people from building semantics with it. If
you say that data attribues are for ["data that should be associated with a particular element but
need not have any defined
meaning,"](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) then
people will use them that way.

We know this is true because some very popular JavaScript libraries eschew the `data-` attributes
altogether and just add custom attributes with prefixes that are very *unlikely* to be added to
HTML. [Classic AngularJS](https://angularjs.org/) uses `ng-`, which is still all over the internet
today; [Alpine.js](https://alpinejs.dev/) prefixes its 15 custom attributes with `x-`;
[htmx](https://htmx.org/) does the same with `hx-` (although AngularJS and htmx both support
prepending *their* prefix with `data-`, just for the pedants).

Browsers have supported this, unofficially for ages, and it also works well. Here's a button that
toggles some arbitrary property using Alpine.js:

```html
<button x-on:click="open = ! open">Toggle</button>
```

This is, in my opinion, the right general idea, even though I (subjectively) dislike almost
everything about it. I find the `open = ! open` sort of weird (it's a global variable I guess?),
having to namespace with `x-` is still a small kludge, and overall it deviates from HTML semantics
in a way I don't vibe with. It's a *very* safe bet that WHATWG is not going to add `x-on:click`, but
it's also, at the time of this writing, not a guarantee.

## Custom attributes are (still) the way

In 2009, during the HTML5 specification process, John Allsop advocated for taking seriously the
possibility of custom attributes in his blog ["Semantics in HTML
5"](https://alistapart.com/article/semanticsinhtml5).

> Instead of new elements, HTML 5 should adopt a number of new attributes. Each of these attributes
> would relate to a category or type of semantics. For example, as I’ve detailed in another article,
> HTML includes structural semantics, rhetorical semantics, role semantics (adopted from XHTML), and
> other classes or categories of semantics.
>
> These new attributes could then be used much as the class attribute is used: to attach to an element
> semantics that describe the nature of the element, or to add metadata about the element.

He includes a couple examples, like one where you markup a paragraph as being ironic (I thought this
was a ridiculous example until I remembered that [people actually do this all the
time](https://en.wikipedia.org/wiki/Irony_punctuation), informally, with stuff like "/s"):

```html
<p rhetoric="irony">He’s a fantastic person.</p>
```

Or this one that would let you specify times in a machine-paresable format (later solved with the
introduction of the [`<time>`
element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/time)):

```html
<span equivalent=“2009-05-01”>May Day next year</span>
```

This was the right path. The thing says what it is, and specifies machine-parseable semantics in the
most human-readable way (although "equivalent" was a terrible name choice in that case).

There are still a lot of questions that need to be answered to make this work properly, which Allsop
also acknowledged at the time:

> I titled this section “some thoughts on a solution” because a significant amount of work needs to
> be done to really develop a workable solution. Open questions include the following.
>
> * How many distinct semantic attributes should there be? Should these categories be extensible,
and if so, how?
> * How are vocabularies determined?
> * Do we simply invent the terms we want, in much the same way that developers have been using
class values, or should the possible values all be determined by a standardized specification? Or
should there be a mechanism for inventing (and hopefully sharing) vocabularies, using some kind of
profile?
> * If we have a conflict between two vocabularies, such that two identical terms are defined by two
different vocabularies, how is this resolved?
> * Do we need a form of name spacing, or does some other mechanism exist?

Many of these questions still don't have good answers, because the field of web development mostly
let this question go stale during its "screw it, JavaScript everything" phase. You don't need to
extend the behavior of a form if you [rewrite it every
time](https://legacy.reactjs.org/docs/forms.html#controlled-components). As we start to exit that
era, I propose that we pick up where Allsop left off and begin doing to the work making HTML a
safely extensible hypertext system.

One thing we can do immediately officially sanction kebab-case attributes, roughly in line with
[this proposal](https://github.com/whatwg/html/issues/2271) (h/t to [Deniz
Akşimşek](https://denizaksimsek.com/en/) for showing me this). This would not only bless many of the
most popular HTML-enhancing frameworks, and therefore huge chunks of existing code on the internet,
with valid HTML, it would legitimatize the project of extending HTML with user- or library-defined
semantics.

## Okay Alex, how would you extend that button?
Remember the button from the beginning?

<button onclick="alert('I\'m back!')">Click me</button>

If you want to make a lot of buttons that display click messages, the best way to do that isn't with
`onclick` or an event listener, it's to enhance the button so that you can turn any button into a
message button.

```html
<button alert message="I was clicked">Click me</button>

<script>
// Get all the buttons with the 'alert' attribute
const buttons = querySelectorAll('button[alert]')
buttons.forEach(btn => {
  // Get the message property of the button
  const message = btn.getAttribute('alert')
  // Set the button to alert that message when clicked
  btn.addEventListener('click', () => { alert(message) })
})
<script>
```

This has the advantage of being re-usable across any button in your document. For less trivial
applications, you can bundle that behavior into a library with a very nice interface (probably with
a prefix, for now).

If you only need to do it for one or two buttons, though, just use `onclick`. It's less
code, it doesn't require that you specify an `id`, and it doesn't make you hunt to a different part
of the codebase to see what it does. Those are all "best practices" in my book.

# Notes

* Implementing the `tooShortMessage` and related attributes is left as an exercise to the reader.
* Even better, for the button example, would probably be `type=alert`, because that extends the
  [existing semantics](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#type), but I
  really don't want to get into how you'd approach namespacing that for forwards compatibility.
* Ironically, attribute interfaces have a much better case against being defined inline than the
  `document.getElementById` style of adding functionality, because the code that enables the
  interfaces can actually be re-used generically across elements.
* Some people think "custom semantics" is an oxymoron, because if it's not in the HTML standard it's
  not "semantic". That's not really what semantics are. Semantics describe the expressive power of
  something. Think of it like a language: whether something is or isn't a language has nothing to do
  with how many people speak it; that only affects how useful learning that language is going to be.
  User-defined semantics may be non-*standard* (at least until they adopted officially), but they
  are still semantics.
* A lot of people *really* hate seeing even tiny amounts of JS syntax in attribute declarations. I
  think this is a little silly, but I do understand it. I'll write on that subject in the future.
