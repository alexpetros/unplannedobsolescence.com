+++
title = "Custom HTML Has Levels To It"
description = "A framework for describing what script tag JavaScript libraries have known for a decade: custom attributes are the simplest way to layer functionality on top of HTML."
date = 2023-12-31
+++

The comment I received most frequently on "[Behavior Belongs in the HTML](@/blog/behavior-belongs-in-html/index.md)" was: "don't Web Components solve this?"

Web Components aren't an interface. They are... well, [a lot of things](https://github.com/WICG/webcomponents/blob/1b75f7516e9901c26f1eb639d929aa82402c2fe0/README.md), including: [the Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM), [HTML templates](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template), and a bunch of JavaScript APIs. But if what you mean is "custom elements," then the answer is no. If you want to customize the behavior of an element, you shouldn't have to wrap it in a new one.

To illustrate, I'm going to use the example that Chris Ferdinandi arrives at in "[HTML Web Components](https://gomakethings.com/html-web-components/)." He uses Web Components to make a form that, when it's submitted, replaces the `#item-list` element with the response body, instead of navigating to a new page:
```html
<ajax-form target="#item-list">
  <form method="post" action="/subscribe">
    <input type="email" id="email" name="email">
    <button>Subscribe</button>
  </form>
</ajax-form>
```

This is great! Its declarative interface is easy to understand, and the form will work in the old, standard way if JavaScript is turned off (a concept called "progressive enhancement"). There's just one problem with it: that wrapper element, `<ajax-form>`, is totally superfluous.

```html
<form method="post" action="/subscribe" target="#item-list">
  <input type="email" id="email" name="email">
  <button>Subscribe</button>
<form>
```

