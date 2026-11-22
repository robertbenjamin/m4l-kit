/** Live Device Kit drawing API (window.LiveKit). All coordinates are body px at Live's 100 % zoom. */
export interface DeviceOptions { /** body width in px */ w: number; /** CSS zoom for viewing, default 2 */ zoom?: number; /** colour token for the body ground, e.g. "title" for tiled devices */ ground?: string; /** false hides the title bar */ title?: boolean; /** false keeps this device out of ?ref=1 mode (by default the first device on the page is the reference) */ ref?: boolean }
export interface DialProps { /** ring centre x */ cx: number; /** label cap top y (band: 120) */ cap: number; label?: string; value?: string; /** 0..1 position */ v: number; /** arc from centre */ bipolar?: boolean; /** ± notch above the ring */ notch?: boolean; /** 37 px ring */ large?: boolean; /** arc colour token, default "teal" */ color?: string }
export interface MeterProps { x: number; y: number; h: number; peak?: number; rms?: number; stereo?: boolean; /** gain reduction in dB: draws an orange bar from the top */ gr?: number; /** dB of the triangle marker */ marker?: number; /** dim the level above this dB */ dimAbove?: number; label?: string; value?: string; valueColor?: string }
export interface Device {
  display(x: number, y: number, w: number, h: number): Device;
  tile(x: number, y: number, w: number, h: number, fill?: string): Device;
  divider(x: number, y: number, h: number): Device;
  dial(p: DialProps): Device;
  numbox(x: number, y: number, w: number, value: string, frac: number): Device;
  button(x: number, y: number, w: number, label: string, state?: "on" | "outline" | "off" | "mapped" | "mapped-on"): Device;
  toggle(x: number, y: number, w: number, label: string, on: boolean): Device;
  connector(x1: number, x2: number, y: number): Device;
  readout(x: number, cap: number, label: string, value: string): Device;
  inlineReadout(x: number, cap: number, label: string, value: string): Device;
  dropdown(x: number, y: number, w: number, label: string): Device;
  chooser(x: number, cap: number, label: string): Device;
  pointer(x: number, y: number, dir?: "down" | "left"): Device;
  graph(x: number, y: number, w: number, h: number, pts: [number, number][], o?: { border?: boolean; cross?: boolean; color?: string; under?: (d: Device) => void }): Device; /** the curve is clipped to the area inside the border */
  freqGrid(x: number, y: number, w: number, h: number, lo?: number, hi?: number, marks?: [number, string][]): Device;
  handle(cx: number, cy: number): Device;
  /** 5 px indicator light; off is led-off, on is led-on unless a colour token is given */
  led(cx: number, cy: number, on: boolean, color?: string): Device;
  meter(p: MeterProps): Device;
  fold(x: number, y: number, open: boolean): Device;
  text(x: number, cap: number, s: string, o?: { align?: "left" | "center" | "right"; color?: string; size?: number; weight?: number }): Device;
  titleName(name: string, fold?: "open" | "closed"): Device;
}
/** Set when the page is opened with ?ref=1&zoom=Z&theme=T. The first device then draws alone: body only, no title,
 * at zoom Z, theme class th-T, on #ff00ff. The page should draw its default state in silence while this is set. */
export interface RefMode { zoom: number; theme: "dark" | "light" | "light-cool" }
export declare const LiveKit: { device(el: HTMLElement, o: DeviceOptions): Device; textWidth(s: string, size?: number, weight?: number): number; ref: RefMode | null };
