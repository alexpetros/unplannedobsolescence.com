+++
title = "The Messy Pile"
description = "Better CSS leads to better HTML"
date = 2024-08-01
+++

A couple months ago I was sitting next to [Ivy Wong](https://ivywong.dev) and I saw them working on
a dropdown menu so cute that I immediately asked how they did it.

It looked something like this:

<style>
ul.base {
  list-style-type: none;
  margin: 0 auto;
  padding: 0;
  width: fit-content;
}

.base li {
  background-color: bisque;
  border: 2px black solid;
  margin: 5px 0;
  text-align: center;
  width: 200px;
}

.messy-pile li:nth-child(odd) {
  transform: rotate(1deg);
}

.messy-pile li:nth-child(even) {
  transform: rotate(-1deg);
}
</style>

<ul class="base messy-pile">
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>


I call this the Messy Pile, and I think it's brilliant. It has lots of personality without breaking
the basic utility and structure of a menu list.
Internally, it feels haphazard; externally, it takes up a very normal box shape on the page, which
easily fits in both desktop and mobile views.

<ul class="base messy-pile" style="border: 2px solid red;">
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>

Let's make it together. We'll start with just a regular list of items:

```html
<ul class=messy-pile>
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>
```

<ul>
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>

And then add some CSS to make them orderly boxes:

```html
<style>
.messy-pile {
  list-style-type: none;
  margin: 0 auto;
  padding: 0;
  width: fit-content;
}

.messy-pile li {
  background-color: bisque;
  border: 2px black solid;
  margin: 5px 0;
  text-align: center;
  width: 200px;
}
</style>
```

<ul class="base">
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>


And finally, we rotate the boxes, one degree clockwise for the odd-numbered items, and counterclockwise for the even-numbered ones:

```css
.messy-pile li:nth-child(odd) {
  transform: rotate(1deg);
}

.messy-pile li:nth-child(even) {
  transform: rotate(-1deg);
}
```

And you get these cute tilted boxes!
<ul class="base messy-pile">
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>

## Better CSS Leads to Better HTML

Ivy's dense yet simple implementation of this pattern highlights something that took me a long time to learn: it's only possible to write good HTML if you write good CSS.

If you showed someone this design and asked them to implement it, it's easy to imagine an implementation that looks like this:

```html
<div class=messy-pile-container>
  <div class="messy-pile-item left">Home</div>
  <div class="messy-pile-item right">New</div>
  <div class="messy-pile-item left">Pages</div>
  <div class="messy-pile-item right">Logout</div>
</div>

<!-- the common styling is omitted for brevity -->
<style>
.messy-pile-item.left { transform: rotate(1deg); }
.messy-pile-item.right { transform: rotate(-1deg); }
</style>
```

I could definitely have written that depending on when in my career you asked me to do it.
So what's better about this one?

```html
<ul class=messy-pile>
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>

<!-- the common styling is omitted for brevity -->
<style>
.messy-pile li:nth-child(odd) { transform: rotate(1deg); }
.messy-pile li:nth-child(even) { transform: rotate(-1deg); }
</style>
```

An obvious reason is that using the CSS [`:nth-child()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child) pseudo-class (along with its `odd` and `even` keyword values) ensures that the pattern will automatically apply to an arbitrary number of items, as opposed to manually switching between  `left` and `right` classes.

Add new items, or move existing ones, and they'll all stay perfectly arranged, without touching the CSS.

<ul class="base messy-pile">
  <li>Home
  <li>New
  <li>Friends
  <li>Pages
  <li>Explore
  <li>Logout
</ul>

A subtler reason is that writing better CSS lets us move redundant information out of the HTML, dramatically simplifying it.
In doing so, we take advantage of both CSS features and HTML semantics.

```html
<ul class=messy-pile>
  <li>Home
  <li>New
  <li>Pages
  <li>Logout
</ul>
```
This is the only HTML in our example.
You'll notice that it's just a regular [unordered list](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul).
Its purpose is immediately clear and it's not visually dense in the slightest.
The only concession we've made to the styling is a single class, `messy-pile`.

The list semantics give us a natural way to style this component,
Lists [pretty much](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul#technical_summary) only have `<li>` children, so we can style the list itself with `.messy-pile` and the items with `.messy-pile li`.
There's very little we have to add to the HTML to make this work.

HTML semantics are often discussed in the context of making it easier for user agents (browsers, accessibility tech, etc.) to understand what your web page is trying to accomplish—but they also make it easier for *you* (and future readers of your code) to understand what your web page is trying to accomplish.

Here's the other sample implementation from before; it does the same thing but with most of the HTML semantics removed.

```html
<div class=messy-pile-container>
  <div class=messy-pile-item>Home</div>
  <div class=messy-pile-item>New</div>
  <div class=messy-pile-item>Pages</div>
  <div class=messy-pile-item>Logout</div>
</div>
```

This is much worse.
We have to add classes to both the container and the list item, since `<div>` is a generic element that could contain lots of things, including other `<div>`s.
The additional visual weight takes more time to read, feels bad to look at, and has none of the same accessibility properties.

This example is trivial—the version with the divs is still very intelligible—but as you start to layer on additional concepts, it gets out of hand quickly. For instance, the items in this example are mean to be a menu bar, so they all have to be links. With a list, that's still pretty easy to read:

```html
<!-- With a list -->
<ul class=messy-pile>
  <li> <a href=/home>Home</a>
  <li> <a href=/new>New</a>
  <li> <a href=/pages>Pages</a>
  <li> <a href=/logout>Logout</a>
</ul>
```

Definitely busier, but still easy to follow.
How does it look with divs?

```html
<!-- With divs -->
<div class=messy-pile-container>
  <div class=messy-pile-item>
    <a href=/home>Home</a>
  </div>
  <div class=messy-pile-item>
    <a href=/new>New</a>
  </div>
  <div class=messy-pile-item>
    <a href=/new>Pages</a>
  </div>
  <div class=messy-pile-item>
    <a href=/logout>Logout</a>
  </div>
</div>
```

Oh. It's starting to become XML (derogatory).

I'm being a little cheeky here by [omitting the closing tags](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li#technical_summary) for `<li>` elements to keep the `<a>` tags on the same line, while not doing the same for the `<div>`s.
But that's also my point!
`<li>` tags can be closed automatically, `<div>` tags can't.
Knowing HTML semantics lets you express your ideas more concisely, which in turn gives you more room to layer on new ideas before you start to feel the pressure to refactor.

Meanwhile, the div version looks and feels like a compile target—which is exactly why lots of people treat it as one.
When your HTML is lots of divs and classes, then higher level abstractions like [React Components](https://react.dev/learn/your-first-component) are necessary to make the code you're writing intelligible again.
Many people start from the assumptions that these abstractions are necessary because they've only ever seen code that's painful to write without them.

## But Does It Scale?

The reason we adopt additional abstractions on top of HTML semantics is because eventually the thing we're trying to describe gets more complicated.
It happens even with the most beautifully-written HTML.
Reality—or at least the little piece of the reality that we're trying to make easier with software—is complicated.

So if you're reading this and thinking, "sure, but what I'm doing could never be done with plain HTML and CSS," I humbly suggest that you give it a try.
You won't know what HTML and CSS can and can't accomplish until you actually try to push their limits for your use-case, forcing yourself to find those native features.
I, personally, have found that they go a lot farther than I previously thought.

Complex page layouts are going to require compromises—the trick is to use the tools available to you to push those compromises as far out as possible.
The better you know your tools, the farther you can get before you have to fashion new ones, and the simpler the abstractions you develop are going to be.

*This blog is about an interaction that Ivy and I had at the [Recurse Center](https://www.recurse.com/scout/click?t=044d120abf1c334d0b2a3132634eb025). If you love programming and are interested in expanding your horizons, you should check it out.*

# Notes

* If the unclosed `<li>` tags bother you, check out Aaron Parks' <cite class=article><a href="http://lofi.limo/blog/write-html-right">Write HTML Right</a>.</cite>
You may or may not want to write all your HTML that way, but it will hopefully break you out of the idea that HTML should look like XML. Markdown doesn't make you close bullets, why should HTML?
* [BEM](https://getbem.com/) is one popular methodology (among many) for scaling up CSS.
If your project and org chart are operating at a scale that BEM helps with, by all means use it, but I am personally of the opinion that strict conventions tend to age poorly as the language naturally develops internal mechanisms to deal with the problems that the conventions were originally built to solve—that's basically the argument of this whole blog.
* Also, `<button class="button">` makes me want to die. That simply can't be the best way to write CSS.
* Speaking of scaling: keep in mind that scaling developers is not a business requirement; scaling your ability to improve the website is.
If you make it easier for a couple developers to manage all the frontend tasks, you don't need to be siloing them so much.
This is true both "vertically" ([frontend vs backend](https://htmx.org/essays/a-real-world-react-to-htmx-port/#dev-team-makeup)), and horizontally (different teams working on different parts of the same page).
* On the other end of the spectrum is the [CSS Zen Garden](https://csszengarden.com/), which demonstrates how the same HTML can be used to create dramatically different-looking layouts, just by swapping out the stylesheet.
You certainly *don't* need your website to be ready for arbitrary stylesheets—and I'm not skilled enough with CSS to pull that off anyway—but you should shoot for a website with sufficiently sane HTML structure that it would easy enough to follow if it had *no* styling.
* I used a modified Messy Pile for the `<aside>`s in [my last blog post](@/blog/hard-page-load/index.md) You have to be on desktop with a wide enough window to see it applied.

