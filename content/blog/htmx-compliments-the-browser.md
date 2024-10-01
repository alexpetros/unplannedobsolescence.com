+++
title = "htmx Compliments the Browser"
description = "You just need to set your cache headers correctly (and start trusting the browser again)."
date = 2024-10-01

[extra]
hidden = true
+++

Hello!

You're probably here for one of two reasons:

* You're new to [htmx](https://htmx.org/) and struggling with how to structure your website to make it feel responsive
* You asked for help fixing a problem with the [`hx-boost`](https://htmx.org/attributes/hx-boost/) attribute

I believe that htmx is beginning of a sea-change in how we build for the web (this is why I volunteer as one of the maintainers).
I do, however, have a small problem with the way that we teach it to beginners, which can cause the two stumbling blocks above.

## How should we teach it beginners?

In my opinion, most websites should be using htmx for page updates that:

1. Users would not expect to see on a refresh i.e. emphemeral fetches
2. Add info that *would* be present on a new, full-page load

Everything else should use regular links and regular forms that do standard, full-page navigations.

<aside>
You also currently need htmx (or an equivalent library) to enable support for PUT and DELETE on forms.
More in that in the <a href="#notes">notes section.</a>
<!-- But, in most cases, you should have the server respond with an `HX-Redirect` header so that, instead of doing a partial page replacement, the browser does a full-page navigation. -->
</aside>

Let's say you're making a website that shows today's baseball games, and you want it to update the stats live.
Each game should live at its own URL, clicking that URL should load the full page with the current count, scoreboard, and stats.
You can then use htmx to update the pitch count, the scoreboard, and the stats each time something happens.
Your website's home page might have all the currently-playing games on it, with just the number of runs scored in each game; those can update with htmx too.
Clicking on the game should navigates to that game's page, and loads the more detailed view.

What I'm trying to emphasize with this example is that while htmx is amazing for targeted page updates, I highly discourage using it to take over *all* page navigation.
Exactly what merits a targeted update versus a link to a new page depends on what you're building, but you should have a mental model that distinguishes between them in some capacity.

<!-- which is among the [htmx-inspired features](https://alexanderpetros.com/triptych) that Carson and I are [working on getting into HTML proper](https://alexanderpetros.com/triptych/form-http-methods). -->

Unfortunately, a lot of the beginner guides, including the *Hypermedia Systems* book, suggest that you can get started easily by "upgrading" your links with `hx-boost`.
I think this is a bad idea.

<!-- <aside> -->
<!-- One of the reason I am familiar with the limitations of the History API is because the Triptych polyfill <a href="https://github.com/alexpetros/triptych?tab=readme-ov-file#limitations">has them too</a>. -->
<!-- </aside> -->

## In case I don't have the full context, what exactly is hx-boost?

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
If you replace this process with an ad-hoc, scripting-based navigation, you remove access to that common language for every other library on your page, and you also initiate a long-lived JavaScript environment that is likely to eventually enter a bad state of some kind.

## What should I do instead?

Use [regular links](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a). `hx-boost` promises to enhance the experience of a regular link; skip the middleman and just use them.

## What about the benefits of hx-boost?

The first time you use `hx-boost`, it feels magical to have the page update "seamlessly" like that, but you can achieve all the same benefits, without the headaches, using the browser features.

### Send cache headers to re-use CSS and JS across page loads

Basically all static file servers support [ETags](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag).
When the server sends the browser a file, it can also send a unique string that identifies *that version* of the file.
The next time you try to load that file (after, for instance, navigating to a new page that uses the same CSS or JS), the browser asks your server, "is it still this one?", and sends that ETag string.
If the file hasn't changed, the server just responds with a [304 Not Modified](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) header and the browser users its cached version.

In most cases, this is process adds essentially nothing to your load times.
The browser has to talk to the server anyway to get whatever info is on the next page, and it's [re-using the same TCP connection](https://www.rfc-editor.org/rfc/rfc2616#section-8.1) to do so.
The GET -> 304 back-and-forth is a handful of extra bytes on an already-open socket.

But if you don't want the browser to even *ask*, you can do that do by setting a single cache header.

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
From that point on, for one year, every time that browser loads webpage at that domain that includes htmx 1.9.3, the browser won't even ask the server for it, it'll just use the saved version.
If I want to upgrade everyone to a new version, I just change the version number in the URL:

```html
<!-- From this... -->
<script src="/htmx-1.9.3.js"></script>

<!-- ...to this -->
<script src="/htmx-1.9.4.js"></script>
```

Then all my users' browses will consider it a new file and ask for the server for it again.

If I don't even want to include a version number—maybe for a file like `stylesheet.css`—I can use a URL query.

```html
<!-- The browser will consider these two different files,
      but your server will know that they're the same -->
<link rel="stylesheet" href="/stylesheet.css">
<link rel="stylesheet" href="/stylesheet.css?id=1">
```

Again, basically every static file server supports this pattern.

### Use same-origin links to automatically stop page repaints

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


## Why does hx-boost exist then, if you think it's so bad?

htmx was created during a period in which it seemed like SPAs were the inevitable future of web development.
To compete in that environment, it had to demonstrate that it could replicate what most people considered to be the killer feature of SPAs: not repainting the whole page.
I believe, in 2024, that [this creates a worse experience for both users and developers](@/blog/hard-page-load/index.md).

Now that htmx has proven itself in the mindshare ecosystem, and developers are starting to trust multi-page websites again, I think the time has come to make the harder, but ultimately more impactful case: HTML and HTTP have the features required to build the vast, vast majority of website functionality; they're easier to use than the scripting alternatives, and they last longer with much less maintenance.

<aside>
Users always trusted multi-page websites, by the way.
We're just now starting to listen again.
</aside>

Building good websites requires dropping the sugar high of `hx-boost` and saying "here's how to use a cache header."

## What is htmx creator Carson's take on this?

Whenever I bring it up, he says: "I like hx-boost."

I think Carson's perspective is that `hx-boost` is too important to the htmx funnel to explicitly disavow.
Curious beginners slap `hx-boost` onto their links and see an instant "smoothness" upgrade.
I don't know if I even disagree with that—it certainly is an easy way to get started, and maybe that's more important.
In any case, I would never advocate for it to be removed, because backwards compatibility is more important.


For what it's worth, my opposition to hx-boost stems from my own experience as a beginner.
hx-boost broke the back button in a way I didn't understand, and removing it fixed my problem.
This was my a-ha moment about "hard" links, and multi-page architectures in general: the ephemeral scripting environment reduces the surface area for complexity.

But I'm writing this because people frequently ask for help with `hx-boost` problems, and they deserve a fully-realized explanation for why I feel that the only way to properly resolve those problems is to stop using it.

## Is there ever a time I should use hx-boost?

My friend [Aram](https://aramzs.xyz/) made a website called [Song Obsessed](https://songobsessed.com) that has a persistent music player which holds its state even as you navigate around the site.
`hx-boost` is a good fit for this because it allows you to construct your website as a series of URLs; you can just slap `hx-boost` on everything and, with a little tweaking, you can get htmx to leave the music player alone while replacing the rest of the page.
You still lost the reliability inherent in the hard page load, but you get genuinely novel functionality in exchange, which is a good trade in this case.
Until HTML has an API for you to keep content like persistent across page navigations, `hx-boost` is a decent way to get that done.

This demonstrates the core problem with `hx-boost`: it's actually an <em>advanced</em> tool masquerading as a simple one.
Aram is a highly experienced web developer who's using `hx-boost` to push the boundaries of what's possible with page navigations;
for most people, who just want to add a little interactivity to their webpage, all `hx-boost` does is degrade the page's performance.

`hx-boost` should be a understood as a finnicky tool, only to be broken out in very specific circumstances, if you know what you're doing.
For most pages, [stick with simple](https://grugbrain.dev/#grug-on-complexity): a [regular link](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a).

# Notes

* htmx community member Delaney Gillilan has his own hypermedia framework called [datastar](https://data-star.dev/) which uses server-side events to drive page updates.
Each event from the server is processed by datastar and merged into the page in the appropriate place.
It's good to take on the complexity of DOM morphing if you're working on the kinds of real-time applications that Delaney does (I saw an amazing 3D graphics demo from him at UtahJS);
it's not a thing we should be burdening beginners and more traditional hypertext documents with.

* Both [datastar](https://data-star.dev/essays/another_dependency#fn:1) and [turbo](https://dev.37signals.com/a-happier-happy-path-in-turbo-with-morphing/) (from 37signals) use Carson's [idiomorph](https://github.com/bigskysoftware/idiomorph) algorithm to merge updates into the page, but Carson ended up rejecting idiomorph as the default merging algorithm for htmx, because it was too complicated!
The default [htmx swap strategy](https://htmx.org/attributes/hx-swap/) is to just wipe away what's inside the `innerHTML` and replace it with the response—not unlike how the default page navigation is to wipe away the environment and give you a fresh one.
Simple, but effective.