In my version, I removed `<ajax-form>` and put the `target` attribute on the form itself. It has the same functionality and same fallback capability, but without any nesting (you'd want to use a slightly different name than "target," but more on that later).

<!-- (I'm aware that Ferdinandi is demonstrating how to use Web Components using their existing interface; I'm aware that Web Components have useful JavaScript APIs that custom attributes do not; I'm making a point about how HTML should support an easier way to accomplish the same task) -->

If all you need to do is augment the functionality of a single DOM node, custom attributes are a better interface for it, for a couple reasons:

1. **A flatter document is easier to read** - I'm not saying you have to write all your HTML [like this guy](http://lofi.limo/blog/write-html-right), but to the extent that you can flatten your document without loss of structure, you should.
1. **Surrounding with tags is a hassle** - Yes, even with a good text editor, adding, editing and removing surrounding tags is annoying, compared to editing an attribute.
1. **It's closer to the default semantics** - The markup (and DOM tree!) reflects that I'm slightly changing how the form works, not nesting the form inside a different form.

Attributes are a demonstrably superior interface for customizing HTML elements—which is why when WHATWG adds behavior to existing elements, it does so by adding new attributes, not new tags to wrap them with. Using tag wrappers to alter the behavior of existing elements is a kludge, required only because HTML doesn't properly support custom attributes. As Ferdinandi himself says: "what I love about Web Components is that you can easily customize behavior with custom attributes." You shouldn't need Web Components for that.

Incidentally, `target` in the above example is identical to [htmx's `hx-target`](https://htmx.org/attributes/hx-target/) attribute, which also goes directly on the form.

```html
<form hx-post="/subscribe" hx-target="#item-list">
  <input type="email" id="email" name="email">
  <button>Subscribe</button>
<form>
```

In my time as an htmx maintainer, no one has ever asked "why can't I wrap the form with a new element instead?"

## Custom attributes fill the semantic deviation gap

My theory of custom attributes is that they are missing link between standard HTML and custom (web) components. They allow library authors to increase the capabilities of HTML, but in exchange for limiting those extensions to existing HTML elements, they get to borrow most of the existing elements' semantic power.

I think of it in levels, where each number represents a jump in the amount you are deviating from HTML's default semantics:

<ol start=0>
<li>Using standard HTML
<li>Using standard HTML elements with custom behavior
<li>Using custom HTML elements
<li>Using elements of some other framework that compiles down to HTML
</ol>

Ideally, you want to deviate as little as possible, because each successive level of semantic deviation represents a responsibility that you have inherited from the browser:

<ol start=0>
<li>The browser understands everything
<li>The browser knows what this element is, but not how it works
<li>The browser knows neither what this element is nor how it works
<li>All of the above, only now it's the framework's responsibility, not yours
</ol>

So when you add a custom attribute to a form to change its behavior, your browser no longer controls that element's functionality, but *it still knows that it's a form*. That means you get all the built-in browser form features with no additional work, including autocomplete, screen reader functionality, and predictable refresh behavior—much better than if just made your own form-like component.

## These features go to Level 2

Sometimes you really do need to go to Deviation Level 2, and create not just new behavior but a new *thing*. Here's an example I adapted from Eric Meyer's "[Blinded by the Light DOM](https://meyerweb.com/eric/thoughts/2023/11/01/blinded-by-the-light-dom/)," which I'm embedding directly inside my page because making your own web site is cool and I get to do that:

<font-slider unit=em target=".preview span">
  <label for=title-size>Title Font Size</label>
  <input id=title-size type=range min=0.5 max=4 step=0.1 value=2>
</font-slider>

<div class=preview>
  <span>Unplanned Obsolescence</span>
</div>

This is a `<font-slider>`. It's a custom element that combines a `<label>` and a `<input type=range>` to make entirely new thing: a reset-able slider that controls font size. Take a moment to read the HTML interface for it.

```html
<!--
I'm deliberately not including any of the CSS or JS, because this blog
is about HTML interfaces. See the link above or View Source for the rest.
-->
<font-slider unit=em target=".preview span">
  <label for=title-size>Title font size</label>
  <input id=title-size type=range min=0.5 max=4 step=0.1 value=2>
</font-slider>

<div class=preview>
  <span>Unplanned Obsolescence</span>
</div>
```

In "[Behavior Belongs in the HTML](http://127.0.0.1:1111/blog/behavior-belongs-in-html/#enhancing-the-semantics)," I emphasized how the attribute controls (`unit`, `target`, `max`) are easy to edit even if you don't know how they're implemented. Still true! But this time I want you to think about what the existence of `<font-slider>` adds to this markup. What new *meaning* it creates. What the HTML is *saying* to you.

It's saying that the label and the input function together as a "font slider"—in which the value of the input will be used for the CSS on the page. That's entirely different from what they mean when they're together inside a `<form>` tag, where the value of that input will be used as a parameter in a network request.

```html
<!-- This is just a labeled slider; it could control anything -->
<label for=random-range>Some slider</label>
<input id=random-range type=range>

<!-- This is a form slider; its value will be submitted to a server -->
<form>
  <label for=form-range>Input value</label>
  <input id=form-range type=range>
</form>

<!-- This is a font slider; its value sets font sizes on the page -->
<font-slider>
  <label for=font-range>Font size</label>
  <input id=font-range type=range>
</font-slider>
```

The difference between `<font-slider>` and `<ajax-form>` is that the former establishes a new meaning for its subtree (this labeled input changes the font) and the latter retains the overall meaning of its subtree (the form still makes an HTTP request and displays the response to the user) while slightly modifying its behavior (this form will will display its response in the current page instead of a new one).

You can quibble about what degree of modification constitutes "new meaning"—that's language for ya—but what matters is that there real tradeoffs at each deviation level. Library authors who only want to enhance existing elements (whatever that means to them) see this, and—correctly—decide that their library will be easier to use if it is based in custom attributes rather than Web Components.

Adding a new element is still more difficult than adding a new attribute, but in exchange for the extra syntax, we get increased power that suits the complexity of the task.

## Fence the cowpaths
There are good reasons for using all of these levels, but only Deviation Level 1 lacks the appropriate support in legal HTML (`data-` attributes are insufficient, for reasons described by [me here](@/blog/behavior-belongs-in-html/index.md#back-to-reality) and better [Joshua Wise here](https://github.com/whatwg/html/issues/2271#issuecomment-744188324)).

When you talk about the need for better interfaces, you always get some comment along the lines of "well the thing you're describing isn't really that bad and people can just do it this other way." That might be true. But if it's worse than the alternative, people will use the alternative.

A significant chunk of the web development community lives happily at Deviation Level 4; they understand HTML not as an authorship language, but as a compile target, and interact with HTML semantics only insofar as they are relevant for understanding the behavior of React, or Svelte, or LiveView. Staying in framework-land offers real ergonomic benefits for writing HTML-like markup, in addition to the actual reactive functionality that people ostensibly use the frameworks for.

<!-- (I will leave it to future blogs posts to convince you that there are many cases where writing plain HTML matters ([but here's a hint](https://htmx.org/essays/no-build-step/)). -->

If you think writing HTML directly should be encouraged (an argument for a future blog post), then it's important that HTML's ergonomics keep up with that of its competitors, where backwards compatibility and good sense permit.

Fortunately, there's an extremely easy way to do this: [save kebab-case attributes for custom behavior](https://github.com/whatwg/html/issues/2271). This has excellent symmetry with kebab-case *elements*  already being reserved for users; instantly blesses multiple, significant JS libraries with valid markup; and encourages a field of HTML innovation whose utility is so self-evident that it has managed to develop in spite of official discouragement. As the OP, [Lea Verou](https://lea.verou.me/), wrote in 2017:

> The more commonplace invalid HTML becomes, the less authors care about authoring valid HTML. Validation becomes pointless in their eyes if they see tons of perfectly good use cases being invalid.

I won't rehash the debate on that WHATWG issue here, but I want to emphasize one point in particular: making custom kebab-case attributes legal is something that can and should be decided on its own merits, independent of what JavaScript interface you build to interact with it. Verou recently put forward [a proposal](https://github.com/WICG/webcomponents/issues/1029) for an `Attribute` class that makes use of a lot of the same ideas as Web Components. That looks great—and hard. Hard to get right, hard to get consensus on, hard to get Google or Apple to commit to building. Reserving just the names, however, is a much smaller problem space, and can be done without convincing a billion-dollar company that it's worth their time.

The best time to make `ng-*`, `x-*` and `hx-*` legal HTML was in 2017. [The second best time is now](https://github.com/whatwg/html/issues/2271#issuecomment-1863139169).

# Notes
*Thanks to [Katrina Scialdone](https://unmodernweb.com/) for reading a draft of this blog*.

1. Copying Eric Meyer's `<super-slider>` (I changed it to `<font-slider>` to make the semantic point a little better) was eye-openingly easy. I just dumped the `<style>` and `<script>` tags from JS Fiddle he embedded and it worked perfectly. That's the future—we're just working on the interface.
1. Web Components aren't an interface—[not one for users anyway](https://daverupert.com/2023/07/why-not-webcomponents/)—but if you want to see what a good declarative interface for Web Components might look like, check out Katrina's in-progress [Facet library](https://github.com/kgscialdone/facet).
1. Supposedly, Web Components are in use [all over the place](https://web-highlights.com/blog/are-web-components-dead/) (probably because they're so reliable to re-use and embed), but "writing custom HTML elements" is what "Web Components" sounds like it should mean, and I expect that's what a lot of people are thinking about when they ask why Web Components haven't taken off.
1. At the risk of wading into the weird holy war around htmx... it's ironic that the libraries most committed to hypermedia—in both [philosophy](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/) and [practice](https://htmx.org/essays/a-response-to-rich-harris/)—are the only ones writing invalid HTML. And it's completely unnecessary.
1. Happy New Year!

<!--
Everything after this point is adapted from Eric Meyer's blog post.
Read it here: https://meyerweb.com/eric/thoughts/2023/11/01/blinded-by-the-light-dom/
-->
<style>
.preview {
  border: 1px solid;
  padding: 1em;
  background: #eee;
}
.preview span {
  font-weight: bold;
  font-size: 2em;
  margin: 0;
}
font-slider {
  display: flex;
  align-items: center;
  margin-block: 1em;
}
font-slider input[type="range"] {
  margin-inline: 0.25em 1px;
}
font-slider .readout {
  width: 3em;
  margin-inline: 0.25em;
  padding-inline: 0.5em;
  border: 1px solid #0003;
  background: #EEE;
  font: 1em monospace;
  text-align: center;
}

</style>
<script>
class fontSlider extends HTMLElement {
  connectedCallback() {
    let targets = document.querySelectorAll(this.getAttribute("target"));
    let unit = this.getAttribute("unit");

    let slider = this.querySelector('input[type="range"]');
    for (const targetEl of targets) {
      slider.addEventListener("input", (e) => {
        targetEl.style.setProperty("font-size", slider.value + unit);
        readout.textContent = slider.value + unit;
      });
    }

    let reset = slider.getAttribute("value");
    let resetter = document.createElement("button");
    resetter.textContent = "↺";
    resetter.setAttribute("title", reset + unit);
    resetter.addEventListener("click", (e) => {
      slider.value = reset;
      slider.dispatchEvent(
        new MouseEvent("input", { view: window, bubbles: false })
      );
    });
    slider.after(resetter);

    let label = this.querySelector("label");
    let readout = document.createElement("span");
    readout.classList.add("readout");
    readout.textContent = slider.value + unit;
    label.after(readout);

    if (!label.getAttribute("for") && slider.getAttribute("id")) {
      label.setAttribute("for", slider.getAttribute("id"));
    }
    if (label.getAttribute("for") && !slider.getAttribute("id")) {
      slider.setAttribute("id", label.getAttribute("for"));
    }
    if (!label.getAttribute("for") && !slider.getAttribute("id")) {
      let connector = label.textContent.replace(" ", "_");
      label.setAttribute("for", connector);
      slider.setAttribute("id", connector);
    }
  }
}

customElements.define("font-slider", fontSlider);
</script>
