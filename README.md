# akintayoakingbehin.com

Static site. Plain HTML, one stylesheet, one script. No build tools, no
`node_modules`, no server code. GitHub serves the `.html` files in this folder
exactly as they are.

## Preview locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Folder layout — everything is flat, and that is deliberate

Every file sits at the root. `site.css`, `site.js`, the images and the video are
beside the HTML, and the HTML refers to them by plain filename: `site.css`,
not `/site.css` and not `css/site.css`.

```
index.html  work.html  sports.html  services.html  about.html  contact.html
fremont-table-tennis.html  table-tennis-usa.html  gewo-usa.html
octagon.html  starting-eleven.html  proof.html  404.html
site.css  site.js  testimonial.mp4  *.jpg  *.png
sitemap.xml  robots.txt  favicon.svg  .nojekyll  build.py
```

**Do not move files into subfolders.** A leading slash breaks on a GitHub Pages
project URL, and a subfolder breaks the moment a folder does not survive an
upload — which is exactly what happened the first time this redesign went up:
`index.html` arrived but `css/`, `js/` and `assets/` did not, so the page
rendered as raw unstyled text. Flat filenames survive both.

**Upload the contents of this folder, not the folder itself.** After deploying,
load the site: it should have a cream background and navy type. If it looks like
plain blue links on white, `site.css` is not being found.

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

Replace `testimonial.mp4` and `testimonial-poster.jpg`.
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

The caption under the video is in `build_home()` — currently Ben Nisbet, CEO &
founder of Table Tennis Store USA and GEWO USA.

To add a second testimonial later, duplicate the `<figure class="testimonial">`
block. Nothing else needs changing.

## Optional images

The Sports page renders a styled placeholder wherever a photo is absent, so
nothing breaks. Drop any of these into the root folder and they appear
automatically, on the Sports page and as the hover preview on the home page:

- `sport-table-tennis.jpg`, `sport-football.jpg`, `sport-cricket.jpg`,
  `sport-volleyball.jpg`, `sport-field-hockey.jpg`, `sport-ice-hockey.jpg`

## Things not to break

- **No prices on the site.** Scope and price go out in writing after a review.
- **No revenue figures.** The Table Tennis USA sales data belongs to the client.
- **No invented testimonials, results, awards or social links.**
- The Fremont case study's Result box deliberately carries no figure. The
  before-and-after screenshots on that page are the evidence. If the academy
  ever shares a sign-up number you can add it, but do not invent one.
