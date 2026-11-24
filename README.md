# akintayoakingbehin.com

Static site. Plain HTML, one stylesheet, one script. No build tools, no
`node_modules`, no server code. GitHub serves the `.html` files in this folder
exactly as they are.

## Preview locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Folder layout

```
index.html  work.html  sports.html  services.html  about.html  contact.html
fremont-table-tennis.html  table-tennis-usa.html  gewo-usa.html
octagon.html  starting-eleven.html  proof.html  404.html
css/site.css      js/site.js
assets/img/...    assets/video/...
sitemap.xml  robots.txt  favicon.svg  .nojekyll  build.py
```

`paul-david.html` is still on disk but is `noindex`, is not linked from
anywhere, and is not in the sitemap.

## Editing

The `.html` files are the deployed site, so you can edit any of them directly.

For anything that appears on more than one page — the header, the CTA block,
the footer, the nav — edit `build.py` and run:

```bash
python3 build.py
```

That rewrites all 13 pages. **It overwrites the HTML**, so don't mix the two
methods on the same page. `build.py` is an authoring convenience only; it never
runs on the server.

## Adding a project

1. Put the screenshot in `assets/img/`.
2. Add an entry to the `PROJECTS` list near the top of `build.py` — `href`,
   `sport` (`table-tennis` or `football`, which drives the Work page filter),
   `label`, `name`, `line`, `im` (file, width, height) and `alt`.
3. Add a `build_*()` function for its page, modelled on `build_octagon()`, and
   add it to the list in `__main__` and to `PUBLIC`.
4. Update the counts in the Work page filter buttons.
5. Run `python3 build.py`.

## Swapping the testimonial video

Replace `assets/video/testimonial.mp4` and `assets/img/testimonial-poster.jpg`.
Keep the video well under 50MB — GitHub warns above that and blocks at 100MB.
To compress:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow \
       -c:a aac -b:a 96k -movflags +faststart testimonial.mp4
```

Grab a poster frame from it:

```bash
ffmpeg -ss 2 -i testimonial.mp4 -frames:v 1 -q:v 3 testimonial-poster.jpg
```

The caption under the video is a `<!-- TODO -->` in `build_home()` — fill in the
client's name, role and organisation there.

To add a second testimonial later, duplicate the `<figure class="testimonial">`
block. Nothing else needs changing.

## Missing assets

The page renders a styled placeholder wherever an image is absent, so nothing
breaks. Drop these into `assets/img/` and they appear automatically:

- `fremont-programs.jpg`
- `sport-table-tennis.jpg`, `sport-football.jpg`, `sport-cricket.jpg`,
  `sport-volleyball.jpg`, `sport-field-hockey.jpg`, `sport-ice-hockey.jpg`

## Things not to break

- **No prices on the site.** Scope and price go out in writing after a review.
- **No revenue figures.** The Table Tennis USA sales data belongs to the client.
- **No invented testimonials, results, awards or social links.**
- The Fremont case study has a dashed "Result" box with a `<!-- TODO -->`.
  Either put a real number in it or delete the whole section before launch.
