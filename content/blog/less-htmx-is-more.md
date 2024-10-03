+++
title = "Less htmx is More"
description = "How to build great websites with htmx by learning a couple browser features alongside it."
date = 2024-10-02

+++

It's been two years since I wrote my first production webservice with [htmx](https://htmx.org).
Two years is not a very long time, but early indicators suggest that the software projects I've written with htmx are a much better experience for users, and orders of magnitude easier to maintain, than the software projects they replaced.
They are likely to remain useful for longer than anything else I've ever written (so far).
Pretty good!

Like any new tool, especially a tool that got popular [as quickly as htmx](https://risingstars.js.org/2023/en#section-framework), there are differing schools of thought on how best to use it.
My approach—which I believe necessary to achieve the results described above—requires you to internalize something that htmx certainly hints at, but doesn't enforce: use plain HTML *wherever possible*.

Once you get the hang of it, htmx starts pushing you in this direction anyway, and you start reaching for htmx less and less.
It requires a mindset shift though, especially if you're not accustomed to [building page behavior with HTML features](@/blog/behavior-belongs-in-html.md).


## How should we use htmx?

In my opinion, most websites should be using htmx for:

1. Updates that users would not expect to see on a refresh (emphemeral content)
2. Updates that would *also* be present on a new, full-page load

Everything else should use [regular links](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a) and [regular forms](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) that do standard, full-page navigations.

<aside>
You also currently need htmx (or an equivalent library) to enable support for PUT and DELETE on regular forms.
More in that in the <a href="#notes">notes section.</a>
</aside>

Let's say you're making a website that shows today's baseball games, and you want it to update the stats live.
Here's how I would approach that.

The website's home page should have all the currently-playing games on it, showing the live score for each one.
Each of those live scoreboards uses htmx to [poll the server](https://htmx.org/attributes/hx-trigger/#polling) at regular intervals for updates.
Clicking on the scoreboard title (which is a regular `<a>` link) takes you to that game's page, at its own URL.
The game page has not just the score, but the pitch count, the game's full box score, and so on;
these update with htmx as well.

The idea here is that the website still has a sound URL structure, which is managed by the core browser functionality, while interactivity is carefully layered on top, with targeted updates.
Exactly what merits a targeted update versus a new page depends on what you're building, but you should have a mental model that distinguishes between them in some capacity.

<aside>
Using htmx to enable specific, isolated functionality, rather than letting it drive the overall experience, is arguably <a href="https://htmx.org/essays/is-htmx-another-javascript-framework/">using it like a library, instead of a framework</a>.
</aside>

Unfortunately, a lot of the beginner guides suggest that you can get started easily by "upgrading" all your links with `hx-boost`.
I disagree with this.
While htmx is amazing for targeted page updates, I highly discourage using it to take over *all* page navigation.

## What is hx-boost?

[`hx-boost`](https://htmx.org/attributes/hx-boost/) is a feature of the converts a "regular" link into a "boosted" link:

```html
<!-- normal link -->
<a href=example.com>Example</a>

<!-- boosted link -->
<a href=example.com hx-boost=true>Example</a>
```

Instead of doing a full page navigation when the "boosted" link is clicked, htmx will issue an HTTP request to the link's URL and replace the `<body>` of the page with the content of the response.
In theory, this feels "smoother" because it only repaints part of the page, mimicking the feel of a Single-Page Application (SPA).

## What's wrong with hx-boost?

The problems it solves are better solved by other means, and it creates a lot of problems on its own.

Use `hx-boost` long enough, and something will go wrong.
You'll click the back button and see only a partial page update;
you'll refresh the page and it'll go blank;
another library that you're using will conk out;
elements will enter or exit the DOM in a way that you did not expect.

From a coding perspective, this is not anyone's fault—the features promised by `hx-boost` are impossible.
`hx-boost` uses the JavaScript [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API), which exists to let single-page apps (SPAs) hook into session management functionality, most notably the browser's forward and back buttons.
In practice, this is virtually impossible to get right, and is so annoying to implement that htmx creator Carson Gross made [a meme](https://htmx.org/img/memes/javascripthistory.png) about it.

The core problem is that with normal page navigation, each link you click resets the JavaScript environment and triggers a full set of page [lifecycle events](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event).
This is a very good thing.
It means that every additional script you include on the page has a standardized way to keep track of what's happening.
If you replace this process with an ad-hoc, scripting-based navigation, you remove access to that common language for every other library on your page.
You also initiate a long-lived JavaScript environment that is likely to eventually enter a bad state of some kind.

This problem is inherent to SPAs, and it can only be resolved by not writing SPAs.
So don't use the attribute that turns your htmx site into an SPA.

## What should I do instead?

Use [regular links](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a). `hx-boost` promises to enhance the experience of a regular link; skip the middleman and just use them.

[Regular links are a better user experience and developer experience](@/blog/hard-page-load/index.md), full stop.

## What about the benefits of hx-boost?

The first time you use `hx-boost`, it feels magical to have the page update "seamlessly" like that, but you can achieve all the same benefits, without the headaches, using browser features.

### Send cache headers to re-use CSS and JS across page loads

Basically all static file servers support [ETags](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag).
When the server sends the browser a file, it can also send a unique string that identifies *that version* of the file.
The next time you try to load that file (after, for instance, navigating to a new page that uses the same CSS), the browser asks your server, "is it still this one?", and sends that ETag string.
If the file hasn't changed, the server just responds with a [304 Not Modified](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) header and the browser users its cached version.

In most cases, this is process adds essentially nothing to your load times.
The browser has to talk to the server anyway to get whatever info is on the next page, and it's [re-using the same TCP connection](https://www.rfc-editor.org/rfc/rfc2616#section-8.1) to do so.
The GET -> 304 back-and-forth is a handful of extra bytes on an already-open socket.

But if you don't want the browser to even *ask*, you can do that do by setting a [cache control header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#response_directives).

Here's how I load htmx in all the websites where I use it.
We'll use version 1.9.3 as an example.
I include a script tag like this in the header:

```html
<script src="/htmx-1.9.3.js"></script>
```

When the user loads the page for the very first time, their browser sends the HTTP request `GET /htmx-1.9.3.js` to my server.
The server will send back something like this in response:

```http
HTTP/2 200
accept-ranges: bytes
cache-control: public, max-age=31536000
last-modified: Fri, 06 Sep 2024 22:09:43 GMT
etag: W/"24b79-191c962d458"
content-type: application/javascript; charset=UTF-8
```

That says: "download htmx 1.9.3 from my server exactly once, and then never ask me for it again for *a full calendar year*."
From that point on, for one year, every time that browser loads a page at the same domain that includes htmx 1.9.3, the browser won't even ask the server for it, it'll just use the saved version.
If I want to upgrade everyone to a new version, I just change the version number in the URL:

```html
<!-- From this... -->
<script src="/htmx-1.9.3.js"></script>

<!-- ...to this -->
<script src="/htmx-1.9.4.js"></script>
```

The next time each of my users loads that page, their browsers will see that the page requires a new file it doesn't have, and ask for the server for it again.

If I don't even want to include a version number—maybe for a file like `stylesheet.css`—I can use a URL query.

```html
<!-- The browser will consider these two different files,
      but your server will know that they're the same -->
<link rel="stylesheet" href="/stylesheet.css">
<link rel="stylesheet" href="/stylesheet.css?id=1">
```

Again, basically every static file server supports this pattern.

### Use same-origin links to get partial page updates

This website ([unplannedobsolescence.com](/)) uses exclusively regular links, and if you click around up top you'll see that the header largely stays in place.
This happens automatically now, for same-origin links to pages with the same structure and stylesheets (like I showed you above).

Here's the Chrome team [announcing this feature](https://developer.chrome.com/blog/paint-holding):

> Try Paint Holding in Chrome Canary (Chrome 76) and let us know what you think. Developers shouldn't have to worry about making any modifications to their pages to take advantage of it.

Chrome 76 came out four years ago, in 2019.
Everyone who built their website with regular links got a significant, free performance upgrade to their website pushed out to billions of people;
the same is not true for everyone who tried to replace that functionality with JavaScript.

### Leverage HTML for free performance upgrades

Using standard HTML features allows the browser to optimize performance and UX in ways that JavaScript is categorically incapable of.
Every time the browser updates it is getting better at loading, parsing, and rendering webpages.
Page history, loading bars, the back button, the cancel button, the URL bar, etc., all work correctly, by default, every time, on every browser.

[In the long run, the browser always wins.](@/blog/hard-page-load/index.md#in-the-long-run-the-browser-always-wins)


## Why does hx-boost exist then?

htmx was created during a period in which it seemed like SPAs were the inevitable future of web development.
To compete in that environment, it had to demonstrate that it could replicate what most people considered to be the killer feature of SPAs: not repainting the whole page.
If this was ever necessary—I'm skeptical—it's sure not necessary anymore.

Now that htmx has proven itself in the mindshare ecosystem, and developers are starting to trust multi-page websites again, I think the time has come to make the harder, but ultimately more impactful case: HTML and HTTP have the features required to build the vast, vast majority of website functionality; they're easier to use than the scripting alternatives, and they last longer with much less maintenance.

<aside>
Users always trusted multi-page websites, by the way.
We're just now starting to listen to them again.
</aside>

Building good websites requires dropping the sugar high of `hx-boost` and saying "here's how to use a cache header."

## Is there ever a time I should use htmx to make an SPA?

My friend [Aram](https://aramzs.xyz/) made a website called [Song Obsessed](https://songobsessed.com) that has a persistent music player which holds its state even as you navigate around the site.
`hx-boost` is a good fit for this because it allows you to construct your website as a series of URLs; you can just slap `hx-boost` on everything and, with a little tweaking, you can get htmx to leave the music player alone while replacing the rest of the page.
You still lost the reliability inherent in the hard page load, but you get genuinely novel functionality in exchange, which is a good trade in this case.
Until HTML has an API to keep live content persistent across page navigations, some SPA functionality is required to make that happen.

SPAs are an <em>advanced</em> tool that the industry deceptively marketed as a simple one.
Aram is a highly experienced web developer who's using `hx-boost` to push the boundaries of what's possible with page navigations;
Most people, who just want to add a little interactivity to their webpage, should [stick with the simplest tool available](https://grugbrain.dev/#grug-on-complexity): a [regular link](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a).


*Thanks to Carson Gross his for feedback on a draft of this article. Comments available on [lobste.rs](https://lobste.rs/s/1uv7e4/less_htmx_is_more)*

# Notes

* [Triptych](https://alexanderpetros.com/triptych/)—the HTML proposals that Carson and I are working on—would render htmx obsolete for the type of website I describe here.
More advanced htmx features, like the ones used to great effect by [David Guillot and Contexte](https://david.guillot.me/en/posts/tech/following-up-mother-of-all-htmx-demos/), will still require htmx for the foreseeable future.
* To add PUT (and DELETE) support to "regular" forms with htmx, add [`hx-put`](https://htmx.org/attributes/hx-put/) to the form, and then have the server respond with status code 200 and an [`HX-Redirect`](https://htmx.org/headers/hx-redirect/) header;
instead of doing partial page replacement, htmx will tell the browser to do a full-page navigation.
This mimics the POST-Redirect-GET pattern, but uses a header instead of a 303 response.
* Ideally, htmx would be able to intercept a normal 303 response and use the `location` header, instead of a custom header, but because of limitations in the fetch API (`manual` redirects [hide all the headers](https://developer.mozilla.org/en-US/docs/Web/API/RequestInit#redirect)), it can't.
I don't totally understand what security purpose this serves, to be honest, but it's a bit of a shame, because it means that [you can't make a proper polyfill](https://github.com/alexpetros/triptych?tab=readme-ov-file#limitations) for PUT and DELETE forms.
* Both [turbo](https://dev.37signals.com/a-happier-happy-path-in-turbo-with-morphing/) and [datastar](https://data-star.dev/essays/another_dependency#fn:1) use Carson's [idiomorph](https://github.com/bigskysoftware/idiomorph) algorithm to merge updates into the page, but Carson ended up rejecting idiomorph as the default merging algorithm for htmx, because it was too complicated—even though he's the one who created it in the first place!
The default [htmx swap strategy](https://htmx.org/attributes/hx-swap/) is to just wipe away what's inside the `innerHTML` and replace it with the response—not unlike how the default page navigation is to wipe away the environment and give you a fresh one.
Simple; effective.

