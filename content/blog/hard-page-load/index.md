+++
title = "Who's Afraid of a Hard Page Load?"
description = ""
date = 2024-07-17
+++

While I'm not going to settle the Single-Page Web Application (SPA) debate in a blog post, there is
one claim about SPAs that routinely goes unchallenged, and it drives me nuts: that users prefer
them because of the "modern," responsive feel.

SPAs achieve their signature feel using partial page replacement: adding or removing DOM elements
instead of loading a new page. Partial page replacement is a very useful feature—I'm [working on an
HTML standards proposal](https://github.com/alexpetros/triptych) for it right now—but SPAs typically
use them for *everything*, including page navigation, which causes a lot of problems.

The way this works is that rather than letting the browser load a new page when the user clicks an
`<a>` tag, SPAs simulate page navigation by fetching with JavaScript, updating the page, and using
the History API to edit the browser's URL bar. [NextJS](https://nextjs.org/) and [React
Router](https://reactrouter.com/) work this way, as does [SvelteKit](https://kit.svelte.dev/). Even
the hypermedia libraries support this paradigm, with htmx's
[`hx-boost`](https://htmx.org/attributes/hx-boost) and Hotwire's [Turbo
Drive](https://turbo.hotwired.dev/handbook/drive).

In theory, avoiding "hard" page navigations has the following benefits:
- The app can make instant UI changes to reflect the user's click, and fill in information from the
  network request when it completes.
- The whole page doesn't repaint, i.e. the header and navigational links might remain in place while
  only the middle of the page changes. This avoids the blank screen that users often see while
  waiting for a new page to load.
- It allows for fancier transitions between pages.

<aside>
This discussion only applies to web applications that can be modeled with
pages, as opposed to something like Google Maps or RuneScape. But, web pages are a very flexible
paradigm, and the chances that you're working on web content that cannot be modeled with pages are
very slim.
</aside>

What this does is essentially abstract away the concept of a link, and make the web page feel more
like an application on your phone. No longer are you navigating web pages, you're moving around an
app. I have a number of problems with this, but purely from a UX standpoint, it's a massive
disservice to web users.

## Managing the network

Every day I ride the New York City Subway. For my carrier, most of the stops have cell service, and
most of the tunnels between stops do not. When I read web pages while riding, I am *keenly* aware
that if I click a link while I don't have service, not only will the page fail to load, I will
probably also lose access to the one I'm currently reading. Everyone who uses a web browser
understands this behavior on some level. So I avoid clicking links until I'm at a stop.

<aside>
I use the subway as an example to highlight that managing unreliable internet is a daily occurrence
even in the most urban environments. Naturally, this concern is magnified in rural areas, which is
why I'm deeply skeptical of the claim that SPAs somehow benefit people with slow or unstable
internet connections.
</aside>

Occasionally though, I'll mis-time it, and click a link right as the subway is pulling out of a
stop: the page fails to load, and now I'm looking at a blank screen. In that situation, I much
prefer to be on a traditional website than an SPA. On a website like Wikipedia, one that uses hard
links and full page loads, then there's a decent chance that the browser can save me: the back
button will usually load the cached version of the page I was just on.

If it's an SPA, however, in all likelihood clicking the back button will take me a different, mostly
blank page, and now I'm just stuck. When the internet comes back, I'll refresh the page and
hopefully land in the same place, but maybe not. In fact, my whole attitude towards a website
changes if feels like an SPA. Subconciously, I know that I have to baby it, and only use it in the
most optimal network conditions. The smoothness of a web application is an anti-indicator of its
reliability and predictability as a web page.

That anti-indicator holds even in situations without unreliable internet. As a user, I'm always
much happier when presented with a form that is entirely on one page, or has a "hard" submit button
for each step that takes me to a new page, as opposed to a "seamless" form that exists as a blob of
JS state. The former has relatively predictable submit, autocomplete, and back button behavior,
while the latter varies widely by implementation.

Maybe you don't ride the subway. But you've probably driven on a highway with spotty service, or had
a bad Wi-Fi connection, or gotten on a plane, or been inside a basement with weirdly thick walls.
Everyone has had to navigate the web under less-than-ideal network conditions, and you quickly
develop an intuition for which websites will be resilient to them.

<!-- While I can't prove it, I am reasonably confident that users have some insight into whether they are -->
<!-- going to get the Wikipedia experience or the "back button borks the entire app" experience -->

## The web has seams, let them show

Developers are naturally inclined to make their applications feel more responsive, and when they
test their SPA, it feels like a more natural experience than a clunky old web page. But this
instinct is usually incorrect, because most websites need to hit the network in response to user
actions.

When a user clicks a link, they want whatever information was at that link—which their device
will have to make a network trip to discover. When a user submits a form, they need to know whether
or not that information was saved to the server, which their device will have to make a network trip
to accomplish.

I suppose there's a version of the web that pre-fetches every possible page for you—and that might
feel pretty instantaneous. But there's no world where that works for user-submitted data, because
the only thing I care about as a user is that *the data actually got submitted*. If I submit a form
to a website, the website optimistically and instantaneously shows me that the submission
succeeded, and I later find out that it didn't, I am **mad**.

<aside>
Have you ever refreshed a page to make sure that your information *really* got saved? Why did you
feel the need to double-check?
</aside>

The friction involved with a hard page load doesn't exist because web developers are too lazy to do
performance work—it reflects a real, physical limitation in the system that is beyond the ability of
one developer, and possibly humanity, to overcome. SPAs not only fail to remove the need for the
network call, they diminish the user's ability to manage when that network call is made, and [handle
failure cases](https://intercoolerjs.org/2016/05/08/hatoeas-is-for-humans.html).

Discussions of user agency in software are often very... optimistic about how much users want to
exercise that agency. But agency comes in many forms. When I was in 5th grade, I would load up
[GameFAQs guides for Final Fantasy
III](https://gamefaqs.gamespot.com/ds/924897-final-fantasy-iii/faqs) on my iPod Touch before a road
trip, and in the car I'd make sure not navigate away from the page, or I'd lose the guide. When I
avoid clicking links between subways stops, I'm building on behavior I learned as a child, not as a
software engineer.

## In the long run, the browser always wins

I suspect that the primary impetus for this smoothness is commerce, or something I call
"casino-driven development." As my Papou used to tell me, casinos do not have clocks because clocks
remind you that time is passing; the casino would like you to forget that time is passing, because
they make more money the longer you remain in the casino. In the ad-based internet attention
economy, the website would like to keep you in their casino as long as possible-the less that
you're reminded you're on the web, where clicks usually require waiting, the better.

Internet folklore has it that, in the 2000s, Amazon and Google research discovered that for each
<math>X</math> additional millisecond of page load latency they lost <math>Y</math> customers and
therefore <math>Z</math> dollars. I can't find any reliable sources for this, but the logic is
sound. Some percentage of people will give up the longer it takes to see a result, and at that
scale, that percentage translates into a lot of lost money.

Here's the problem: your team almost certainly doesn't have what it takes to out-engineer the
browser. The browser will continuously improve the experience of plain HTML, at no cost to you,
using a rendering engine that is orders of magnitude more efficient than JavaScript. To beat that,
you need to be continuously investing significant engineering effort into cutting-edge application
work.

Some things you have to consider with SPAs:
- What happens when users refresh the page?
- What happens when users click the back button?
- What happens when users click the back button twice?
- What happens when users click the back button twice, the forward button once, and then the back
  button again?
- What happens when users try to open a link in a new tab?
- What happens when users users copy the link from the address bar and send it to a friend?
- Where does the page focus go when it navigates?

You can engineer your way out of basically all the problems I've described here, but it takes
enormous effort. And maintenance on the pile of libraries required to get back basic browser
features like "back button navigation" on your SPA [is a new fixed cost, paid for with your
time](https://htmx.org/essays/no-build-step/). If you use hard page loads, those things not only
work for free, they work forever, and they work in exactly the way the user expects and desires.

<aside>
Hard page loads also reset the JavaScript environment every time, drastically reducing the surface
area for memory leaks.
</aside>

At the time of this writing, the [NextJS showcase](https://nextjs.org/showcase) lists Nike's
shopping platform as one of their successes. If you are literally Nike, and throwing millions at
making your shopping portal slightly more responsive could result in tens of millions of revenue, by
all means take a crack at it. I, personally, am dubious that the math typically pencils out, even
for Nike, but I concede that it's at least plausible that you will deliver a networked experience
that is a hair quicker than what the default HTML can do, and reap the rewards.

<aside>
Here I'm going to be annoying and note that the Nike website is kinda slow.
</aside>

Meanwhile, the browser marches on, improving the UX of every website that uses basic HTML semantics.
For instance: browsers often *don't* repaint full pages anymore. Try browsing
[Wikipedia](https://en.wikipedia.org/wiki/Web_browser) (or [my blog](/)) on a decent internet
connection and notice how rarely the common elements flash (I can't find *any* documentation for
this feature, but it definitely exists). And, if the connection isn't fast, then the browser shows
a loading bar! It's a win for users, and one of the many ways that sticking with the web primitives
rewards developers over time.

So if you're a bank, or a government, or pretty much anyone with engineering resources short of
"limitless," you will likely be better served by sticking to hard page loads (and the default HTML
capabilities) as much as possible. It's dramatically easier to implement and benefits from browser
performance and security improvements over time. For page responsiveness improvements, try tweaking
your cache headers, scrutinizing the JavaScript you send to the client, and optimizing your CDN
setup. It always pays off in the long run.

## Bonus: A Good Use of SPAs

When I worked at the Washington Post, I worked on the interactive map that they used for live
election night coverage. [Watch my former boss, Jeremy Bowers, clicking around it the
livestream](https://www.youtube.com/live/czuu6s0gew4?si=Ch_Lp0YS1iBzyIYN&t=5628). Here's me and
[Dylan Friedman](https://dylanfreedman.com/), in front of an early version:

<figure>
  <img src="/blog/hard-page-load/alex-dylan-election-map.jpg"
       width=500
       alt="Alex Petros and Dylan Friedman in front of a big screen with a gray map on it,
       at the Washington Post offices"
       >
  <figcaption>
    I had to leave this project after like 6 weeks and <a href="https://www.brmayes.com">Brittany</a>
    took my place. As you can see, it improved dramatically after I left.
  </figcaption>
</figure>

That's a giant SvelteKit app! The map GUI is controlled by a [Svelte
store](https://svelte.dev/docs/svelte-store), and, if I remember correctly, a websocket updates the
votes totals in the background. When you click on a US State, it shows a close-up of that
state and all the election info that had come in so far.

This is a great use of a reactive UI framework, because the data stored on the client doesn't
update in response to user actions, it updates in response to new election results. The clicking
should be instantaneous, and the UI should live entirely on the client, because they can!

And it's remarkable that you can compete with very expensive interactive map products using nothing
but a browser, open source libraries, and a couple months of engineer-time.

I had so much fun learning Svelte for this that I used to as the basis for
[AYTA](https://areyoutheasshole.com/). If I were doing AYTA again though, I would definitely use
htmx.

*Thanks to [Mani Sundararajan](https://www.itsrainingmani.dev/) for his feedback on a draft of this
post.*

# Notes
- When *is* a good time to do partial page replacements? Either a) to add new information that would
  be there after a refresh, because it reflects the current state of the resource, e.g. a
  live-updating baseball score or b) as a result of actions that the user understands are ephemeral,
  and wouldn't expect to see after a refresh, like a dialog box.
- I am generously assuming that the SPA psuedo-navigation actually does use `<a>` tags. For a while
  that was not really incentivized by SPA frameworks, and people would just use `<div>`s for
  everything, but this has definitely gotten better lately.
- Ironically, [Triptych](https://github.com/alexpetros/triptych) has to simulate full-page
  navigations with partial page replacements and the history API, exactly the same way that hx-boost
  does, and is subject to the same inherent bugginess and lack of isolation. This is a limitation of
  the tools available in userland, and a big reason why these proposals should be supported
  natively, rather than in a library.
- Earlier, I said that actions that do require a round-trip to server should just use one, but the
  inverse applies as well: ideally, actions that do not required a round-trip to the server wouldn't
  use one. A good example of this is form validation. In the htmx world, sometimes [returning a new
  form with inline validation errors](https://htmx.org/examples/inline-validation) is "good enough,"
  (you always have to validate on the server, after all) but that experience can clearly be improved
  by having the validation occur without a network request. I usually wouldn't use an SPA just for
  client-side validation, but we can acknowledge that they are better at it right now.
- Further reading:
  - ["A Response To 'Have Single-Page Apps Ruined the Web?'"](https://htmx.org/essays/a-response-to-rich-harris/), Carson Gross
  - ["The Market For Lemons"](https://infrequently.org/2023/02/the-market-for-lemons/), Alex Russell

