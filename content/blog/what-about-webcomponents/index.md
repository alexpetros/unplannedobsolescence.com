+++
title = "Web Components Have a Missing Link"
description = ""
date = 2023-12-20
draft=true

[extra]
image = ""
+++

The comment I received most frequently on [Behavior Belongs in the HTML](@/blog/behavior-belongs-in-html/index.md) was: don't Web Components solve this? I'll give the short answer, and then an example, and then some thoughts about relationship between custom attributes and Web Components.

## The short answer
No.

If you want to customize the behavior of an element, you shouldn't have to wrap it in a new one.

## Custom attributes vs custom elements
In a recent [blog post](https://gomakethings.com/html-web-components/), Chris Ferdinandi at Go Make Things demonstrates how Web Components can be used to add functionality to regular form elements. Here it is, edited down for clarity (I removed a few of the attributes):

```html
<ajax-form target="#item-list">
  <form method="post" action="/subscribe">
    <input type="email" id="email" name="email">
    <button>Subscribe</button>
  </form>
</ajax-form>
```

This concept is great! It augments the form so that when it's submitted, instead of navigating to a new page, a subtree of the DOM (`#item-list`) gets replaced with the response body. Its declarative interface is easy to understand, and it "progressively enhances" the form, meaning it will work in the old, standard way if JavaScript is turned off. There's just one problem with it: that wrapper element, `<ajax-form>`, is totally superfluous.

```html
<form method="post" action="/subscribe" target="#item-list">
  <input type="email" id="email" name="email">
  <button>Subscribe</button>
<form>
```

In my version, I removed `<ajax-form>` and put the `target` attribute on the form itself. It has the same functionality and same fallback capability, but without any nesting.

(I'm aware that Ferdinandi is demonstrating how to use Web Components using their existing interface; I'm aware that Web Components have useful JavaScript APIs that custom attributes do not; I'm making a point about how HTML should support an easier way to accomplish the same task)

If all you need to do is augment the functionality of a single DOM node, the latter example is a better interface for doing it, for a couple reasons:

1. **A flatter document is easier to read** - I'm not saying you have to write all your HTML [like this guy](http://lofi.limo/blog/write-html-right), but to the extent that you can flatten your document without loss of structure, you should.
1. **Surrounding with tags is a hassle** - Yes, even with a good text editor, adding or removing surrounding tags is annoying, compared to adding or removing an attribute.
1. **It's closer to the default semantics** - The markup (and DOM tree!) reflects that I'm slightly changing how the form works, not nesting the form inside a different form.

Attributes are a demonstrably superior interface for customizing HTML elements than tag wrappers, which is why when WHATWG adds behavior to existing elements, it does so by adding new attributes, not new wrappers.

Library authors who also want to enhance existing elements see this, and—correctly—decide that their library will be easier to use if it is based in custom attributes rather than Web Components.

## The missing level of HTML customization
So attributes are a better interface for customizing the behavior of one element. The problem is that custom elements are legal but custom attributes are not (`data-` attributes are not sufficient, for reasons [described here](@/blog/behavior-belongs-in-html/index.md)).

My theory of custom attributes is that they are missing link between standard HTML and custom (web) components. They allow library authors to increase the capabilities of HTML, but in exchange for limiting those extensions to existing HTML elements, they get to borrow most of the existing elements' semantic power.

I think of it in levels, where each number represents a jump in the amount you are deviating from HTML's default semantics:

<ol start=0>
<li>Using standard HTML
<li>Using standard HTML elements with custom behavior
<li>Using custom HTML elements
<li>Using elements of some other framework that compiles down to HTML
</ol>

Ideally, you want to deviate as little as possible, because each successive level of deviation represents a responsibility that you have inherited from the browser:
<!-- If all you want to do is make your form behave a little differently, than you don't anything more than deviation Level 1. This is important because each -->


<ol start=0>
<li>The browser understands everything
<li>The browser knows what this element is, but not how it works
<li>The browser knows neither what this element is nor how it works
<li>All of the above, only now it's the framework's responsibility, not yours
</ol>

So when you add a custom attribute to a form to change its behavior, your browser no longer controls that functionality, but, crucially, it *still knows that its a form*. That means you get all the other form behavior by default, including autocomplete, screen reader functionality,

There are good reasons for using all of these levels, but only deviation Level 1 lacks the appropriate support in legal HTML .

## If you want to encourage people write HTML, make it the easiest thing
Some significant chunk of the web development community lives happily at #4; they understand HTML not as an authorship language, but as a compile target, and interact with HTML semantics only insofar as they are relevant for understanding the behavior of React, or Svelte, or LiveView. If you are among them, I will leave it to future blogs posts to convince you that there are many cases where writing plain HTML matters ([but here's a hint](https://htmx.org/essays/no-build-step/)).

<!-- There are, however, a lot of people who care deeply about making plain HTML useful and easy. For reasons I'll expand upon as I continue this blog, I am one them. -->

When you talk about the need for better interfaces, you always get some comment along the lines of "well the thing you're describing isn't really that bad and people can just do it this other way." That's blaming the user for HTML's bad ergonomics, and, if you want people to read, write, and enhance HTML, it's completely unproductive.

Not everyone thinks this is important!

<!-- So what? The Web Component solution is good enough. You use [vim-surround](https://github.com/tpope/vim-surround) and are happy to delete tags with a simple `dst`. It's not *that* annoying. -->

<!-- Obviously, in many cases, custom attributes are not going to be enough. -->

<!-- The only other thing I changed was `target` to `resp-target` so that it would have a hyphen and be forwards compatible if [WHATWG reserves hyphenated attributes for custom behavior](https://github.com/whatwg/html/issues/2271), which they should. -->

HTML currently has *much* better tools for supporting custom elements (i.e. Web Components) than it does for custom attributes, which are illegal (but perfectly functional) if you don't prefix them with `data-`.

Incidentally, `target` in the above example is identical to [htmx's `hx-target`](https://htmx.org/attributes/hx-target/) attribute, which also goes directly on the form.

```html
<form hx-post="/subscribe" hx-target="#item-list">
  <input type="email" id="email" name="email">
  <button>Subscribe</button>
<form>
```

To my knowledge, no one has ever asked "why can't I wrap the form with a new element instead?"


