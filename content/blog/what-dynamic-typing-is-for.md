+++
title = "What Dynamic Typing Is For"
description = "How dynamic typing makes DSL-driven development easy, and what can be done to bring static typing up to par."
date = 2025-10-12
+++

<style>
.languages {
  grid-template-columns: 1fr 1fr fit-content(60%);
}
</style>

*Unplanned Obsolescence* is a blog is about writing maintainable, long-lasting software.
It also frequently touts—or is, at the very least, not inherently hostile to—writing software in dynamically-typed programming languages.

These two positions are somewhat at odds.

## Static Typing is Better For Maintainability

Dynamically-typed languages encode less information.
That's a problem for the person reading the code and trying to figure out what it does.

This is a simplified version of an authentication middleware that I include in most of my web services:
it checks an HTTP request to see if it corresponds to a logged-in user's session.

```js
function authenticate(req) {
  const cookieToken = req.cookies['token']
  const user = req.db.get_user_by_token(cookieToken)

  if (user) {
    return user
  } else {
    throw new AuthorizationError()
  }
}
```

Pretty straightforward stuff.
The function gets a `token` cookie from the HTTP request, checks the database to see if that token corresponds to a user, and then returns the user if it does.
Line 2 fetches the cookie from the request, line 3 gets the user from the database, and the rest either returns the user or throw an error.

<!-- For instance, what type is `user`? -->
<!-- If you want the user's database ID, would that be `user.id` or `user.user_id`? -->
<!-- To answer this question you need to look at the implementation of `db.get_user_by_token`, and now we're entering a rabbit hole. -->

There are, however, some problems with this.
What happens if there's no `token` cookie included in the HTTP request?
Will it return `undefined` or an empty string?
Will `req.cookies` even exist if there's no cookies at all?
There's no way to know without looking at the implementation (or, less reliably, the documentation).

