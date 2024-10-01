+++
title = "Do Not Use Hx-boost"
description = ""
date = 2024-10-01

[extra]
hidden = true
+++

Hello!

You're probably here because you asked me (or someone who agrees with me) for help fixing a problem with the [`hx-boost`](https://htmx.org/attributes/hx-boost/) attribute.
Here's the simplest answer: do not use `hx-boost`.
It's doing nothing but getting in your way, and any problem you think it's solving can be solved much more simply using other means.

First of all, just try it.
Please.
Literally just remove `hx-boost=true` from all your attributes and see if it fixes every single problem you have.
Then come back and read the rest of the article.

## In case I don't have the full context, what exactly is hx-boost?

`hx-boost` is a feature of the [htmx JavaScript library](https://htmx.org/).
It's a single attribute that converts a "regular" link into a "boosted" link.

```html
<!-- normal link -->
<a href=example.com>Example</a>

<!-- boosted link -->
<a href=example.com hx-boost=true>Example</a>
```

Instead of doing a full page navigation when the "boosted" link is clicked, htmx will issue an HTTP request to the link's URL and replace the `<body>` of the page with the content of the response.
In theory, this perfectly mimics the functionality of a normal link, but feels "smoother" due to only partially repainting the page.
It is sometimes billed as an easy entrypoint into htmx.

## Why shouldn't I use it?

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

Use regular links. `hx-boost` promises to replicate the experience of a regular link; skip the middle man and just use them.

## What about the benefits of hx-boost?

The purported benefits of `hx-boost` can be better achieved through other means:

### I don't want to re-download JS and CSS on each click
Basically all static file servers support [ETags](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag).
When the server sends the browser a file, it can also send a unique string that identifies *that version* of the file.
The next time you try to load that file (after, for instance, navigating to a new page that uses the same CSS or JS), the browser asks your server, "is it still this one?", and sends that ETag string.
If the file hasn't changed, the server just responds with a [304 Not Modified](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) header and the browser users its cached version.

In most cases, this is process is essentially instantaneous. The browser has to talk to the server anyway to get whatever info is on the next page, and it's [re-using the same TCP connection](https://www.rfc-editor.org/rfc/rfc2616#section-8.1) to do so.

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

If I don't even want to include a version number—maybe for a file like `stylesheet.css`—you can use a URL query.

```html
<!-- The browser will consider these two different files,
      but your server will know that they're the same -->
<link rel="stylesheet" href="/stylesheet.css">
<link rel="stylesheet" href="/stylesheet.css?id=1">
```

Again, basically every static file server supports this pattern.

### I don't want the whole page to repaint

If you have your cache headers set properly, browsers don't do this anymore.
This website ([unplannedobsolescence.com](/)) uses exclusively regular links, and if you click around up top you'll see that the header largely stays in place.

Here's the Chrome team [announcing this feature](https://developer.chrome.com/blog/paint-holding):

> Try Paint Holding in Chrome Canary (Chrome 76) and let us know what you think. Developers shouldn't have to worry about making any modifications to their pages to take advantage of it.

Chrome 76 came out four years ago, in 2019.
Everyone who built their website with regular links got a significant, free performance upgrade to their website pushed out to billions of people;
the same cannot be said for everyone who tried to replace that functionality with JavaScript.

## What's even the point of htmx then? Does htmx suck?

htmx is incredible and the beginning of a complete sea-change in how we build for the web. I am one of the htmx maintainers.

In my opinion, you should be using htmx to enable changes on the page that either:

1. Users would not expect to see on a refresh i.e. emphemeral fetches
2. Updates info that *would* be present on a new, full-page load

For example: if your page shows a baseball score, you might use htmx to update it live.
A full-page reload would obviously show the current score, but you don't need to be reloading the whole page for each pitch;
use htmx to update the count and the scoreboard.

You also currently need htmx (or an equivalent library) to enable support for PUT and DELETE on forms, which is among the [htmx-inspired features](https://alexanderpetros.com/triptych) that Carson and I are [working on getting into HTML proper](https://alexanderpetros.com/triptych/form-http-methods).

<aside>
One of the reason I am familiar with the limitations of the History API is because the Triptych polyfill <a href="https://github.com/alexpetros/triptych?tab=readme-ov-file#limitations">has them too</a>.
</aside>

## Why does it exist then, if you think it's so bad?

htmx was created during a period in which it seemed like SPAs were the inevitable future of web development.
To compete in that environment, it had to demonstrate that it could replicate what most people considered to be the killer feature of SPAs: not repainting the whole page.
I believe, in 2024, that [this creates a worse experience for both users and developers](@/blog/hard-page-load/index.md).

Now that htmx has proven itself in the mindshare ecosystem, and people are more sick of SPAs, I think the time has come to make the harder, but ultimately more impactful case: HTML and HTTP have the features required to build the vast, vast majority of website functionality; they're easier to use than the scripting alternatives, and they last longer with much less maintenance.

Building good websites requires dropping the sugar high of `hx-boost` and saying "here's how to use a cache header."

## What is htmx creator Carson's take on this?

Whenever I bring it up, he says: "I like hx-boost."

I think his perspective is that `hx-boost` is too important to the htmx funnel to explicitly disavow.
I don't know if I event disagree with that, and either way, I would never advocate for it to be removed, because backwards compatibility is more important.

But I'm writing this because people always ask me for help with `hx-boost` problems, and the only way to fully resolve those is to stop using it.

## Is there ever a time I should use hx-boost?

My friend [Aram](https://aramzs.xyz/) made a website called [Song Obsessed](https://songobsessed.com) that has a persistent music player which holds its state even as you navigate around the site.
`hx-boost` is a good fit for this because it allows you to construct your website as a series of URLs; you can just slap `hx-boost` on everything and, with a little tweaking, you can get htmx to leave the music player alone while replacing the rest of the page.
You still lost the reliability inherent in the hard page load, but you get genuinely novel functionality in exchange, which is a good trade.

Until HTML has an API for you to keep content like persistent across page navigations, `hx-boost` is a decent way to get that done.
But there is a better-than-decent chance that you came to htmx not to replicate MySpace, but to accomplish something much simpler (simplicity is, after all, [a core virtue](https://grugbrain.dev/) widely espoused by the htmx community).
To that end, `hx-boost` should be a understood as a finnicky tool, only to be broken out in very specific circumstances.
