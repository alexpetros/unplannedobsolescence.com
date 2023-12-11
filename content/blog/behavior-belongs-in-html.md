+++
title = "Behavior Belongs in the HTML"
date = 2023-12-10
+++

When you click the button below, it's going to show you a little message.

<button onclick="alert('I was clicked!')">Click me</button>

Showing a pop-up when the user clicks a button isn't something the button supports on its own; you
have to code it. There are two ways to attach custom functionality to an HTML element: inline, or
using an event listener.

This is how you'd do it with an inline handler:

```html
<button onclick="alert('You clicked me :]')">Click me</button>
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

In this conception of the web page, HTML is essentially the scaffolding that you dress up with CSS
(for style) and JS (for interactivity). But HTML is inherently interactive, too. It's sufficiently
interactive to power billion-dollar businesses without a single line of JavaScript.

Let's say you want to set up a text box and a search button so that people can search the web.
You'd start with an `<input type=text>` for the text box, and a `<button>` to search.

```html
<div>
  <input type=text name=query>
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
`http://example.com/search?q=cats`. This is exactly how [the Google homepage
worked](https://web.archive.org/web/20040426014304/http://www.google.com/) for a long time.

This is functionality that the HTML defined. The page does something interactive—it makes a network
request using your input, when you click the button—and no JavaScript was involved. It's easy to
read, semantic, and will work in every web browser forever. And it demonstrates that the entire
concept of "HTML defines the layout, JS defines the functionality" is definitionally incorrect.

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
         messageElement="#email-error"
         valueMissingMessage="You need to enter an email address."
         typeMismatchMessage="Entered value needs to be an email address."
         tooShortMessage="Email should be at least ${email.minLength} characters; you entered ${email.value.length}."
  >
  <span id=email-error></span>
  <button>Submit</button>
</form>
```

Instead of adding new messages in JavaScript, you write them on the input itself. That's better, for
a couple reasons:
* It's legible. Where is the "input too short" message defined? In `tooShortMessage`.
* It's easy to change the message, potentially even for nontechnical owners.
* The logic can be re-used without re-using the messages themselves; different inputs can have
  different message just a one-line attribute
* The interface automatically implements the [aria-live](https://w3c.github.io/aria/#aria-live) role
  that is appropriate for a validation message

In some sense these are all the same advantage: they give HTML richer semantics.

Hopefully you're howling at your computer screen about this. "You didn't solve anything! Doing
validation is complex and you just magic wanded it away by designing a perfect interface for it."
Yes. Exactly. That is what interfaces are supposed to do. Better semantics make it possible for the
programmer to describe what they want to happen, and for someone else to take care of the details
for them.

I'm not saying you're not going to have to write JavaScript—[someone's got to write
JavaScript](https://www.youtube.com/watch?v=co4EsnwAM1Q&t=110s)—but if we start writing our
JavaScript libraries to enrich HTML's semantics, rather than replace them, we might get a lot more
mileage out of both.

## Taking HTML seriously
The first task is to acknowledge that HTML, as a *hyper*text markup language, is inherently
functional: the "hyper" denotes all the extra functionality, like links and forms, that we add to
the text. You need to [take HTML
seriously](https://intercoolerjs.org/2020/01/14/taking-html-seriously) to build good interfaces for
it. Once we do that, the task ahead is to figure out how best to augment its limited semantics with
our own.

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
  const message = btn.getAttribute('message')
  // Set the button to alert that message when clicked
  btn.addEventListener('click', () => { alert(message) })
})
<script>
```

If you only want to do it for one or two buttons, though, just use `onclick`. I promise it's fine.

# Notes

* Implementing the `tooShortMessage` and related attributes is left as an exercise to the reader.
* Some JavaScript libraries do use attribute interfaces, like [htmx](https://htmx.org/) (disclosure,
  I am a maintainer), [Alpine.js](https://alpinejs.dev/), and [Turbo](https://turbo.hotwired.dev/).
  This article should be understood as a defense of that interface choice, and an encouragement that
  other JS libraries consider the same.
* Ironically, attribute interfaces have a much better case against being defined inline than the
  `document.getElementById` style of adding functionality, because it can actually be re-used
  generically across elements.
