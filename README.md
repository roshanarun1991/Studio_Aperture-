# Studio Aperture — Website

## Adding your own photos (no code editing needed)

1. Open the `images/` folder. Inside it you'll find one folder per gallery:
   `portrait`, `weddings`, `landscape`, `street`, `fashion`, `product`
   (plus two optional ones: `hero` for the homepage slideshow, and `about`
   for the studio photo).

2. Drop your photos into the matching folder — `.jpg`, `.jpeg`, `.png`, or
   `.webp`. Any filename works, e.g. `IMG_0231.jpg`.

3. Re-run the update script:
   - **Mac:** double-click `update-images.command`
     (first time only: right-click → Open, to bypass the "unknown developer" warning)
   - **Windows:** double-click `update-images.bat`
   - **Either OS, via terminal:** `python3 generate_manifest.py`

4. Refresh the site in your browser. Your photos now appear automatically —
   the first photo in each folder becomes the homepage cover image, and
   every photo in the folder appears on that category's detail page, in
   filename order.

`index.html` never needs to be opened or edited for this — it just reads
`images/manifest.json`, which the script regenerates for you.

## Notes

- If a folder is empty, that gallery keeps its built-in placeholder photos,
  so the site never looks broken.
- The `hero` and `about` folders are optional — leave them empty to keep
  the default homepage photos.
- Photo order = filename order (`1.jpg`, `2.jpg`, `3.jpg`... works well).
- Requires Python 3 to run the update script (already installed on most
  Macs; on Windows, install from python.org and check "Add to PATH").

## Running the site

Open this folder in VS Code and use the **Live Server** extension
("Go Live" in the bottom-right corner) to preview `index.html`.

## How the contact form and "Choose package" buttons work

Both the contact form and the pricing "Choose [package]" buttons open the
visitor's own default email app with a message already filled in —
addressed to `sahith.yellabonu@gmail.com`. The visitor just needs to review it
and hit send. This only works if the visitor has an email app configured
on their device (e.g. Mail, Outlook, Gmail app set as default) — on a
device with no default mail app, nothing will visibly happen when they
click.
