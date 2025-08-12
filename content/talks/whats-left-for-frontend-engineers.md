+++
title = "What's Left for Frontend Engineers?"
description = "How to build software infrastucture that lasts a very long time"
date = 2025-08-12
+++

<style>
iframe {
  display: block;
  margin: 10px auto;
}
</style>

I went back to Bozeman!

<iframe width="560" height="315" src="https://www.youtube.com/embed/z7M2inHiT4Y?si=FVOp0xVAx2lUSuem" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<!-- A couple months ago <a href="https://deniz.aksimsek.tr/en/">Deniz Akşimşek</a> made an offhand comment to me: -->

<!-- > i really don't want to be a full stack developer... i want to be a frontend developer in the alternate universe where htmx has fully taken over and write web components and css all day -->

<!-- This talk is about what it's like to be a frontend developer in that world. It's closer than you think. -->


## Summary

Building webservices with HTML APIs (aka MVC, aka [server-side rendering](@/blog/the-server-doesnt-render.md), aka "rails-style") is gaining traction again, thanks to improvements in web standards and lightweight [HTML-driven](@/blog/behavior-belongs-in-html.md) libraries like [htmx](https://htmx.org).
Although there will occasionally be reasons to go beyond what the platform provides, this will always be [the architecture that best aligns with the core competencies of the web](@/blog/hard-page-load/index.md), and the platform is improving every day.

But if the backend engineers are writing HTML, what's left for the frontend engineers?
I propose a basic set of responsibilities for the browser specialists on the team.

1. **Setup the infrastucture** - know how a template engine works, get it installed, and set up the basic page structure
1. **Extend HTML** - write new [custom elements](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements) that add [declarative capabilities to your templates](https://htmx.org/essays/webcomponents-work-great/)
1. **Be the browser expert** - own the more complicated frontend problems—like security and accessibility—and be up to date on the most future-proof ways to handle them

And if you run out of things to do?
Well, your backend colleagues are full-stack now—no reason you can't be too.

## Further watching

A number of Big Sky Dev Con '25 talks touched on similar ideas (hypermedia-mentum?), and if you enjoy this one, I recommend also checking out these others:

["HTML is stealing our jobs!"](https://youtu.be/cdocEPDlwYM?si=zeLwnNNduQm8cVII) - Robbie Wagner

["Extending vs Scripting: Lessons from building the Hyperview client"](https://www.youtube.com/watch?v=GJdgZsnihnM) - Adam Stepinski

["The Platform and a Stylesheet (A path to Platform & SPA Parity)"](https://www.youtube.com/watch?v=aknX6xq8Vfg) - Tony Ennis
