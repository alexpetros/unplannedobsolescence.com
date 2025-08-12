+++
title = "Building the Hundred-Year Web Service"
description = "How to build software infrastucture that lasts a very long time"
date = 2024-10-11
+++

<style>
iframe {
  display: block;
  margin: 10px auto;
}
</style>

My [UtahJS](https://utahjs.com/) talk, ["Building the Hundred-Year Web Service"](https://www.youtube.com/watch?v=lASLZ9TgXyc), was put online this week!
It's about how to build software infrastructure that lasts a very long time.

<!-- more -->

If you're not a software engineer (very unlikely that you're reading this blog if so, but it's possible) the first 11 minutes of the talk are non-technical, and have some insights about the future of the internet that I hope to expand on soon, in other contexts.
So it's worth watching up until that point, before I start explaining to web developers how I think they should be making web services.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/lASLZ9TgXyc?si=QbvceWOSzarlGWVr" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Summary

This is my first stab at publicly articulating something that has been on my mind for a while: is it possible to build software infrastructure with longevity and maintenance characteristics that rival those of physical infrastructure?
A lot of people think this is basically impossible—our computational capabilities are increasing too rapidly, and our software is changing too frequently, that the only way to keep up is a constant and significant expenditure of resources.
I disagree.

In the talk, I analogize this moment in software to the building of the [Williamsburg Bridge](https://en.wikipedia.org/wiki/Williamsburg_Bridge).
The Williamsburg Bridge was conceived in the 1800s, and built with horse-drawn carriage in mind, yet we've been able to adapt that structure to the needs of a 21st-century city (well, sort of; it should have more bike lanes, but that's a political problem).
Maintaining that bridge today, we make use of the work of engineers who could not possibly have imagined what we're using it for; the invention of the automobile did not require us to ["write" the bridge from scratch](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/).

If you consider what software abstractions could plausibly be used to build hundred-year software infrastructure, so far there's really only one: The Web.
This talk takes seriously the idea that something you put online today could remain online and useful for 100 years, and walks through some technology choices that I believe would make that outcome more likely.

## tl;dw

1. [Use SQLite](https://blog.wesleyac.com/posts/consider-sqlite)
2. Describe the actions of your service with [HTTP verbs](https://alexanderpetros.com/triptych/form-http-methods#REST-in%20Practice) as much as possible
3. Write plain HTML (with templates); enhance it sparsely; use isolated scripts.

There are a lot of specifics in the second half of the talk, and [this blog you're reading now](/blog) has other explainers that synthesize with that design philosophy.

And of course, the ideas expressed here are why it's so important to (carefully, deliberately) [enhance HTML with proper HTTP Method support and more dynamic functionality](https://alexanderpetros.com/triptych/).
