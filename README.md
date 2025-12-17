# Unplanned Obsolescence
New blog, this one's about web development. You can find it here:
[https://unplannedobsolescence.com](https://unplannedobsolescence.com)

## Running it
It runs on [zola](https://github.com/getzola/zola), which you will need to install. Then run `zola
serve` in the source root.


## Making Drafts

Add the following to the blog's front matter.

```toml
[extra]
hidden=true
```

## Fonts

The fonts is [Valkyrie](https://mbtype.com/fonts/valkyrie/) by [Matthew Butterick](https://mbtype.com/bio.html).
It is not committed and needs to be included in `./static/fonts` separately.
