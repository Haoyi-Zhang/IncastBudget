# Clean-package verification protocol

The release is accepted only after a fresh extraction performs all of the following without modifying the source archive:

1. Verify every entry in `MANIFEST.sha256`.
2. Compile all Python sources and run the complete test suite under two hash seeds.
3. Run `reproduce.py --part first` and `--part second`.
4. Run `reproduce_review_all.py --include-external-oracle`.
5. Compare normalized scientific JSON from the project artifact and standalone artifact.
6. Rebuild the main paper and supplement from source.
7. Require a 12-page US-Letter main PDF, embedded fonts, qpdf-clean streams, no unresolved reference, no overfull box, and successful rendering of every page.
8. Compare the rebuilt paper and supplement text with the delivered PDFs.

The external file `incast-safe-queue-budget-package-verification-FINAL.json` records the final execution of this protocol.
