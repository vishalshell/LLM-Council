# Contributing to LLM Council Vetting Harness

Thank you for considering a contribution! The project is in rapid development; your bug reports and pull‑requests are welcome.

## Pull‑Request checklist

1. Fork ➜ feature branch (`feat/…`, `fix/…`).
2. Follow [Conventional Commits](https://www.conventionalcommits.org/).
3. Run `pytest -q` and ensure all tests pass.
4. If you add a dependency, update **requirements.txt**.
5. Update `README.md` / wiki if behaviour changes.
6. Target the **dev** branch; we squash‑merge to **main**.

## Project style

* Python ≥ 3.11
* Black + isort (pre‑commit coming soon)
* Docstrings: Google style

## Reporting bugs

Open an issue with:

* Repro steps
* Expected vs actual behaviour
* Stack trace or error snippet