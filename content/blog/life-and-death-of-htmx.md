+++
title = "Talk: \"The Life & Death of htmx\""
description = "Three small proposals to enhance the expressive power of HTML"
date = 2024-06-13
+++

<style>
iframe {
  display: block;
  margin: 10px auto;
}
</style>

This past weekend, I gave a talk entitled "The Life & Death of htmx" at [Big Sky Dev Con](https://bigskydevcon.com/).

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/inRB6ull5WQ?si=rMeNsVv2jQkUcFO_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Summary

The thesis of the talk is that, with 30 years of real-world usage evidence, we have a clear
understanding of HTML's limitations as hypertext, and with just three small additions to HTML, we
can address most of the use cases that the declarative AJAX libraries ([htmx](https://htmx.org),
[turbo/hotwire](https://hotwired.dev/), [unpoly](https://unpoly.com),
[pjax](https://github.com/defunkt/jquery-pjax), etc.) exist to resolve.

These three additions are:

1. Support PUT, PATCH, and DELETE methods in forms
2. Allow buttons to make HTTP requests on their own, without being wrapped in forms
3. Add the `target` attribute to buttons, and allow the response from links, forms, and buttons to replace arbitrary DOM elements, using CSS selectors in the `target` attribute

In the talk, I explain the importance of each, and describe at a high level how each addition should
be integrated alongside the existing HTML controls.

I don't have formal proposals for these yet, but I'm working on them! I'll update this space with
links when they are available, and if you have thoughts or help to offer, definitely [contact me](@/about.md).

## Post Script

I think the talk went pretty well, and don't have too many of the "ah, I forgot to say that one
thing" regrets that inevitably hit the minute you walk off stage. But there are a couple themes that
I want to highlight, alongside the main argument, about why vanilla HTML is not just one way to make
a website, but the most important one.

### Pure HTML is the past and future of essential internet infrastructure

Websites implemented in pure HTML are not only comically easy to maintain, but they largely adhere
to set of interface metaphors that all internet users understand. It's remarkable how many people we
were able to teach concepts like page navigation and form submission. To the extent that your
website adds to these basic concepts, it shrinks the base of users who will feel comfortable
navigating it.

While many businesses require additional interface metaphors and don't care if a septuagenarian pensioner with an HP notebook can navigate them, government services and other crucial web infrastructure need to be accessible to the largest group of people possible.

### Accessibility should be a pit of success

The best way to get people to use interfaces that computers (and therefore screen readers,
alternative controls, and other assistive technologies) can understand is to make to the "right" elements capable of things that the "wrong" elements are not. If a button can make HTTP requests without JavaScript but a `<div>` cannot, then a *lot* fewer people will use `<div>`s where they should be using `<button>`s.

Where possible, the most accessible way to build webpages should also be the easiest. If writing pure HTML is easy, expressive, and fun, then fewer people will turn to more complicated, less accessible solutions.

### Declarative interfaces are more maintainable

...for as long as the interface remains relevant. The SQL queries that you wrote 10 years ago work well with modern web stacks, and new features can be integrated seamlessly alongside old ones; the SOAP APIs, maybe not so much.

Perhaps a better universal interface for the internet will come along soon, but it is a [fairly good bet](https://en.wikipedia.org/wiki/Lindy_effect) that if 10 years from now you were handed a frontend codebase that hadn't been touched since 2024, you would want that codebase to be as close to pure HTML as possible.
