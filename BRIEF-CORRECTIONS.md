# Brief corrections

Where the brief was wrong, or where this repository did something other than it says, and why. The brief itself is never edited.

## C-01 · The domain: investor or investors?

The brief says **investor.sgit.ai**; the repository's README, written when the repository was created, said investors.sgit.ai. The site uses investor.sgit.ai, as the brief does. No CNAME is committed until the DNS exists (board 003).

## C-02 · Section 4 built in the first version

The build brief says "first version: the first three, then the rest". The evaluation framework's source could be read in full on 29 October 2026, so it was built as a working scorecard in the same session. Sections 5 to 8 are pages marked proposed.

## C-03 · The build is stdlib Python with plain classes, not Type_Safe

The repository guidance asks for Type_Safe data classes in Python. The build uses only the standard library so that it fetches nothing at build time and needs no vendored dependency. It keeps the other rules: classes, no module-level functions. To revisit if the build grows.

## C-04 · GitHub Actions pinned by major version, not commit hash

The guidance asks for dependencies pinned and hashed. The workflow uses `actions/checkout@v4`, `setup-node@v4`, `upload-pages-artifact@v3` and `deploy-pages@v4`. Pinning by commit hash is a security task (board, to add).

## C-05 · CI builds the pages, so there is no pending version

The newsroom builds against a pending version because CI cannot run its generator. This site's build runs in CI, so the release job writes the number and then builds. The guard is different too: the `version` file at the pushed head must equal the latest tag.

## C-06 · The news section ships empty

The brief asks for the news from investor circles. Who writes the feed is an open question in the brief, and items must be public, dated, linked and checked, so the first version publishes the rules, the schema and an empty ledger rather than unchecked items.

## C-07 · Corrected in our own data before publishing

The first draft of the option pool change note said the smaller pool moved "about 1.5 points" to the existing shareholders. The build computed 2.00 points for the founders alone. The note now points to the computed figure instead of stating one.
