+++
title = "The Mostly True Naming Rule"
description = "A common-sense naming convention that usually works."
date = 2025-04-17

[extra]
hidden = true
+++

Naming things properly is [very hard to do](https://martinfowler.com/bliki/TwoHardThings.html), so, as programmers, we come up with little rules to help us.
These rules are often inconsistent.

* Variables should be snake case (e.g. `last_name`) in [Python](https://peps.python.org/pep-0008/#function-and-variable-names) but camel case (e.g. `lastName`) in [JavaScript](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide/Code_style_guide/JavaScript)
* Names should be snake case in Python, except [classes](https://peps.python.org/pep-0008/#class-names) and [exceptions](https://peps.python.org/pep-0008/#exception-names), which are camel case
* Constants should be all caps in [Java](https://www.oracle.com/java/technologies/javase/codeconventions-namingconventions.html) but not [Scala](https://docs.scala-lang.org/style/naming-conventions.html#constants-values-variable-and-methods)

And these are all relatively similar programming languages.
Naming conventions start to diverge wildly when you start talking about languages like SQL, or HTML, or COBOL.

[Reasonable people](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds) understand that these rules [are more what you'd call guidelines](https://www.youtube.com/watch?v=k9ojK9Q_ARE), and that being consistent in your conventions is generally the most important thing.
I do have a naming rule that I like, though, one which is mostly applicable everywhere.

<center>
<p><strong>Do not give multiple names to the same thing.</strong>
</center>

Like all rules, it often comes into conflict with other rules, but I find this one usually wins.

## Case Study: Outdoor Trips

I have a production application that manages a college's outdoor trips program.
It has an SQL table that catalogs the gear that students going on the trip have requested to borrow (backpacks, headlamps, things of that nature);
this table is called `member_gear_requests`.
I named it this because there is also a table called `trip_members` that holds the students going on a particular trip.
Trip **members** request **gear**, therefore, `member_gear_requests`.
Simple enough.

At some point while building the application, I decided that the term "member gear" sounded kind of weird.
Trips have two types of gear: gear that everyone shares (like a tent) and gear that belongs to each person (like a backpack).
In the frontend, I called the two lists "Group Gear" and "Individual Gear".

You might be wondering: how does "member gear," as it's called in the database, become "individual gear", as it's called in the frontend?

I've never tried to answer this, so let's take a look together, going backwards from the HTML template.

```jinja,name=trip-card.njk
<h3>Individual Gear</h3>
<table class="gear">
  {% for item in member_requested_gear %}
  <tr><th>{{ item.name }}<td>{{ item.quantity }}
  {% endfor %}
</table>
```

Okay well that's not so bad.
There's an `<h3>` header that says "Individual Gear" and then a template variable called `member_requested_gear`.
Perhaps the entire application refers to this concept as "member gear," and then just puts an "Individual Gear" header on top of it.
Not ideal, but certainly reasonable.

Where does the data for that line come from?

```js,name=trip-card.js
trip.member_requested_gear = memberRequestedGear
```

Oh, uh, sure.
I guess I wanted to maintain JavaScript and HTML casing conventions (JS is camel case, HTML is... more complicated).
Where does `memberRequestedGear` get set?

```js,name=trip-card.js
const memberRequestedGear = gear.getIndividualRequestedGear(req.db, tripId)
```

Oh God no.
"Individual Gear" again?
You mean it __*switches back and forth?*__

And, of course, that function makes an SQL query to a table called... `member_gear_requests`.

```js,name=gear.js
export function getIndividualRequestedGear(db, tripId) {
  // Some SQL query here, to the effect of:
  // SELECT ...
  // FROM member_gear_requests
}
```

In summary, here are all the names I gave to the concept of "gear that trip participants requested for their personal use":

* Individual Gear
* member_requested_gear
* memberRequestedGear
* (get)IndividualRequestedGear
* member_gear_requests

That turned out to be an even stupider example than I expected (I wrote 100% of that code myself, by the way).

Some of these are necessary.
The frontend is *supposed* to be a friendlier representation of the data than the code; we're not going to use snake case for the `<h3>`.
But if I had named the table correctly and didn't bother with camel case variable names, we could easily have had the following:

* Individual Gear (in the frontend)
* getIndividualGearRequests (as a function)
* individual_gear_requests (in the database and all variable names)

<aside>
A braver person than me would also tell you to use snake case for the function as well.
I think functions and variables are different enough, conceptually, that it doesn't matter.
But feel free!
</aside>

## Takeaways

Codebases, like the rings on a tree, reflect the varying conditions that produced them over time.
For this application:

1. I was re-writing an existing MongoDB + ReactJS app to [SQLite + htmx](@/blog/building-the-hundred-year-web-service.md)
2. This was my first time doing #1 and I was learning patterns for it as I progressed

In general, it's important to have grace for the process by which a codebase grows, which necessarily leaves behind knots and scars as indicators of progress.
So here's a couple of the knots.

### If you're not willing to change it everywhere, don't change it anywhere

One lesson from this case study is not to switch between "individual" and "member," at random.
That happened because I wanted to change what the thing was called, but didn't feel like doing the migrations and grepping required to do it properly.
It's reasonable to change the name, it's reasonable not to change the name—but pick one.
Otherwise: [squish like grape](https://www.youtube.com/watch?v=dhAJ2PL3_XY).

(Once again, this doesn't apply to anything that users see, which often doesn't match up perfectly with what's in the database)

Many codebases experience semantic drift over time, as multiple people with different ideas work on it and new requirements get added.
But in my case that was just a huge unforced error.

You have permission to laugh at me for up to 20 seconds.

### If you use SQL, adopt snake case variables

SQL has the annoying limitation that if you want upper-case letters in your table or column names, you have to quote them:

```sql
-- Classic SQL
SELECT first_name, last_name
FROM users
WHERE first_name like 'Alex%';

-- These columns you have quote with double quotes.
-- Unlike string literals, which are single quotes!
SELECT "firstName", "lastName"
FROM users
WHERE "firstName" like 'Alex%';
```

The quoting rules are slightly different depending on the implementation, which is also irritating.
The point is: stick to snake case names, and you're fine.

With that constraint in place, we then have to use the values in our application.
At first, it feels natural to translate the snake case SQL column name into something that matches your programming language's casing convention.

If you can at all avoid it, don't.
Calling something `first_name` in the database but `firstName` in the application code is just not worth it.
Changing case provides an unnecessary surface for inconspicuous bugs, and makes it meaningfully harder to search your codebase for all the usages of a particular concept.
It accomplishes nothing besides scratching your own itch for "cleanliness."
As much as possible, `first_name` should always be `first_name`.

Many ORMs (the libraries that translate database queries into application logic) will perform a casing translation for you (see: [Hibernate](https://www.baeldung.com/hibernate-naming-strategy), [Sequelize](https://sequelize.org/docs/v6/other-topics/naming-strategies/)).
This, too, is an opportunity for strange bugs, in which queries fail because the casing translation doesn't work the way you, or the ORM, expected.
It's an obvious error once you see it, but reading through strange, auto-generated SQL (if the stack trace even includes that by default), is a chore.

<aside>I picked Hibernate and Sequelize as examples because I got hit with this exact problem in both of those ORMs.</aside>

If you're planning to basically never write SQL and you trust the ORM's magic renaming (not my style, but to each their own), or you are using a database that doesn't have this constraint, then this note doesn't apply to you.
That's fine too.

Follow naming conventions where you can; jettison them when they require you to rename something for no reason other than convention.

### Don't abbreviate

This one doesn't really come up in the case study but it's helpful and relevant: resist the temptation to abbreviate.

If it's called `start_time` in one place, don't assign it to `start` somewhere else.
Again, just not worth it.

You're only going to type that code once, but you will likely search the codebase for `start_time` more than once, and you do not want to have to worry about alternative names, spellings, or abbreviations.
Over the lifetime of an application, especially one that might change hands, that matters.

Java is the language that most tempts you to come up with abbreviated names for things, because the [Kingdom of Nouns](https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html) is vast indeed.
Java also has such great tooling that it's easy to tell yourself that code inspection will never fail to find the thing you're looking for.
Write the whole thing out and your future self will thank you while typing CMD+SHIFT+F into IntelliJ.

## Conclusion

I'm confident there are situations when it's wise to assign multiple names to the same concept.
As I lead with, there simply aren't any hard rules in coding.

But this is a good one, and it's mostly true: **do not give multiple names to the same thing**.

# Notes

* Software Engineering is an almost entirely abstract practice, so it's not always obvious whether two concepts constitute the same concept—especially since they're all concepts someone made up.
Properly unplacking *that* requires layers of philosophy that I, unfortunately, do not have ready to go.
I think Plato is probably the right place to start?
* I recently had a situation where my database conventions lost to a more important constraint.
In SQL databases I like to give all primary keys unique names (i.e. `users.user_id` instead of `users.id`), since that lets you take advantage of the `USING` syntax.
In an ActivityPub application I'm working on, this rule lost to the naming rule, because ActivityPub *does* use [`id` as an identifier](https://www.w3.org/TR/activitypub/#actor-objects) for every possible type of object.
I figured that out a little late and did go through the effort to write the migration; this turned out to be the right call.
* I'm mildly curious if anyone will respond to this by saying that they've never searched their codebase for an identifier, preferring instead to rely on LSP go-to-definition or (*sigh*) hoping the AI tool won't miss anything.
Even if that's true, text is the universal interface through which we interact with almost all code; navigating code at that level (as text) is an essential skill that makes you comfortable even in unfamiliar languages and environments.
