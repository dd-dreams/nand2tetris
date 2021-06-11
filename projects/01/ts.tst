load Mux415.hdl,
output-file Mux415.out,
output-list a%B1.16.1 b%B1.16.1 sel%B2.2.2 out%B1.16.1;

set a %B0001001000110100,
set b %B1001100001110110,
set sel 0,
eval,
output;

set sel 1,
eval,
output;