That doesn't mean there isn't an answer!
A request with no `"token"` cookie [will return `undefined`](https://expressjs.com/en/4x/api.html#req.cookies).
That results in a `get_user_by_token(undefined)` call, which returns `undefined` (the function checks for that).
`undefined` is a [falsy](https://developer.mozilla.org/en-US/docs/Glossary/Falsy) value in JavaScript, so the conditional evaluates to false and throws an `AuthorizationError`.

The code works and it's very readable, but you have to do a fair amount of digging to ensure that it works reliably.
That's a cost that gets paid in the future, anytime the "missing token" code path needs to be understood or modified.
That cost reduces the maintainability of the service.

Unsurprisingly, the equivalent Rust code is much more explicit.

```rust
fn authenticate(req: Request) -> AuthStatus {
  let cookie_token = match req.cookies.get("token") {
      Some(token) => token,
      None => return AuthStatus::Failure("Token not included in request")
  };

  match req.db.get_user_by_token(cookie_token) {
      Some(user) => AuthStatus::Success(user),
      None => AuthStatus::Failure("Could not find user for token")
  }
}
```

In Rust, the tooling can answer a lot more questions for me.
What type is `cookie_token`?
A simple hover in any code editor with an LSP tells me, definitively, that it's `Option<String>`.

Because it's Rust, you have to explicitly check if the token exists;
ditto for whether the user exists.
That's better for the reader too: they don't have to wonder whether certain edge cases are handled.

<aside>
It's possible to write sloppier Rust than this, but the baseline is quite a bit higher.
</aside>

Rust is not the only language with a strict, static typing.
At every place I've ever worked, the longest-running web services have all been written in Java.
Java is not as good as Rust at forcing you to show your work and handle edge cases, but it's much better than JavaScript.

Putting aside the question of which one I prefer to write, if I find myself in charge a production web service that someone *else* wrote, I would much prefer it to be in Java or Rust than JavaScript or Python.

## Web Development Has Lots of DSLs

Conceding that, *ceteris paribus*, static typing is good for software maintainability, one of the reasons that I like dynamically-typed languages is that they encourage a style I find important for web services in particular: writing to the DSL.

A DSL (domain-specific language) is programming language that's designed for a specific problem area.
This is in contrast to what we typically call "general-purpose programming languages" (e.g. Java, JavaScript, Python, Rust), which can reasonably applied to most programming tasks.

Most web services have to contend with at least three DSLs: HTML, CSS, and SQL.
A web service with a JavaScript backend has to interface with, at a *minimum*, four programming languages: one general-purpose and three DSLs.

<table class="as-grid-table languages">
  <tr><th>Language    <th>DSL? <th>Purpose
  <tr><td>HTML        <td>Yes  <td>Website layout <a href="/blog/behavior-belongs-in-html">and functionality</a>
  <tr><td>SQL         <td>Yes  <td>Data persistence and retrieval
  <tr><td>CSS         <td>Yes  <td>Website design
  <tr><td>JavaScript  <td>No   <td>Server logic and website functionality missing from HTML
</table>

If you have the audacity to use [something other than JavaScript](https://htmx.org/essays/hypermedia-on-whatever-youd-like/) on the server, then that number goes up to five, because you still need JavaScript to augment HTML.

<table class="as-grid-table languages">
  <tr><th>Language    <th>DSL? <th>Purpose
  <tr><td>HTML        <td>Yes  <td>Website layout <a href="/blog/behavior-belongs-in-html">and functionality</a>
  <tr><td>SQL         <td>Yes  <td>Data persistence and retrieval
  <tr><td>CSS         <td>Yes  <td>Website design
  <tr><td>Java        <td>No   <td>Server logic
  <tr><td>JavaScript  <td>No   <td>Website functionality missing from HTML
</table>

That's a lot of languages!
How are we supposed to find developers who can do *all this stuff*?

## Two Approaches to Language Proliferation

### Expanding The Bounds

The answer that a big chunk of the industry settled on is to build APIs so that the domains of the DSLs can be described in the general-purpose programming language.

Instead of writing HTML...

```html,name=HTML
<!DOCTYPE html>
<h1>Classic Movies</h1>
<p>Louis, I think this is the beginning of a beautiful website.</p>
```
...you can write JSX, a JavaScript syntax extension that supports tags.

```jsx,name=JSX
const header = <h1>Classic Movies</h1>
const paragraph = <p>
  Louis, I think this is the beginning of a beautiful website.
</p>
const page = <>
  {header}
  {paragraph}
</>
```

This has the important advantage of allowing you to include dynamic JavaScript expressions in your markup.
And now we don't have to kick out to another DSL to write web pages.
Can we start abstracting away CSS too?

Sure can! This example uses [styled-components](https://styled-components.com/).

```jsx, name=JSX
const Button = styled.button({
  color: 'gray',
})

const page = <>
  <h1>Classic Movies</h1>
  <p>Louis, I think this is the beginning of a beautiful website.</p>
  <Button>Round up the usual suspects.</Button>
</>
```

<aside>Sorry, I just saw Casablanca again recently. That's the last one.</aside>

This is a tactic I call "expanding the bounds" of the programming language.
In an effort to reduce complexity, you try to make one language express everything about the project.
In theory, this reduces the number of languages that one needs to learn to work on it.

<table class="as-grid-table languages">
  <tr><th>Language    <th>DSL? <th>Purpose
  <tr><td>SQL         <td>Yes  <td>Data persistence and retrieval
  <tr><td>JavaScript  <td>No   <td>Server logic, website layout, <br>website functionality, and website design
</table>

The problem is that it usually doesn't work.
Expressing DSLs in general-purpose programming syntax does not free you from having to understand the DSL—you can't actually use styled-components without understanding CSS.
So now a prospective developer has to both understand CSS and a new CSS syntax that only applies to the styled-components library.

<aside>
I got hit with that library in a job interview a while back, and I spent five minutes trying to figure out how to express <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/Child_combinator">child selectors</a> before the interviewer took pity on me and was like "don't worry, I can tell you know CSS."
Which I do!
Let me write it!
</aside>

<table class="as-grid-table languages">
  <tr><th>Language                <th>DSL? <th>Purpose
  <tr><td>HTML                    <td>Yes  <td>Website layout and functionality
  <tr><td>JSX                     <td>Yes  <td>Website layout and functionality
  <tr><td>SQL                     <td>Yes  <td>Data persistence and retrieval
  <tr><td>CSS                     <td>Yes  <td>Website design
  <tr><td>styled-components       <td>Yes  <td>Website design
  <tr><td>JavaScript              <td>No   <td>Server logic
</table>

<aside>
I suspect people are going to be more inclined to defend JSX than CSS-in-JS.
Do you <strong>really</strong> need to know HTML to write JSX?
Yes, unless you want to re-implement functionality that's built into <code>&lt;a></code>, <code>&lt;form></code> <code>&lt;details></code>, <code>&lt;input></code>, etc.
Many people waste enormous amounts of time and money doing exactly that.
</aside>

Not to mention, it is almost always a worse syntax.
CSS is designed to make expressing declarative styles very easy, because that's the only thing CSS has to do.

```css,name=CSS
button {
  color: gray;
}
```

Expressing this in JavaScript is naturally way clunkier.

```js,name=JS
const Button = styled.button({
  color: 'gray',
})
```

Plus, you've also tossed the web's backwards compatibility guarantees.
I picked styled-components because it's very popular.
If you built a website with styled-components in [2019](https://styled-components.com/releases#v4.4.0), didn't think about the styles for a couple years, and then tried to upgrade it in [2023](https://styled-components.com/releases#v6.0.2), you would be two major versions behind.
Good luck with the [migration guide](https://styled-components.com/docs/faqs#what-do-i-need-to-do-to-migrate-to-v6).
CSS files, on the other hand, [are evergreen](https://htmx.org/essays/no-build-step/).

Of course, one of the reasons for introducing JSX or CSS-in-JS is that they add functionality, like dynamic population of values.
That's an important problem, but I prefer a different solution.

### Building Good Boundaries

Instead of expanding the bounds of the general-purpose language so that it can express everything, another strategy is to build strong and simple API boundaries between the DSLs.
Some benefits of this approach include:

1. DSLs are better at expressing their domain, resulting in simpler code
1. It aids debugging by segmenting bugs into natural categories
1. The skills gained by writing DSLs are more more transferable

The following example uses a JavaScript backend.
A lot of enthusiasm for [htmx](https://htmx.org/) (the software library I co-maintain) is driven by communities like [Django](https://forum.djangoproject.com/t/adding-template-fragments-or-partials-for-the-dtl/21500) and [Spring Boot](https://github.com/wimdeblauwe/htmx-spring-boot) developers, who are thrilled to no longer be bolting on a JavaScript frontend to their website;
that's a core value proposition for [hypermedia-driven development](https://htmx.org/essays/hypermedia-driven-applications/).
I happen to like JavaScript though, and sometimes write services in NodeJS, so, at least in theory, I could still use JSX if I wanted to.

What I prefer, and what I encourage hypermedia-curious NodeJS developers to do, is use a [template engine](https://htmx.org/essays/web-security-basics-with-htmx/#always-use-an-auto-escaping-template-engine).
This bit of production code I wrote for an events company uses [Nunjucks](https://mozilla.github.io/nunjucks/), a template engine [I once (fondly!) called "abandonware" on stage](@/talks/building-the-hundred-year-web-service.md).
Other libraries that support [Jinja](https://jinja.palletsprojects.com/en/stable/)-like syntax are available in pretty much any programming language.
```html
<h2>Upcoming Events</h2>
<table>
<tr>
  <th>Name
  <th>Location
  <th>Date
  <th>Registration Deadline
</tr>

{% for event in events %}
<tr>
  <td><a href="/events/{{ event.event_id }}">{{ event.name }}</a>
  <td>{{ event.location }}
  <td>{{ event.date }}
  <td>{{ event.registration_deadline }}
</tr>
{% endfor %}
</table>
```

This is just HTML with basic loops (`{% for event in events %}`) and data access (`{{ event.name }}`).
I get very frustrated when something that is easy in HTML is hard to do because I'm using some wrapper with inferior semantics;
with templates, I can dynamically build content for HTML without abstracting it away.

<aside>
Nunjucks actually has no concept of HTML syntax; it's just providing the curly-brace functionality.
You could template anything you wanted with it.
</aside>

Populating this template in JavaScript is *so easy*.
You just give it a JavaScript object with an `events` field.

```js
const events = db.getUpcomingEvents()
req.render('events.html', { events })
```

That's not particularly special on its own—many languages support serialized key-value pairs.
This strategy really shines when you start stringing it together with SQL.
Let's replace that database function call with an actual query, using an interface similar to [`better-sqlite3`](https://github.com/WiseLibs/better-sqlite3).

```js
function getEvent(req) {
  const events = db.all(`
    SELECT event_id, name location, date, registration_deadline
    FROM events
    WHERE date start_date >= date('now')
    ORDER BY start_date ASC
  `

  req.render('events.html', { events })
}
```

I *know* the above code is not everybody's taste, but I think it's marvelous.
You get to write all parts of the application in the language best suited to each: HTML for the frontend and SQL for the queries.
And if you need to do any additional logic between the database and the template, JavaScript is still right there.

One result of this style is that it increases the percentage of your service that is specified declaratively.
The database schema and query are declarative, as is the HTML template.
The only imperative code in the function is the glue that moves that query result into the template: two statements in total.

<aside>
Declarative languages tend to have better backwards compatibility guarantees, but HTML and SQL in particular are phenomenal in this regard.
</aside>

Debugging is also dramatically easier.
I typically do two quick things to narrow down the location of the bug:

1. **CMD+U to View Source** - If the missing data is in the HTML, it's a frontend problem
2. **Run the query in the database** - If the missing data is in the SQL, it's a problem with the GET route

<aside>
JetBrains IDEs are especially good at running parameterized SQL queries straight from the embedded-string source.
</aside>

Those two steps are easy, can be done in production with no deployments, and provide excellent signal on the location of the error.

Fundamentally, what's happening here is a quick check at the two hard boundaries of the system:
the one between the server and the client, and the one between the client and the database.
Similar tools are available to you if you abstract over those layers, but they are lessened in usefulness.

Every web service has network requests that can be inspected, but putting most frontend logic in the template means that the HTTP response's **data** ("does the date ever get send to the frontend") **and functionality** ("does the date get displayed in the right HTML element?") can be inspected in one place, with one keystroke.
Every database can be queried, but using the database's native query language in your server means you can validate both the **stored data** ("did the value get saved?") **and the query** ("does the code ask for the right value?") independent of the application.

By pushing so much of the business logic outside the general-purpose programming language, you reduce the likelihood that a bug will exist in the place where it is hardest to track down—runtime server logic.
You'd rather the bug be a malformatted SQL query or HTML template, because those are easy to find and easy to fix.

When combined with the router-driven style described in [Building The Hundred-Year Web Service](@/talks/building-the-hundred-year-web-service.md),
you get simple and debuggable web systems.
Each HTTP request is a relatively isolated function call: it takes some parameters, runs an SQL query, and returns some HTML.

In essence, dynamically-typed languages help you write the least amount of server code possible, leaning heavily on the DSLs that define web programming while validating small amounts of server code via means other than static type checking.

## Raising the Inference Bar

To finish, let's take a look at the equivalent code in Rust, using [rusqlite](https://github.com/rusqlite/rusqlite), [minjina](https://github.com/mitsuhiko/minijinja), and a quasi-hypothetical server implementation:

```rust
#[derive(Serialize, Deserialize)]
struct Event {
    event_id: String,
    name: String,
    date: String,
    registration_deadline: String,
}

pub async fn get_events(req: Request) -> ServerResult {
  let profile = req.db.query_map("
    SELECT event_id, name location, date, registration_deadline
    FROM events
    WHERE date start_date >= date('now')
    ORDER BY start_date ASC
  ",
  [],
  |row| {
    let event = Event {
      event_id: row.get("event_id")?,
      name: row.get("name")?,
      date: row.get("date")?,
      registration_deadline: row.get("registration_deadline")?,
    };
    Ok(event)
  })?;

  let body = req.render("events.html")?;
  req.send(body)
}

```

I am again obfuscating some implementation details (Are we storing human-readable dates in the database? What's that universal result type?).
The important part is that this blows.

Most of the complexity comes from the need to tell Rust exactly how to unpack that SQL result into a typed data structure, and then into an HTML template.
The `Event` struct is declared so that Rust knows to expect a `String` for `event_id`.
The derive macros create a representation that minijinja knows how to serialize.
It's tedious.

<!-- But you also lose the obligation of specifying those conversions manually, which is very handy because SQL, JavaScript, and HTML all have different type systems (a topic for another blog post), and specifying those conversions is quite tedious. -->

Worse, after all that work, the compiler still doesn't do the most useful thing: check whether `String` is the correct type for `event_id`.
If it turns out that `event_id` can't be represented as a `String` (maybe it's a [blob](https://sqlite.org/datatype3.html)), the query will compile correctly and then fail at runtime.
From a safety standpoint, we're not really in a much better spot than we were with JavaScript:
we don't know if it works until we run the code.

Speaking of JavaScript, remember that code? That was great!

```js
const events = db.all(`
  SELECT event_id, name, location, date, registration_deadline
  FROM events
  WHERE date start_date >= date('now')
  ORDER BY start_date ASC
`

req.render('events.html', { events })
```

Now we have no idea what any of these types are, but if we run the code and we see some output, it's probably fine.
By writing the JavaScript version, you are banking that you've made the code so highly auditable by hand that the compile-time checks become less necessary.
In the long run, this is always a bad bet, but at least I'm not writing 150% more code for 10% more compile-time safety.

The "expand the bounds" solution to this is to pull everything into the language's type system: the database schema, the template engine, everything.
Many have trod that path; I believe it leads to madness (and toolchain lock-in).
Is there a better one?

I believe there is.
The compiler should understand the DSLs I'm writing and automatically map them to types it understands.
If it needs more information—like a database schema—to figure that out, that information can be provided.

Queries correspond to columns with known types—the programming language can infer that `events.name` is of type `SQLITE_TEXT`.
HTML has [context-dependent escaping rules](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#output-encoding)—the programming language can validate that `events.name` is being used in a valid element and escape it correctly.

With this functionality in the compiler, if I make a database migration that would render my usage of a dependent variable in my HTML template invalid, the compiler will show an error.
All without losing the advantages of writing the expressive, interoperable, and backwards-compatible DSLs the comprise web development.

Dynamically-typed languages show us how easy web development can be when we ditch the unnecessary abstractions.
Now we need tooling to make it just as easy in statically-typed languages too.

# Notes
*Thanks to [Meghan Denny](https://mlog.nektro.net/) for her feedback on a draft of this blog.*

* Language extensions that just translate the syntax are alright by me, like generating HTML with [s-expressions](https://github.com/weavejester/hiccup), [ocaml functions](https://yawaramin.github.io/dream-html/), or [zig comptime functions](https://github.com/nektro/zig-pek). I tend to end up just using templates, but language-native HTML syntax can be done tastefully, and they are probably helpful in the road to achieving the DX I'm describing; I've never seen them done well for SQL.
* [Sqlx](https://github.com/launchbadge/sqlx) and [sqlc](https://docs.sqlc.dev) seem to have the right idea, but I haven't used either because I to stick to SQLite-specific libraries to avoid async database calls.
* I don't know as much about compilers as I'd like to, so I have no idea what kind of infrastructure would be required to make this work with existing languages in an extensible way. I assume it would be hard.

