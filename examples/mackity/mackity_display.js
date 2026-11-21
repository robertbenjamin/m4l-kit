// Mackity display, drawn like the design's Graph and ClipLight with Live theme colours.
// jsarguments: curve | led | meterframe. Messages: "drive <A>" (raw In Trim), "level <x>" (driven input peak).

autowatch = 1;
mgraphics.init();
mgraphics.relative_coords = 0;
mgraphics.autofill = 0;

var MODE = jsarguments.length > 1 ? jsarguments[1] : "curve";
var st = { drive: 0.1 };
var RELEASE = 0.39;   // s; shows on screen as Saturator's measured 0.30 s fade
var LED_FULL = 0.65;  // Saturator's lit soft-clip light is the theme teal at about 65 %
var env = 0, glow = 0, last = 0;
// x half-range in driven units at 0 dB; above 0 dB it zooms out by sqrt(drive gain), as Saturator's does
var DOM0 = 1.5;
function dom() { return DOM0 * Math.sqrt(Math.max(1, 100 * st.drive * st.drive)); }
var LED_OFF = 0.83;   // Saturator's unlit light: #141414 on its #181818 display
// Saturator's band opacity, measured against a known band in the same screen recording
var BAND_ALPHA = 0.27;

// v8ui does not route messages to plain top-level functions ("no function drive"): use anything()
function level(x) {
	var now = Date.now(), k = last ? Math.exp(-(now - last) / 1000 / RELEASE) : 0;
	last = now;
	env = Math.max(x, env * k);
	// brightness follows how far past the clamp it goes: 0 dB over = dark, 6 dB over = full
	var over = x > 1 ? Math.min(1, 20 * Math.log(x) / Math.LN10 / 6) : 0;
	glow = Math.max(over, glow * k);
	mgraphics.redraw();
}

function anything() {
	if (messagename === "level") { level(arguments[0]); return; }
	if (messagename in st && arguments.length) { st[messagename] = arguments[0]; mgraphics.redraw(); }
}

function setc(id, alpha) {
	var c = max.getcolor(id);
	mgraphics.set_source_rgba(c[0], c[1], c[2], alpha === undefined ? (c.length > 3 ? c[3] : 1) : alpha);
}
function shaper(x) { x = Math.max(-1, Math.min(1, x)); return x - Math.pow(x, 5) * 0.1768; }

// a thrown error would leave the box blank; error() reaches Max's console, which Live copies to Log.txt
function paint() {
	try { draw(); } catch (e) { error("mackity_display: " + e + "\n"); }
}

function draw() {
	var s = mgraphics.size, w = s[0], h = s[1];
	if (MODE === "led") {
		// Max widens the box to 10 px, so place the dot from the design's 9 px box, not w / 2
		var a = max.getcolor("live_value_arc"), b = max.getcolor("live_lcd_bg");
		var lo = [b[0] * LED_OFF, b[1] * LED_OFF, b[2] * LED_OFF], hi = [a[0] * LED_FULL, a[1] * LED_FULL, a[2] * LED_FULL];
		mgraphics.set_source_rgba(lo[0] + (hi[0] - lo[0]) * glow, lo[1] + (hi[1] - lo[1]) * glow, lo[2] + (hi[2] - lo[2]) * glow, 1);
		mgraphics.ellipse(2, 2, 5, 5);
		mgraphics.fill();
		return;
	}
	var DOM = dom();
	var px = function (v) { return Math.max(1.75, Math.min(w - 1.75, w / 2 + v / DOM * (w / 2))); };
	// v8ui has no clip(): keep the curve inside the border by hand
	var py = function (v) { return Math.max(1.75, Math.min(h - 1.75, h / 2 - v * (h / 2 - 6))); };
	var reach = Math.min(DOM, env);
	if (MODE === "meterframe") {
		w = 11; h = 84;   // the design's box: Max rounds v8ui sizes up
		setc("live_spectrum_grid_lines");
		mgraphics.set_line_width(1);
		mgraphics.rectangle(0.5, 0.5, w - 1, h - 1);
		mgraphics.stroke();
		return;
	}
	// Saturator draws the band over the crosshair
	setc("live_spectrum_grid_lines");
	mgraphics.set_line_width(1);
	mgraphics.move_to(w / 2, 1); mgraphics.line_to(w / 2, h - 1);
	mgraphics.move_to(1, h / 2); mgraphics.line_to(w - 1, h / 2);
	mgraphics.stroke();
	setc("live_value_arc", BAND_ALPHA);
	var x0 = Math.max(1, px(-reach)), x1 = Math.min(w - 1, px(reach));
	if (x1 - x0 > 0.5) { mgraphics.rectangle(x0, 1, x1 - x0, h - 2); mgraphics.fill(); }
	setc("live_spectrum_grid_lines");
	mgraphics.rectangle(0.5, 0.5, w - 1, h - 1);
	mgraphics.stroke();
	setc("live_value_arc");
	mgraphics.set_line_width(1.5);
	for (var i = 0; i <= 120; i++) {
		var v = -DOM + 2 * DOM * i / 120;
		if (i === 0) mgraphics.move_to(px(v), py(shaper(v))); else mgraphics.line_to(px(v), py(shaper(v)));
	}
	mgraphics.stroke();
}

// repaint after an autowatch reload, which otherwise leaves the box blank
mgraphics.redraw();
