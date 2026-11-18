"""Beat-marker sheets (07 §1.5 verbatim for the master; §1.6 for the cut-down)."""

BEATS = {
    'master': """# Kiwi Go hero Reel — master 20.000 s, 24 fps, 120 BPM, 4/4. TC = seconds; frame = TC*24
0.000  f000  B1.1  HIT    hook frame 0, bubble 1 «где моя посылка?»
0.500  f012  B1.2  pop    bubble 2
1.000  f024  B1.3  pop    bubble 3
1.500  f036  B1.4  SEND   lime bubble «Отправлено ✓»
2.500  f060  B2.2  HIT    light-leak cut to pickup (riser 1.5→2.5)
3.000  f072  B2.3  accent courier turns
4.500  f108  B3.2  whip   whip-pan cut to journey
6.000  f144  B4.1  SWELL  crane begins rising; chip «В пути»
8.000  f192  B5.1  swell-top chip «В городе»
8.500  f204  B5.2  cut    haze cut to arrival
9.000  f216  B5.3  accent chip «У курьера»
11.000 f264  B6.3  cut    glow cut to payoff
11.500 f276  B6.4  accent bubble «получила, спасибо!»
12.000 f288  B7.1  BREATH (drop out, one beat)
12.500 f300  B7.2  re-entry truck shot
14.000 f336  B8.1  HIT    kiwi wheel born (light sweep)
15.000 f360  B8.3  PEAK   flash cut to card
16.000 f384  B9.1  accent price
16.500 f396  B9.2  CTA    «Оформите доставку» + kiwigo.kg
17.000 f408  B9.3  accent WhatsApp line
19.500 f468  B10.4 loop   resolve; loop point at 20.000 → 0.000
""",
    'cutdown': """# Kiwi Go hero Reel — cut-down 10.000 s, 24 fps, 120 BPM, 4/4. TC = seconds; frame = TC*24
0.000  f000  B1.1  HIT    hook frame 0, bubble 1 «где моя посылка?»
0.500  f012  B1.2  pop    bubble «??»
1.500  f036  B1.4  SEND   lime bubble «Отправлено ✓»
2.000  f048  B2.1  HIT    light-leak cut to pickup
2.500  f060  B2.2  accent courier turns
3.500  f084  B2.4  whip   whip-pan cut to journey
4.000  f096  B3.1  SWELL  chip «В пути»; swell B3.1–B3.4
5.500  f132  B3.4  cut    haze cut to truck
5.700  f137  —     accent front wheel turns kiwi (light sweep)
6.000  f144  B4.1  HIT    kiwi wheel born (rear wheel)
6.500  f156  B4.2  PEAK   flash cut to card
7.000  f168  B4.3  accent price
7.500  f180  B4.4  CTA    «Оформите доставку» + kiwigo.kg
8.000  f192  B5.1  accent WhatsApp line
9.500  f228  B5.4  loop   resolve; loop point at 10.000 → 0.000
""",
}
