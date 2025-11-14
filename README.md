# Octoclip

Octoclip generates collectible-style octopus prompts, bundles them into a JSON payload, and copies the result to your clipboard via a small shell helper.

## What it does

- `generate_octopus_prompt.py` reads from `octopus_traits.json` to choose skin colors, accessories, expressions, and other traits for a single octopus subject.
- The CLI script formats everything into a structured prompt plus metadata that you can feed into a generative tool or log for later use.
- `octoclip.zsh` exposes an `octoclip` shell function you can source in `~/.zshrc`. The helper runs the generator, prints the JSON payload, copies it to the clipboard, and reports success.

## Getting started

1. Create a Python 3 virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install any dependencies (none beyond the standard library at the moment).
3. Run the generator manually if you want to inspect the JSON:
   ```bash
   python3 generate_octopus_prompt.py
   ```
4. Source the helper in your shell (or add it to `~/.zshrc`):
   ```bash
   source octoclip.zsh
   ```
5. Call `octoclip` (optionally passing the number of tentacle accessories to include, defaults to 1):
   ```bash
   octoclip 2
   ```

## Configuration

- `octopus_traits.json` defines color pools, accessories, outfits, and prompts. Edit it to adjust palettes or add new accessories.
- `generate_octopus_prompt.py` currently samples 1–3 tentacle accessories. If you want more control, adjust the selection logic there.

## Contributing

1. Fork the repo, make changes, and test via `python3 generate_octopus_prompt.py`.
2. Keep trait JSON updates consistent with the prompt wording.

## License

This project has no license file; assume default owner rights unless you add one.
