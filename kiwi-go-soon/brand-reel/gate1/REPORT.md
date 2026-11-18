# Gate 1: style frames, report (saved by the orchestrator from the production agent's hand-back)

- Credits: 488.92 before → 465.17 after. **Spend 23.75** (the exact hard budget).
- Made:
  - 3 sheets: seller and courier on seedream_5_5 2k; truck + parcel on gpt_image_2_6 high 2k.
  - 14 start frames: gpt_image_2_6 medium 2k 9:16, each referencing the sheets.
- Picks: S1-b, S2-a, S3-start-b, S3-end-a, S4-a, S5-b. All of them PASS.
- FAIL: S6-a and S6-b. Two hi-vis worker dolls leaked in from the truck sheet, and the truck is too small (rear wheel about 140 px vs the planned 300 px). The truck design itself is correct. There was no budget left to retry.
- All 17 images: no text, logos or plates; the felt look is consistent; no face or hand distortion; nothing culturally off.
- Sheet notes:
  - The courier's trainers have three stripes that read as a sportswear brand. This is suppressed in the frames.
  - The courier has a beard the brief didn't ask for (client decision).
  - The truck sheet contains 2 unrequested figures.

## Fixes for Gate 2/3
1. Regenerate OB-1 "objects only, no people" (2.75 cr), or upload a clean crop (needs upload.higgsfield.ai allowed).
2. S6: "no people; truck fills about 85 % of frame width; rear wheel centre at 59 % of the width and 42 % of the height; wheel about 28 % of the width". Or use the 0-cr 2.5D fallback.
3. Courier: "plain all-ink trainers, no stripes"; "clean-shaven" if the client rejects the beard (re-sheet, 3.5 cr).
4. Lime: "no lime specks in hair/clothing; foliage muted sage green"; paint out leftovers in post.
5. S1 vs S5 contrast:
   - S1: lamps off, cool phone glow, tired face.
   - S5: warm golden lamp and morning light, the seller softly defocused. This can also be done in the grade.
6. S3-start: a tiny truck (1/20 of the frame width), the city hidden, a plain front.
7. S3-end: no people.
8. S4: her full figure between y 450–950, with empty paving below.
9. Rate limits: at most about 6 items per batch; check the balance before resubmitting.

Files: sheet-*.png, S*-a/b.png, jobs.json, contact-sheet.png, picks.png.
